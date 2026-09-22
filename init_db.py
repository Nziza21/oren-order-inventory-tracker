import sqlite3

connection = sqlite3.connect("oren.db")

with open("schema.sql") as f:
    connection.executescript(f.read())

products = [
    ("The Threshold", "S", 70000, 6),
    ("The Threshold", "M", 70000, 6),
    ("The Threshold", "L", 70000, 6),
    ("Tailored Shirt", "S", 60000, 5),
    ("Tailored Shirt", "M", 60000, 5),
    ("Tailored Shirt", "L", 60000, 5),
    ("Suit Jacket", "S", 100000, 3),
    ("Suit Jacket", "M", 100000, 3),
    ("Suit Jacket", "L", 100000, 3),
    ("Tailored Trouser", "S", 50000, 5),
    ("Tailored Trouser", "M", 50000, 5),
    ("Tailored Trouser", "L", 50000, 5),
]

for name, size, price, quantity in products:
    connection.execute(
        "INSERT INTO products (name, size, price, quantity) VALUES (?, ?, ?, ?)",
        (name, size, price, quantity),
    )

connection.commit()
connection.close()
print("Database created with ORÉN products")