import sqlite3

connection = sqlite3.connect("oren.db")

with open("schema.sql") as f:
    connection.executescript(f.read())

connection.execute(
    "INSERT INTO products (name, size, price, quantity) VALUES (?, ?, ?, ?)",
    ("Linen Shirt", "M", 25000, 10),
)
connection.execute(
    "INSERT INTO products (name, size, price, quantity) VALUES (?, ?, ?, ?)",
    ("Cotton Tee", "M", 15000, 15),
)

connection.commit()
connection.close()
print("Database created with sample products")