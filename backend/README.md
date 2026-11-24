# OAuth Playground Client (Python nativo)

Cliente OAuth 2.0 para los endpoints de Google que usa el
[OAuth 2.0 Playground](https://developers.google.com/oauthplayground/).
El código de **runtime no tiene dependencias externas** (solo librería estándar).

## Estructura

```
oauth_playground/
├── src/
│   └── oauth_client/
│       ├── __init__.py          # API pública del paquete
│       ├── config.py            # Configuración (variables de entorno)
│       ├── exceptions.py        # Errores de dominio
│       ├── http/
│       │   └── client.py        # Capa de transporte (urllib)
│       └── oauth/
│           ├── authorization.py # Paso 1: URL de consentimiento
│           ├── tokens.py        # Pasos 2/2b: exchange, refresh, revoke
│           └── api.py           # Paso 3: llamadas autenticadas
├── tests/
│   ├── conftest.py              # Fakes de urllib
│   ├── unit/                    # Tests aislados (HTTP mockeado)
│   └── integration/             # Test contra Google real (opcional)
├── examples/run_flow.py         # Demo del flujo completo
├── pyproject.toml
├── .env.example
└── requirements-dev.txt
```

## Configuración

```bash
cp .env.example .env
# edita .env con tu CLIENT_ID y CLIENT_SECRET de Google Cloud Console
export $(grep -v '^#' .env | xargs)   # carga las variables (Linux/Mac)
```

## Ejecutar el ejemplo

```bash
PYTHONPATH=src python examples/run_flow.py
```

## Testing

Los tests unitarios corren **sin dependencias** con unittest:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

O con pytest (opcional, más cómodo):

```bash
pip install -r requirements-dev.txt
pytest
```

Cobertura:

```bash
coverage run -m pytest && coverage report -m
```

El test de integración (`tests/integration`) solo se ejecuta si defines
`GOOGLE_REFRESH_TOKEN`; en caso contrario se salta automáticamente.
```
