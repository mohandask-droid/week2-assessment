import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_orders(customer_id):
    conn = psycopg2.connect(
        host="localhost",
        dbname="perf_db",
        user="postgres",
        password=os.getenv("DB_PASSWORD"),
    )
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, customer_id, amount FROM big_orders WHERE customer_id = %s",
                (customer_id,),
            )
            return cur.fetchall()
    except psycopg2.Error:
        return []
    finally:
        conn.close()


if __name__ == "__main__":
    print("Normal input 500 ->", len(get_orders(500)), "rows")
    print("Injection input '1 OR 1=1' ->", len(get_orders("1 OR 1=1")), "rows")