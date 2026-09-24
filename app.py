import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from datetime import date

app = Flask(__name__)


def get_db():
    connection = sqlite3.connect("oren.db")
    connection.row_factory = sqlite3.Row
    return connection


@app.route("/")
def home():
    db = get_db()
    count = db.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    db.close()
    return f"ORÉN Order & Inventory Tracker is running. Products in database: {count}"


@app.route("/products")
def products():
    db = get_db()
    all_products = db.execute("SELECT * FROM products").fetchall()
    db.close()
    return render_template("products.html", products=all_products)


@app.route("/products/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form["name"]
        size = request.form["size"]
        price = request.form["price"]
        quantity = request.form["quantity"]

        db = get_db()
        db.execute(
            "INSERT INTO products (name, size, price, quantity) VALUES (?, ?, ?, ?)",
            (name, size, price, quantity),
        )
        db.commit()
        db.close()
        return redirect(url_for("products"))

    return render_template("add_product.html")


@app.route("/products/<int:product_id>/update_stock", methods=["GET", "POST"])
def update_stock(product_id):
    db = get_db()

    if request.method == "POST":
        new_quantity = request.form["quantity"]
        db.execute(
            "UPDATE products SET quantity = ? WHERE id = ?",
            (new_quantity, product_id),
        )
        db.commit()
        db.close()
        return redirect(url_for("products"))

    product = db.execute(
        "SELECT * FROM products WHERE id = ?", (product_id,)
    ).fetchone()
    db.close()
    return render_template("update_stock.html", product=product)


@app.route("/orders/add", methods=["GET", "POST"])
def add_order():
    db = get_db()

    if request.method == "POST":
        customer = request.form["customer"]
        product_id = request.form["product_id"]
        quantity = int(request.form["quantity"])
        payment_status = request.form["payment_status"]

        db.execute(
            "INSERT INTO orders (customer, order_date, payment_status, order_status) VALUES (?, ?, ?, ?)",
            (customer, str(date.today()), payment_status, "new"),
        )
        order_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]

        db.execute(
            "INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)",
            (order_id, product_id, quantity),
        )

        db.execute(
            "UPDATE products SET quantity = quantity - ? WHERE id = ?",
            (quantity, product_id),
        )

        db.commit()
        db.close()
        return redirect(url_for("products"))

    all_products = db.execute("SELECT * FROM products").fetchall()
    db.close()
    return render_template("add_order.html", products=all_products)

if __name__ == "__main__":
    app.run(debug=True)