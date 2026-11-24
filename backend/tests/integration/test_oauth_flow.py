# -*- coding: utf-8 -*-
"""Test de integración contra los servidores REALES de Google.

Solo se ejecuta si están definidas las variables de entorno con credenciales
y un refresh_token válido. Si no, se salta automáticamente.

    GOOGLE_CLIENT_ID
    GOOGLE_CLIENT_SECRET
    GOOGLE_REFRESH_TOKEN   (obtenido una vez desde el Playground)
"""

import os
import unittest

from oauth_client import OAuthConfig, HttpClient, TokenService, ApiClient


@unittest.skipUnless(
    os.environ.get("GOOGLE_REFRESH_TOKEN"),
    "Requiere GOOGLE_REFRESH_TOKEN para correr contra Google real.",
)
class TestOAuthFlowReal(unittest.TestCase):
    def setUp(self):
        self.config = OAuthConfig.from_env()
        self.http = HttpClient()
        self.tokens = TokenService(self.config, self.http)
        self.api = ApiClient(self.http)

    def test_refresh_y_llamada_a_userinfo(self):
        data = self.tokens.refresh(os.environ["GOOGLE_REFRESH_TOKEN"])
        self.assertIn("access_token", data)

        info = self.api.call(
            data["access_token"],
            "https://www.googleapis.com/oauth2/v3/userinfo",
            method="GET",
        )
        self.assertIn("sub", info)  # id del usuario


if __name__ == "__main__":
    unittest.main()
