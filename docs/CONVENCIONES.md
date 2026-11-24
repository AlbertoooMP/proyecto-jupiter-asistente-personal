# Convenciones del Proyecto Júpiter

Normas para personas y agentes (incluida la fábrica) que cambian este repo. Versión inicial: se irá ampliando.

## Estructura
- `mobile-app/`: app Expo (SDK 56, React Native, TypeScript estricto). **Android primero**.
- `backend/`: Python. Hoy contiene el cliente OAuth de Google (solo librería estándar en runtime).
- `docs/`: investigación y documentación técnica.

## Estilo
- Identificadores de código en inglés (como el código existente); comentarios, docstrings y documentación en español.
- TypeScript con `strict`. Nada de `any` sin justificarlo.
- Python: tipado cuando aporte claridad; el runtime del backend no añade dependencias externas sin justificarlo en el PR.

## App móvil (Expo)
- Antes de usar una API de Expo, consulta la documentación de la versión exacta: https://docs.expo.dev/versions/v56.0.0/
- Permisos y configuración nativa se declaran en `app.json` (o en un config plugin), **nunca solo a mano en `android/`**: esa carpeta se puede regenerar con `npx expo prebuild`.
- Requiere development build (`npx expo run:android`); Expo Go no sirve para UsageStats ni ubicación en segundo plano.

## Privacidad (datos personales)
- Recoger solo lo necesario para la función que se implementa.
- No registrar en logs datos personales (ubicaciones, títulos de eventos, correos, nombres de apps de un usuario concreto).
- Nunca subir claves, tokens ni `.env`. Las credenciales se leen de variables de entorno.

## Tests y verificación
Todo cambio debe dejar pasando, desde la raíz del repo:
- `npm --prefix mobile-app run typecheck`
- `python -m pytest backend -q`

Cada funcionalidad nueva del backend lleva tests unitarios sin red (HTTP simulado, como en `backend/tests/conftest.py`).
El test de integración contra Google solo se ejecuta si existe `GOOGLE_REFRESH_TOKEN`.

## Prohibido
- Modificar `.github/workflows/` (lo gestiona la persona responsable).
- Añadir dependencias sin explicar por qué en el PR.
