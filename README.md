# Proyecto Júpiter - Asistente personal

Aplicación móvil basada en IA generativa para construir una memoria personal digital del usuario a partir de fuentes autorizadas como uso de apps, calendario, ubicación, texto y audio.

## Estructura

- `mobile-app/`: aplicación móvil con Expo / React Native. Parte de la prueba técnica de `UsageStatsManager` y ubicación en Android.
- `backend/`: backend del proyecto en Python. Parte del cliente OAuth 2.0 para las APIs de Google.
- `docs/`: documentación técnica e investigación. Normas de código en [docs/CONVENCIONES.md](docs/CONVENCIONES.md).

## Verificación

```bash
npm ci --prefix mobile-app && python -m pip install -r backend/requirements-dev.txt
npm --prefix mobile-app run typecheck
python -m pytest backend -q
```

## Estado actual

Proyecto en fase inicial de investigación y definición del MVP.
