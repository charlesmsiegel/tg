"""Forwarded addresses are accepted only through declared proxy networks."""

import re
from pathlib import Path

from django.conf import settings
from django.test import RequestFactory, SimpleTestCase, override_settings

from accounts import throttle


class ThrottleAddressTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def address(self, peer, header=""):
        return throttle.client_address(
            self.factory.post("/", REMOTE_ADDR=peer, HTTP_X_FORWARDED_FOR=header)
        )

    @override_settings(AUTH_THROTTLE_TRUSTED_PROXIES=[])
    def test_unconfigured_proxy_headers_are_ignored(self):
        self.assertEqual(self.address("198.51.100.5", "203.0.113.1"), "198.51.100.5")

    @override_settings(AUTH_THROTTLE_TRUSTED_PROXIES=["10.0.0.0/24"])
    def test_header_from_an_untrusted_peer_is_ignored(self):
        self.assertEqual(self.address("198.51.100.5", "203.0.113.1"), "198.51.100.5")

    @override_settings(AUTH_THROTTLE_TRUSTED_PROXIES=["10.0.0.0/24"])
    def test_walk_stops_at_first_untrusted_hop(self):
        self.assertEqual(self.address("10.0.0.2", "forged, 203.0.113.9, 10.0.0.1"), "203.0.113.9")

    @override_settings(AUTH_THROTTLE_TRUSTED_PROXIES=["2001:db8::/32"])
    def test_ipv6_proxies_and_addresses_are_normalized(self):
        self.assertEqual(
            self.address("2001:db8::2", "2001:4860:0:0::1, 2001:db8::1"), "2001:4860::1"
        )

    @override_settings(AUTH_THROTTLE_TRUSTED_PROXIES=["10.0.0.2"])
    def test_missing_or_invalid_header_falls_back_to_peer(self):
        for header in ("", "not an address", "203.0.113.9, "):
            with self.subTest(header=header):
                self.assertEqual(self.address("10.0.0.2", header), "10.0.0.2")


class InstallerProxyHeaderTests(SimpleTestCase):
    def test_nginx_replaces_untrusted_client_forwarded_headers_before_daphne(self):
        # Daphne --proxy-headers takes the first XFF entry. App-level proxy trust
        # cannot repair a forged REMOTE_ADDR if nginx appended an untrusted chain.
        script = (Path(settings.BASE_DIR) / "clean_install.sh").read_text(encoding="utf-8")
        directives = re.findall(r"proxy_set_header X-Forwarded-For ([^;]+);", script)
        self.assertTrue(directives)
        for directive in directives:
            with self.subTest(directive=directive):
                self.assertEqual(directive, "\\$remote_addr")
