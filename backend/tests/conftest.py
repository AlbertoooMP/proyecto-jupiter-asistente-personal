# -*- coding: utf-8 -*-
"""Utilidades compartidas para los tests.

Se pueden importar tanto desde unittest como desde pytest.
"""

import io


class FakeUrlopenResponse:
    """Simula el context manager que devuelve urllib.request.urlopen."""

    def __init__(self, status=200, body="{}", headers=None):
        self.status = status
        self._body = body.encode("utf-8")
        self.headers = headers or {"Content-Type": "application/json"}

    def read(self):
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def fake_http_error(code, body, headers=None):
    """Crea un urllib.error.HTTPError realista para los tests de error."""
    import urllib.error

    return urllib.error.HTTPError(
        url="https://oauth2.googleapis.com/token",
        code=code,
        msg="error",
        hdrs=headers or {},
        fp=io.BytesIO(body.encode("utf-8")),
    )
