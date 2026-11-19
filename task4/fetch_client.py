import time

import requests

TOKEN_URL = "http://127.0.0.1:9000/token"
CLIENT_ID = "my-client"
CLIENT_SECRET = "mock-secret"


def get_token():
    resp = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def fetch_all(url, page_size=3):
    token = "stale-token"
    results = []
    offset = 0
    retried = False

    while True:
        resp = requests.get(
            url,
            params={"offset": offset, "limit": page_size},
            headers={"Authorization": f"Bearer {token}"},
        )

        if resp.status_code == 401:
            if retried:
                raise RuntimeError("Still unauthorized after token refresh")
            print("401 received -> refreshing token")
            token = get_token()
            retried = True
            continue

        resp.raise_for_status()
        retried = False

        if resp.headers.get("X-RateLimit-Remaining") == "0":
            print("Rate limit reached -> sleeping 2 seconds")
            time.sleep(2)

        data = resp.json()
        results.extend(data["items"])
        if not data["items"] or len(results) >= data["total"]:
            break
        offset += page_size

    return results


if __name__ == "__main__":
    all_items = fetch_all("http://127.0.0.1:9000/items")
    print("Fetched", len(all_items), "items")