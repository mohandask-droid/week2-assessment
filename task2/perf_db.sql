-- T2 Part A: create big table
CREATE TABLE big_orders (
  id SERIAL PRIMARY KEY,
  customer_id INT,
  amount INT,
  ordered_at DATE
);

INSERT INTO big_orders (customer_id, amount, ordered_at)
SELECT (random()*10000)::int + 1,
       (random()*1000)::int,
       DATE '2026-01-01' + (random()*300)::int
FROM generate_series(1,200000);

SELECT COUNT(*) FROM big_orders;

-- T2 before index
EXPLAIN ANALYZE SELECT * FROM big_orders WHERE customer_id = 500;


-- T2 create index
CREATE INDEX idx_big_orders_customer ON big_orders(customer_id);
ANALYZE big_orders;

-- T2 after index
EXPLAIN ANALYZE SELECT * FROM big_orders WHERE customer_id = 500;

-- T2 Part C: tables
CREATE TABLE cust_check (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE
);

CREATE TABLE order_check (
  id SERIAL PRIMARY KEY,
  customer_id INT REFERENCES cust_check(id),
  amount INT CHECK (amount > 0)
);

-- T2 valid row
INSERT INTO cust_check (name, email) VALUES ('Arun', 'arun@mail.com');

-- T2 error 1: NOT NULL
INSERT INTO cust_check (name, email) VALUES (NULL, 'a@mail.com');

-- T2 error 2: UNIQUE
INSERT INTO cust_check (name, email) VALUES ('Arun2', 'arun@mail.com');

-- T2 error 3: FOREIGN KEY
INSERT INTO order_check (customer_id, amount) VALUES (999, 100);

-- T2 error 4: CHECK
INSERT INTO order_check (customer_id, amount) VALUES (1, -50);
