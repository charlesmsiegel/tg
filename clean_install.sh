#!/usr/bin/env bash
set -Eeuo pipefail

fail() {
    echo "ERROR: $*" >&2
    exit 1
}

if [[ "${EUID}" -eq 0 ]]; then
    fail "Run clean_install.sh as your normal login user, not with sudo. The script requests sudo itself immediately."
fi

echo "Requesting sudo access for system setup..."
sudo -v

# Keep the sudo timestamp alive while the install runs so authorization is requested once,
# right at the beginning.
while true; do
    sudo -n true 2>/dev/null || exit
    sleep 60
done &
SUDO_KEEPALIVE_PID=$!

cleanup() {
    kill "${SUDO_KEEPALIVE_PID}" 2>/dev/null || true
}
trap cleanup EXIT
trap 'echo "ERROR: clean_install.sh failed at line ${LINENO}. See the command output above." >&2' ERR

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"
REPO_ROOT="${PWD}"
APP_USER="$(id -un)"
APP_GROUP="$(id -gn)"
VENV="${REPO_ROOT}/.venv"
PYTHON="${VENV}/bin/python"
PIP="${VENV}/bin/pip"
DAPHNE="${VENV}/bin/daphne"

[[ -f "${REPO_ROOT}/manage.py" && -d "${REPO_ROOT}/tg" ]] || \
    fail "This script must be run from the root of the tg repository."

[[ -f "${REPO_ROOT}/.env" ]] || fail \
    "No .env file found. Copy your production .env into ${REPO_ROOT}/.env and run this script again."

sudo chown "${APP_USER}:${APP_GROUP}" "${REPO_ROOT}/.env"
chmod 600 "${REPO_ROOT}/.env"

if [[ ! -r /etc/os-release ]]; then
    fail "Cannot identify the operating system; this installer supports Ubuntu Server."
fi
# shellcheck disable=SC1091
source /etc/os-release
[[ "${ID:-}" == "ubuntu" ]] || fail \
    "This installer supports Ubuntu Server; detected ${PRETTY_NAME:-an unknown operating system}."

echo
echo "==> Installing Ubuntu packages"
export DEBIAN_FRONTEND=noninteractive
sudo apt-get update
sudo apt-get install -y \
    acl \
    build-essential \
    ca-certificates \
    curl \
    git \
    libffi-dev \
    libfreetype6-dev \
    libjpeg-dev \
    libssl-dev \
    nginx \
    openssl \
    pkg-config \
    python3 \
    python3-dev \
    python3-pip \
    python3-venv \
    redis-server \
    sqlite3 \
    zlib1g-dev

python3 - <<'PY'
import sys

if sys.version_info < (3, 10):
    raise SystemExit(
        f"Python 3.10+ is required; this Ubuntu install provides "
        f"{sys.version_info.major}.{sys.version_info.minor}."
    )
PY

echo
echo "==> Creating Python virtual environment and installing dependencies"
if [[ ! -x "${PYTHON}" ]]; then
    python3 -m venv "${VENV}"
fi
"${PYTHON}" -m pip install --upgrade pip wheel setuptools
"${PIP}" install -r "${REPO_ROOT}/requirements.txt"

mkdir -p \
    "${REPO_ROOT}/logs" \
    "${REPO_ROOT}/media" \
    "${REPO_ROOT}/collected_static"

echo
echo "==> Validating .env"
"${PYTHON}" - <<'PY'
from dotenv import dotenv_values

values = dotenv_values(".env")
environment = (values.get("DJANGO_ENVIRONMENT") or "").strip().lower()
secret = (values.get("SECRET_KEY") or "").strip()
hosts = (values.get("DJANGO_ALLOWED_HOSTS") or "").strip()

errors = []
if environment != "production":
    errors.append("DJANGO_ENVIRONMENT must be production")
if not secret or "CHANGE-THIS" in secret or "django-insecure-default-key" in secret:
    errors.append("SECRET_KEY must contain a real production secret")
if not hosts:
    errors.append("DJANGO_ALLOWED_HOSTS must list at least one host")

if errors:
    raise SystemExit("Invalid production .env:\n  - " + "\n  - ".join(errors))
PY

echo
echo "==> Enabling Redis"
sudo systemctl enable --now redis-server
sudo systemctl is-active --quiet redis-server || fail "redis-server did not start."

echo
echo "==> Building database and static assets"
"${PYTHON}" manage.py makemigrations --noinput
"${PYTHON}" manage.py migrate --noinput
"${PYTHON}" manage.py collectstatic --noinput
"${PYTHON}" manage.py populate_gamedata
"${PYTHON}" manage.py check --deploy

echo
echo "==> Granting nginx read access to static and uploaded files"
# nginx runs as www-data on Ubuntu. Grant traverse-only access to parent directories,
# then read access to the two trees it serves. Default ACLs make future media/static
# files readable without opening the rest of the repository.
parent="${REPO_ROOT}"
while [[ "${parent}" != "/" ]]; do
    sudo setfacl -m u:www-data:x "${parent}"
    parent="$(dirname "${parent}")"
done

for served_dir in "${REPO_ROOT}/collected_static" "${REPO_ROOT}/media"; do
    sudo find "${served_dir}" -type d -exec setfacl -m u:www-data:rx,d:u:www-data:rx {} +
    sudo find "${served_dir}" -type f -exec setfacl -m u:www-data:r {} +
done

echo
echo "==> Installing the systemd service"
sudo tee /etc/systemd/system/tg.service >/dev/null <<EOF
[Unit]
Description=Tellurium Games Django ASGI server
After=network-online.target redis-server.service
Wants=network-online.target redis-server.service

[Service]
Type=simple
User=${APP_USER}
Group=${APP_GROUP}
WorkingDirectory=${REPO_ROOT}
Environment=PYTHONUNBUFFERED=1
ExecStart="${DAPHNE}" --proxy-headers -b 127.0.0.1 -p 8000 --access-log - tg.asgi:application
Restart=always
RestartSec=5
TimeoutStopSec=30
UMask=0027

[Install]
WantedBy=multi-user.target
EOF

echo
echo "==> Creating a first-boot TLS certificate"
sudo install -d -m 0755 /etc/ssl/tg
TLS_KEY=/etc/ssl/tg/tg-selfsigned.key
TLS_CERT=/etc/ssl/tg/tg-selfsigned.crt

if [[ ! -s "${TLS_KEY}" || ! -s "${TLS_CERT}" ]]; then
    HOST_FQDN="$(hostname -f 2>/dev/null || hostname)"
    HOST_IP="$(hostname -I 2>/dev/null | awk '{print $1}')"
    SAN="DNS:${HOST_FQDN},DNS:localhost,IP:127.0.0.1"
    if [[ -n "${HOST_IP}" ]]; then
        SAN="${SAN},IP:${HOST_IP}"
    fi

    sudo openssl req \
        -x509 \
        -nodes \
        -newkey rsa:3072 \
        -sha256 \
        -days 3650 \
        -keyout "${TLS_KEY}" \
        -out "${TLS_CERT}" \
        -subj "/CN=${HOST_FQDN}" \
        -addext "subjectAltName=${SAN}"
    sudo chmod 600 "${TLS_KEY}"
    sudo chmod 644 "${TLS_CERT}"
fi

echo
echo "==> Configuring nginx"
sudo tee /etc/nginx/sites-available/tg >/dev/null <<EOF
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    listen 443 ssl default_server;
    listen [::]:443 ssl default_server;
    server_name _;

    ssl_certificate ${TLS_CERT};
    ssl_certificate_key ${TLS_KEY};
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_session_cache shared:TGSSL:10m;
    ssl_session_timeout 1d;

    client_max_body_size 6m;

    location /static/ {
        alias "${REPO_ROOT}/collected_static/";
        access_log off;
        expires 7d;
        add_header Cache-Control "public";
    }

    location /media/ {
        alias "${REPO_ROOT}/media/";
        access_log off;
    }

    location /ws/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header Origin \$http_origin;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
        proxy_send_timeout 86400;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header Origin \$http_origin;
        proxy_read_timeout 300;
    }
}
EOF

sudo rm -f /etc/nginx/sites-enabled/default
sudo ln -sfn /etc/nginx/sites-available/tg /etc/nginx/sites-enabled/tg
sudo nginx -t

echo
echo "==> Starting Tellurium Games"
sudo systemctl daemon-reload
sudo systemctl enable tg nginx
sudo systemctl restart tg
sudo systemctl restart nginx

sudo systemctl is-active --quiet tg || {
    sudo systemctl --no-pager --full status tg || true
    fail "tg.service did not start."
}
sudo systemctl is-active --quiet nginx || {
    sudo systemctl --no-pager --full status nginx || true
    fail "nginx did not start."
}

PRIMARY_HOST="$("${PYTHON}" - <<'PY'
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tg.settings")
from django.conf import settings

host = settings.ALLOWED_HOSTS[0]
if host == "*":
    host = "localhost"
elif host.startswith("."):
    host = host[1:]
print(host)
PY
)"

echo
echo "==> Smoke-testing nginx -> Daphne -> Django"
HTTP_STATUS=""
for _ in {1..30}; do
    HTTP_STATUS="$(curl \
        --insecure \
        --silent \
        --output /dev/null \
        --write-out '%{http_code}' \
        --header "Host: ${PRIMARY_HOST}" \
        https://127.0.0.1/ || true)"
    if [[ "${HTTP_STATUS}" =~ ^(2|3)[0-9][0-9]$ ]]; then
        break
    fi
    sleep 1
done

[[ "${HTTP_STATUS}" =~ ^(2|3)[0-9][0-9]$ ]] || {
    sudo journalctl -u tg -n 100 --no-pager || true
    sudo tail -n 100 /var/log/nginx/error.log || true
    fail "Site smoke test failed with HTTP status ${HTTP_STATUS:-no response}."
}

LAN_IP="$(hostname -I 2>/dev/null | awk '{print $1}')"

echo
echo "============================================================"
echo "Tellurium Games clean install completed successfully."
echo
echo "Django/Daphne:  tg.service (127.0.0.1:8000)"
echo "Reverse proxy:  nginx (ports 80 and 443)"
echo "Redis:          redis-server.service"
echo "Smoke test:     HTTPS returned ${HTTP_STATUS}"
echo
echo "Configured host: https://${PRIMARY_HOST}/"
if [[ -n "${LAN_IP}" ]]; then
    echo "VM address:      https://${LAN_IP}/"
fi
echo
echo "The installer uses a self-signed TLS certificate so the site is immediately"
echo "usable. Browsers will warn until you replace it with a trusted certificate"
echo "(for example, Let's Encrypt or a certificate supplied by your NAS/reverse proxy)."
echo
echo "Useful commands:"
echo "  sudo systemctl status tg nginx redis-server"
echo "  sudo journalctl -u tg -f"
echo "  sudo tail -f /var/log/nginx/error.log"
echo
echo "To create an admin account:"
echo "  cd ${REPO_ROOT} && ${PYTHON} manage.py createsuperuser"
echo "============================================================"
