# -*- coding: utf-8 -*-
"""Pasos 2 y 2b del flujo: gestión de tokens contra el token endpoint."""

from ..exceptions import HttpError, TokenError


class TokenService:
    """Encapsula las operaciones sobre el token endpoint de Google."""

    def __init__(self, config, http_client):
        self.config = config
        self.http = http_client

    def exchange_code(self, authorization_code):
        """Canjea el `code` por access_token y refresh_token."""
        payload = {
            "code": authorization_code,
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret,
            "redirect_uri": self.config.redirect_uri,
            "grant_type": "authorization_code",
        }
        return self._post_token(payload)

    def refresh(self, refresh_token):
        """Obtiene un access_token nuevo a partir del refresh_token."""
        payload = {
            "refresh_token": refresh_token,
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret,
            "grant_type": "refresh_token",
        }
        return self._post_token(payload)

    def revoke(self, token):
        """Revoca (invalida) un access o refresh token."""
        return self.http.request(
            self.config.revoke_endpoint,
            method="POST",
            data={"token": token},
        )

    def _post_token(self, payload):
        # El token endpoint EXIGE form-urlencoded (no JSON).
        try:
            resp = self.http.request(
                self.config.token_endpoint, method="POST", data=payload
            )
        except HttpError as e:
            # Traducimos el error HTTP a un error de dominio más claro.
            raise TokenError(f"Fallo del token endpoint: {e.body}") from e
        return resp.body
