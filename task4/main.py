import hashlib
import hmac
import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException, Query, Request
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import CustomerRow

load_dotenv()

API_KEY = os.getenv("API_KEY", "")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")

Base.metadata.create_all(engine)

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def verify_api_key(key: Optional[str] = Depends(api_key_header)):
    if key is None:
        raise HTTPException(status_code=401, detail="Missing API key")
    if not hmac.compare_digest(key, API_KEY):
        raise HTTPException(status_code=403, detail="Invalid API key")


class CustomerIn(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=3, max_length=100)
    city: Optional[str] = None


def to_dict(c: CustomerRow):
    return {"id": c.id, "name": c.name, "email": c.email, "city": c.city}


app = FastAPI(title="Customer API")
router = APIRouter(dependencies=[Depends(verify_api_key)])


@router.post("/customers", status_code=201)
def create_customer(data: CustomerIn, db: Session = Depends(get_db)):
    customer = CustomerRow(**data.model_dump())
    db.add(customer)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already exists")
    db.refresh(customer)
    return to_dict(customer)


@router.get("/customers")
def list_customers(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    total = db.scalar(select(func.count()).select_from(CustomerRow))
    rows = db.scalars(
        select(CustomerRow)
        .order_by(CustomerRow.id)
        .offset((page - 1) * per_page)
        .limit(per_page)
    ).all()
    return {
        "page": page,
        "per_page": per_page,
        "total": total,
        "items": [to_dict(r) for r in rows],
    }


@router.get("/customers/{customer_id}")
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.get(CustomerRow, customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return to_dict(customer)


@router.put("/customers/{customer_id}")
def update_customer(customer_id: int, data: CustomerIn, db: Session = Depends(get_db)):
    customer = db.get(CustomerRow, customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    customer.name = data.name
    customer.email = data.email
    customer.city = data.city
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already exists")
    return to_dict(customer)


@router.delete("/customers/{customer_id}", status_code=204)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.get(CustomerRow, customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(customer)
    db.commit()


app.include_router(router)


@app.post("/webhooks/order-events")
async def order_events(request: Request, x_signature: Optional[str] = Header(default=None)):
    body = await request.body()
    expected = hmac.new(WEBHOOK_SECRET.encode(), body, hashlib.sha256).hexdigest()
    if x_signature is None or not hmac.compare_digest(x_signature, expected):
        raise HTTPException(status_code=401, detail="Invalid signature")
    return {"status": "received"}