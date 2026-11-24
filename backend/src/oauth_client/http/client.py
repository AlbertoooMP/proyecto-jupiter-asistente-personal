# -*- coding: utf-8 -*-
"""Capa de transporte HTTP.

Envuelve urllib en una clase testeable. Al ser una clase con un único punto
de entrada (`request`), en los tests basta con mockear `urllib.request.urlopen`.
"""

import json
import urllib.request
import urllib.parse
import urllib.error

from ..exceptions import HttpError, NetworkError


class HttpResponse:
    """Respuesta normalizada, independiente de urllib."""

    def __init__(self, status, headers, body):
        self.status = status
        self.headers = headers
        self.body = body

    def __repr__(self):
        return f"<HttpResponse status={self.status} body={self.body!r}>"


class HttpClient:
    """Cliente HTTP mínimo construido sobre la librería estándar."""

    def __init__(self, timeout=30):
        self.timeout = timeout

    def request(self, url, method="GET", data=None, headers=None):
        """Envía una petición y devuelve un HttpResponse.

        - data dict + Content-Type JSON  -> cuerpo JSON
        - data dict (por defecto)        -> form-urlencoded
        Lanza HttpError en 4xx/5xx y NetworkError si no hay respuesta.
        """
        headers = dict(headers or {})
        body_bytes = self._encode_body(data, headers)

        req = urllib.request.Request(
            url=url, data=body_bytes, headers=headers, method=method
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                raw = resp.read().decode("utf-8")
                return HttpResponse(resp.status, dict(resp.headers),
                                    self._parse(raw))
        except urllib.error.HTTPError as e:
            raw = e.read().decode("utf-8")
            raise HttpError(e.code, self._parse(raw), dict(e.headers))
        except urllib.error.URLError as e:
            raise NetworkError(str(e.reason))

    @staticmethod
    def _encode_body(data, headers):
        if data is None:
            return None
        content_type = headers.get("Content-Type", "application/x-www-form-urlencoded")
        if "application/json" in content_type:
            headers.setdefault("Content-Type", "application/json")
            return json.dumps(data).encode("utf-8")
        headers.setdefault("Content-Type", "application/x-www-form-urlencoded")
        return urllib.parse.urlencode(data).encode("utf-8")

    @staticmethod
    def _parse(text):
        try:
            return json.loads(text)
        except (json.JSONDecodeError, ValueError):
            return text
