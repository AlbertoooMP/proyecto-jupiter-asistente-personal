# -*- coding: utf-8 -*-
"""
Prueba rápida de la Places API (New) v1 usando tu refresh token.

Colócalo en la raíz de tu repo (junto al .env) y ejecuta:
    python places_test.py

El .env debe tener:
    GOOGLE_CLIENT_ID=...
    GOOGLE_CLIENT_SECRET=...
    GOOGLE_REFRESH_TOKEN=...
    GOOGLE_CLOUD_PROJECT=tu-project-id   # el ID del proyecto en Cloud Console

Solo usa la librería estandar (urllib). No hay dependencias.
"""

import json
import os
import urllib.request
import urllib.parse
import urllib.error


# ---------------------------------------------------------------------------
# 1) Leer el .env manualmente (sin dependencias)
# ---------------------------------------------------------------------------
def cargar_env(ruta=".env.example"):
    valores = {}
    if not os.path.exists(ruta):
        return valores
    with open(ruta, encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea or linea.startswith("#") or "=" not in linea:
                continue
            clave, _, valor = linea.partition("=")
            valores[clave.strip()] = valor.strip().strip('"').strip("'")
    return valores


env = cargar_env()
CLIENT_ID     = env.get("GOOGLE_CLIENT_ID")
CLIENT_SECRET = env.get("GOOGLE_CLIENT_SECRET")
REFRESH_TOKEN = env.get("GOOGLE_REFRESH_TOKEN")
PROJECT_ID    = env.get("GOOGLE_CLOUD_PROJECT")   # ID del proyecto (para X-Goog-User-Project)


# ---------------------------------------------------------------------------
# 2) Renovar el access token con el refresh token
# ---------------------------------------------------------------------------
def obtener_access_token():
    datos = urllib.parse.urlencode({
        "client_id":     CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type":    "refresh_token",
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://oauth2.googleapis.com/token",
        data=datos,
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode("utf-8"))["access_token"]


# ---------------------------------------------------------------------------
# 3) Llamar a la Places API (New) -> búsqueda de texto
# ---------------------------------------------------------------------------
def buscar_lugares(access_token, texto):
    cuerpo = json.dumps({"textQuery": texto}).encode("utf-8")

    headers = {
        "Content-Type":     "application/json",
        "Authorization":    "Bearer " + access_token,
        # La Places API (New) EXIGE indicar qué campos quieres de vuelta:
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress",
    }
    # Con OAuth (credenciales de usuario) hay que indicar el proyecto:
    if PROJECT_ID:
        headers["X-Goog-User-Project"] = PROJECT_ID

    req = urllib.request.Request(
        "https://places.googleapis.com/v1/places:searchText",
        data=cuerpo,
        method="POST",
        headers=headers,
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode("utf-8"))


# ---------------------------------------------------------------------------
# 4) Ejecutar y mostrar la respuesta
# ---------------------------------------------------------------------------
def main():
    faltan = [k for k, v in {
        "GOOGLE_CLIENT_ID": CLIENT_ID,
        "GOOGLE_CLIENT_SECRET": CLIENT_SECRET,
        "GOOGLE_REFRESH_TOKEN": REFRESH_TOKEN,
    }.items() if not v]
    if faltan:
        print("Faltan estas claves en tu .env:", ", ".join(faltan))
        return

    try:
        token = obtener_access_token()
        print("Access token obtenido correctamente.\n")

        response = buscar_lugares(token, "restaurantes en Madrid")
        print("=== Respuesta de la Places API (New) ===")
        print(json.dumps(response, indent=2, ensure_ascii=False))

    except urllib.error.HTTPError as e:
        # Muestra el cuerpo del error, que en estas APIs suele explicar el problema
        detalle = e.read().decode("utf-8")
        print(f"Error HTTP {e.code}:")
        print(detalle)
    except urllib.error.URLError as e:
        print("Error de red:", e.reason)


if __name__ == "__main__":
    main()