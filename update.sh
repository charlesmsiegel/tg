git pull
python manage.py makemigrations
python manage.py migrate
yes yes | python manage.py collectstatic
