"""Run the service in-process and check the probes the manifests call."""

from app import app


def main():
    client = app.test_client()
    for path in ("/", "/health", "/ready", "/weather", "/info"):
        response = client.get(path)
        if response.status_code != 200:
            raise SystemExit(f"{path} returned {response.status_code}")
        if not response.is_json:
            raise SystemExit(f"{path} was not JSON")
    body = client.get("/health").get_json()
    if body.get("status") != "healthy":
        raise SystemExit(body)
    print("kubernetes app smoke ok")


if __name__ == "__main__":
    main()
