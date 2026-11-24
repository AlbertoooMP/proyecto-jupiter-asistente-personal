# -*- coding: utf-8 -*-
"""Configuración del cliente.

Se lee de variables de entorno para NO hardcodear secretos en el código.
Usa solo librería estándar (dataclasses + os).
"""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class OAuthConfig:
    """Configuración inmutable del flujo OAuth 2.0."""

    client_id: str
    client_secret: str
    redirect_uri: str = "https://developers.google.com/oauthplayground"
    scopes: str = "https://www.googleapis.com/auth/userinfo.profile"

    # Endpoints oficiales de Google
    auth_endpoint: str = "https://accounts.google.com/o/oauth2/v2/auth"
    token_endpoint: str = "https://oauth2.googleapis.com/token"
    revoke_endpoint: str = "https://oauth2.googleapis.com/revoke"

    @classmethod
    def from_env(cls):
        """Construye la config a partir de variables de entorno."""
        client_id = os.environ.get("GOOGLE_CLIENT_ID")
        client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
        if not client_id or not client_secret:
            raise ValueError(
                "Faltan GOOGLE_CLIENT_ID y/o GOOGLE_CLIENT_SECRET en el entorno."
            )
        return cls(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=os.environ.get(
                "GOOGLE_REDIRECT_URI",
                "https://developers.google.com/oauthplayground",
            ),
            scopes=os.environ.get(
                "GOOGLE_SCOPES",
                "https://www.googleapis.com/auth/userinfo.profile",
            ),
        )
