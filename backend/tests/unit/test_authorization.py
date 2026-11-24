# -*- coding: utf-8 -*-
import unittest
import urllib.parse

from oauth_client.config import OAuthConfig
from oauth_client.oauth.authorization import build_authorization_url


class TestAuthorizationUrl(unittest.TestCase):
    def setUp(self):
        self.config = OAuthConfig(client_id="ID", client_secret="SECRET")

    def test_contiene_parametros_obligatorios(self):
        url = build_authorization_url(self.config)
        query = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
        self.assertEqual(query["client_id"], ["ID"])
        self.assertEqual(query["response_type"], ["code"])
        self.assertEqual(query["access_type"], ["offline"])

    def test_incluye_state_si_se_pasa(self):
        url = build_authorization_url(self.config, state="xyz123")
        self.assertIn("state=xyz123", url)


if __name__ == "__main__":
    unittest.main()
