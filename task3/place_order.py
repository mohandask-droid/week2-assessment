from sqlalchemy import select

from database import SessionLocal
from models import Order, Product


def place_order(customer_id, product_id, qty, fail_after_update=False):
    with SessionLocal() as session:
        with session.begin():
            product = session.execute(
                select(Product).where(Product.id == product_id).with_for_update()
            ).scalar_one()
            if product.stock < qty:
                raise ValueError("Insufficient stock")
            product.stock -= qty
            session.flush()
            if fail_after_update:
                raise RuntimeError("Forced failure after stock update")
            session.add(Order(customer_id=customer_id, product_id=product_id, qty=qty))


def get_stock(product_id):
    with SessionLocal() as session:
        return session.get(Product, product_id).stock


if __name__ == "__main__":
    try:
        place_order(1, 1, 2, fail_after_update=True)
    except RuntimeError:
        print("Forced failure: rolled back, stock still", get_stock(1))

    before = get_stock(1)
    place_order(1, 1, 2)
    print("Order placed: stock", before, "->", get_stock(1))

    try:
        place_order(1, 1, 999)
    except ValueError:
        print("Insufficient stock: rolled back, stock still", get_stock(1))