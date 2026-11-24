# -*- coding: utf-8 -*-
import unittest
from unittest.mock import patch

from oauth_client.http.client import HttpClient
from oauth_client.exceptions import HttpError, NetworkError

from tests.conftest import FakeUrlopenResponse, fake_http_error


class TestHttpClient(unittest.TestCase):
    def setUp(self):
        self.client = HttpClient()

    @patch("oauth_client.http.client.urllib.request.urlopen")
    def test_get_ok_parsea_json(self, mock_open):
        mock_open.return_value = FakeUrlopenResponse(
            status=200, body='{"access_token": "abc"}'
        )
        resp = self.client.request("https://x", method="GET")
        self.assertEqual(resp.status, 200)
        self.assertEqual(resp.body["access_token"], "abc")

    @patch("oauth_client.http.client.urllib.request.urlopen")
    def test_post_form_urlencoded(self, mock_open):
        mock_open.return_value = FakeUrlopenResponse(body='{"ok": true}')
        self.client.request("https://x", method="POST", data={"a": "b"})
        # Verificamos que el body se codificó como formulario
        sent_request = mock_open.call_args[0][0]
        self.assertEqual(sent_request.data, b"a=b")

    @patch("oauth_client.http.client.urllib.request.urlopen")
    def test_http_error_lanza_excepcion(self, mock_open):
        mock_open.side_effect = fake_http_error(400, '{"error": "invalid_grant"}')
        with self.assertRaises(HttpError) as ctx:
            self.client.request("https://x", method="POST", data={})
        self.assertEqual(ctx.exception.status, 400)
        self.assertEqual(ctx.exception.body["error"], "invalid_grant")

    @patch("oauth_client.http.client.urllib.request.urlopen")
    def test_network_error(self, mock_open):
        import urllib.error
        mock_open.side_effect = urllib.error.URLError("sin red")
        with self.assertRaises(NetworkError):
            self.client.request("https://x")


if __name__ == "__main__":
    unittest.main()
