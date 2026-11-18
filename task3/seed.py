from database import SessionLocal
from models import Customer, Product

with SessionLocal() as session:
    session.merge(Customer(id=1, name="Arun", city="Chennai", phone="9999999999"))
    session.merge(Product(id=1, name="Laptop A", stock=10))
    session.commit()
print("Seeded: stock = 10")