# -*- coding: utf-8 -*-
"""Excepciones propias del cliente OAuth.

Tener excepciones de dominio permite que las capas superiores (servicios,
CLI, API web) capturen errores concretos sin depender de urllib.
"""


class OAuthClientError(Exception):
    """Excepción base del paquete."""


class HttpError(OAuthClientError):
    """Error HTTP (4xx / 5xx) devuelto por un endpoint."""

    def __init__(self, status, body, headers=None):
        self.status = status
        self.body = body
        self.headers = headers or {}
        super().__init__(f"HTTP {status}: {body}")


class NetworkError(OAuthClientError):
    """Fallo de red / DNS / conexión (sin respuesta del servidor)."""


class TokenError(OAuthClientError):
    """El token endpoint devolvió un error (invalid_grant, etc.)."""
