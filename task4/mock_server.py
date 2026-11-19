from urllib.parse import parse_qs

from fastapi import FastAPI, Header, HTTPException, Request, Response

app = FastAPI()

ITEMS = [{"id": i, "name": f"item{i}"} for i in range(1, 8)]
VALID_TOKEN = "fresh-token"
calls = {"n": 0}


@app.post("/token")
async def token(request: Request):
    data = parse_qs((await request.body()).decode())
    if data.get("grant_type") != ["client_credentials"] or data.get("client_secret") != ["mock-secret"]:
        raise HTTPException(status_code=401, detail="invalid_client")
    return {"access_token": VALID_TOKEN, "token_type": "bearer", "expires_in": 3600}


@app.get("/items")
def items(
    response: Response,
    offset: int = 0,
    limit: int = 3,
    authorization: str = Header(default=None),
):
    if authorization != f"Bearer {VALID_TOKEN}":
        raise HTTPException(status_code=401, detail="token expired")
    calls["n"] += 1
    response.headers["X-RateLimit-Remaining"] = "0" if calls["n"] == 2 else "5"
    return {"items": ITEMS[offset:offset + limit], "total": len(ITEMS)}