import json

from oauth_client import OAuthConfig, HttpClient, TokenService, ApiClient
from oauth_client.oauth.authorization import build_authorization_url


def main():
    config = OAuthConfig.from_env()
    http = HttpClient()
    tokens = TokenService(config, http)
    api = ApiClient(http)

    # PASO 1: URL de autorización
    response = build_authorization_url(config, state="csrf-token-demo")
    print("=== PASO 1: URL de autorización ===")
    print(response)

    # PASO 2: canjear el code (pégalo tras autorizar en el navegador)
    authorization_code = input("\nPega el authorization code: ").strip()
    response = tokens.exchange_code(authorization_code)
    print("=== PASO 2: Tokens ===")
    print(json.dumps(response, indent=2, ensure_ascii=False))

    access_token = response.get("access_token")

    # PASO 3: llamar a una API protegida
    if access_token:
        response = api.call(
            access_token,
            "https://www.googleapis.com/oauth2/v3/userinfo",
            method="GET",
        )
        print("=== PASO 3: userinfo ===")
        print(json.dumps(response, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
