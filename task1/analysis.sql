-- Q0 setup
CREATE TABLE customers (id INT PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders (id INT PRIMARY KEY, customer_id INT REFERENCES customers(id), amount INT, ordered_at DATE);
CREATE TABLE products (id INT PRIMARY KEY, name TEXT, attrs JSONB);

INSERT INTO customers VALUES (1,'Arun','Chennai'),(2,'Priya','Mumbai'),(3,'Rahul','Chennai'),(4,'Divya','Bangalore');

INSERT INTO orders VALUES
(101,1,700,'2026-01-05'),(102,1,600,'2026-02-10'),(103,2,300,'2026-01-20'),
(104,2,400,'2026-02-15'),(105,3,1500,'2026-02-18'),(106,1,450,'2026-03-01'),
(107,3,200,'2026-03-05'),(108,2,250,'2026-03-10'),(109,3,800,'2026-03-20');

INSERT INTO products VALUES
(1,'Laptop A','{"brand":"Dell","ram":16}'),
(2,'Laptop B','{"brand":"HP","ram":8}');

-- Q1
SELECT c.name, SUM(o.amount) AS total
FROM customers c
JOIN orders o ON o.customer_id = c.id
GROUP BY c.name
HAVING SUM(o.amount) > 1000;

-- Q2
SELECT c.id, c.name
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
WHERE o.id IS NULL;

-- Q3
WITH customer_totals AS (
  SELECT c.name, c.city, SUM(o.amount) AS total
  FROM customers c
  JOIN orders o ON o.customer_id = c.id
  GROUP BY c.name, c.city
),
ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY city ORDER BY total DESC) AS rn
  FROM customer_totals
)
SELECT city, name, total FROM ranked WHERE rn = 1;

-- Q4
SELECT customer_id, id AS order_id, amount, ordered_at,
  ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY amount DESC) AS rank_no,
  LAG(amount) OVER (PARTITION BY customer_id ORDER BY ordered_at) AS prev_amount
FROM orders
ORDER BY customer_id, ordered_at;

-- Q5
SELECT id, name, attrs ->> 'ram' AS ram
FROM products
WHERE attrs @> '{"brand": "Dell"}';