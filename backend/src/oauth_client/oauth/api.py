# -*- coding: utf-8 -*-
"""Paso 3 del flujo: llamar a una API protegida con el access token."""


class ApiClient:
    """Realiza peticiones autenticadas inyectando el header Authorization."""

    def __init__(self, http_client):
        self.http = http_client

    def call(self, access_token, url, method="GET", body=None,
             content_type="application/json"):
        headers = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": content_type,
        }
        resp = self.http.request(url, method=method, data=body, headers=headers)
        return resp.body
