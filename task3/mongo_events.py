import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client = MongoClient(
    os.getenv("MONGO_URI", "mongodb://localhost:27017"),
    serverSelectionTimeoutMS=5000,
)
events = client["retail_events_db"]["order_events"]

events.delete_many({})
events.insert_many([
    {"order_id": 101, "customer_id": 1, "amount": 700, "event": "order_placed"},
    {"order_id": 102, "customer_id": 1, "amount": 600, "event": "order_placed"},
    {"order_id": 103, "customer_id": 2, "amount": 300, "event": "order_placed"},
    {"order_id": 104, "customer_id": 2, "amount": 400, "event": "order_placed"},
    {"order_id": 105, "customer_id": 2, "amount": 250, "event": "order_placed"},
])
print("Events stored:", events.count_documents({}))

pipeline = [
    {"$group": {"_id": "$customer_id", "total": {"$sum": "$amount"}}},
    {"$sort": {"_id": 1}},
]
for row in events.aggregate(pipeline):
    print("Mongo totals: customer", row["_id"], "->", row["total"])