# -*- coding: utf-8 -*-
"""Paso 1 del flujo: construir la URL de autorización."""

import urllib.parse


def build_authorization_url(config, state=None):
    """Devuelve la URL a la que el usuario debe entrar para dar consentimiento.

    `state` es opcional pero recomendado (protección CSRF).
    """
    params = {
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "response_type": "code",
        "scope": config.scopes,
        "access_type": "offline",
        "prompt": "consent",
    }
    if state:
        params["state"] = state
    return config.auth_endpoint + "?" + urllib.parse.urlencode(params)
