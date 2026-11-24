# -*- coding: utf-8 -*-
import unittest
from unittest.mock import Mock

from oauth_client.config import OAuthConfig
from oauth_client.http.client import HttpResponse
from oauth_client.oauth.tokens import TokenService
from oauth_client.exceptions import HttpError, TokenError


class TestTokenService(unittest.TestCase):
    def setUp(self):
        self.config = OAuthConfig(client_id="ID", client_secret="SECRET")
        self.http = Mock()  # doble de prueba del HttpClient
        self.service = TokenService(self.config, self.http)

    def test_exchange_code_devuelve_tokens(self):
        self.http.request.return_value = HttpResponse(
            200, {}, {"access_token": "AT", "refresh_token": "RT"}
        )
        result = self.service.exchange_code("CODE")
        self.assertEqual(result["access_token"], "AT")
        # Verifica que se llamó al token endpoint por POST
        _, kwargs = self.http.request.call_args
        self.assertEqual(kwargs["method"], "POST")
        self.assertEqual(kwargs["data"]["grant_type"], "authorization_code")

    def test_refresh_usa_grant_correcto(self):
        self.http.request.return_value = HttpResponse(200, {}, {"access_token": "NEW"})
        self.service.refresh("RT")
        _, kwargs = self.http.request.call_args
        self.assertEqual(kwargs["data"]["grant_type"], "refresh_token")

    def test_error_http_se_traduce_a_tokenerror(self):
        self.http.request.side_effect = HttpError(400, {"error": "invalid_grant"})
        with self.assertRaises(TokenError):
            self.service.exchange_code("BAD")


if __name__ == "__main__":
    unittest.main()
