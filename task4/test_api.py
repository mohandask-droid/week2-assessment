import hashlib
import hmac
import json

BODY = json.dumps({"order_id": 1, "status": "shipped"}).encode()


def sign(body):
    return hmac.new(b"test-secret", body, hashlib.sha256).hexdigest()


def make_customer(client, headers, n=1):
    return client.post(
        "/customers",
        json={"name": f"User{n}", "email": f"user{n}@mail.com", "city": "Chennai"},
        headers=headers,
    )


def test_create_customer_success(client, headers):
    resp = make_customer(client, headers)
    assert resp.status_code == 201
    assert resp.json()["email"] == "user1@mail.com"


def test_list_customers_pagination(client, headers):
    for n in range(1, 7):
        make_customer(client, headers, n)
    resp = client.get("/customers?page=1&per_page=5", headers=headers)
    assert resp.status_code == 200
    assert len(resp.json()["items"]) == 5
    assert resp.json()["total"] == 6


def test_missing_api_key_returns_401(client):
    assert client.get("/customers").status_code == 401


def test_wrong_api_key_returns_403(client):
    resp = client.get("/customers", headers={"X-API-Key": "wrong"})
    assert resp.status_code == 403


def test_customer_not_found_returns_404(client, headers):
    assert client.get("/customers/99999", headers=headers).status_code == 404


def test_duplicate_email_returns_409(client, headers):
    make_customer(client, headers)
    assert make_customer(client, headers).status_code == 409


def test_invalid_body_returns_422(client, headers):
    resp = client.post("/customers", json={"email": "a@mail.com"}, headers=headers)
    assert resp.status_code == 422


def test_webhook_valid_signature_returns_200(client):
    resp = client.post(
        "/webhooks/order-events",
        content=BODY,
        headers={"X-Signature": sign(BODY), "Content-Type": "application/json"},
    )
    assert resp.status_code == 200


def test_webhook_tampered_returns_401(client):
    resp = client.post(
        "/webhooks/order-events",
        content=BODY + b"x",
        headers={"X-Signature": sign(BODY), "Content-Type": "application/json"},
    )
    assert resp.status_code == 401