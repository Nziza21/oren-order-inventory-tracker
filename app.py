import os
import sqlite3
from datetime import date
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(__name__)
app.secret_key = "change-this-to-something-random"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

ADMIN_PASSWORD_HASH = generate_password_hash(os.environ.get("ADMIN_PASSWORD", "changeme"))


class Admin(UserMixin):
    id = "admin"


@login_manager.user_loader
def load_user(user_id):
    if user_id == "admin":
        return Admin()
    return None


def get_db():
    connection = sqlite3.connect("oren.db")
    connection.row_factory = sqlite3.Row
    return connection


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form["password"]
        if check_password_hash(ADMIN_PASSWORD_HASH, password):
            login_user(Admin())
            return redirect(url_for("products"))
        return "Wrong password. Go back and try again."
    return render_template("login.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/")
def home():
    db = get_db()
    count = db.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    db.close()
    return f"ORÉN Order & Inventory Tracker is running. Products in database: {count}"


@app.route("/products")
@login_required
def products():
    db = get_db()
    all_products = db.execute("SELECT * FROM products").fetchall()
    db.close()
    return render_template("products.html", products=all_products)


@app.route("/products/add", methods=["GET", "POST"])
@login_required
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
@login_required
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
@login_required
def add_order():
    db = get_db()

    if request.method == "POST":
        customer = request.form["customer"]
        payment_status = request.form["payment_status"]
        product_ids = request.form.getlist("product_id")
        quantities = request.form.getlist("quantity")

        totals = {}
        for product_id, quantity in zip(product_ids, quantities):
            quantity = int(quantity)
            totals[product_id] = totals.get(product_id, 0) + quantity

        for product_id, total_quantity in totals.items():
            product = db.execute(
                "SELECT * FROM products WHERE id = ?", (product_id,)
            ).fetchone()
            if total_quantity > product["quantity"]:
                db.close()
                return f"Not enough stock. Only {product['quantity']} left of {product['name']} ({product['size']})."

        db.execute(
            "INSERT INTO orders (customer, order_date, payment_status, order_status) VALUES (?, ?, ?, ?)",
            (customer, str(date.today()), payment_status, "new"),
        )
        order_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]

        for product_id, total_quantity in totals.items():
            db.execute(
                "INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)",
                (order_id, product_id, total_quantity),
            )
            db.execute(
                "UPDATE products SET quantity = quantity - ? WHERE id = ?",
                (total_quantity, product_id),
            )

        db.commit()
        db.close()
        return redirect(url_for("products"))

    all_products = db.execute("SELECT * FROM products").fetchall()
    db.close()
    return render_template("add_order.html", products=all_products)


@app.route("/orders")
@login_required
def orders():
    db = get_db()
    all_orders = db.execute("SELECT * FROM orders").fetchall()
    db.close()
    return render_template("orders.html", orders=all_orders)


@app.route("/orders/search")
@login_required
def search_orders():
    query = request.args.get("q", "")
    db = get_db()
    results = db.execute(
        "SELECT * FROM orders WHERE customer LIKE ?", (f"%{query}%",)
    ).fetchall()
    db.close()
    return render_template("orders.html", orders=results, search_query=query)


@app.route("/orders/<int:order_id>/update", methods=["GET", "POST"])
@login_required
def update_order(order_id):
    db = get_db()

    if request.method == "POST":
        db.execute(
            "UPDATE orders SET payment_status = ?, order_status = ? WHERE id = ?",
            (request.form["payment_status"], request.form["order_status"], order_id),
        )
        db.commit()
        db.close()
        return redirect(url_for("orders"))

    order = db.execute(
        "SELECT * FROM orders WHERE id = ?", (order_id,)
    ).fetchone()
    db.close()
    return render_template("update_order.html", order=order)


@app.route("/orders/<int:order_id>")
@login_required
def order_detail(order_id):
    db = get_db()
    order = db.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    items = db.execute("""
        SELECT products.name, products.size, products.price, order_items.quantity
        FROM order_items
        JOIN products ON order_items.product_id = products.id
        WHERE order_items.order_id = ?
    """, (order_id,)).fetchall()
    db.close()
    return render_template("order_detail.html", order=order, items=items)


@app.route("/sales-summary")
@login_required
def sales_summary():
    db = get_db()

    total_revenue = db.execute("""
        SELECT SUM(products.price * order_items.quantity) AS total
        FROM order_items
        JOIN products ON order_items.product_id = products.id
    """).fetchone()["total"] or 0

    by_product = db.execute("""
        SELECT products.name, products.size, SUM(order_items.quantity) AS total_sold,
               SUM(products.price * order_items.quantity) AS revenue
        FROM order_items
        JOIN products ON order_items.product_id = products.id
        GROUP BY products.id
        ORDER BY total_sold DESC
    """).fetchall()

    db.close()
    return render_template("sales_summary.html", total_revenue=total_revenue, by_product=by_product)

if __name__ == "__main__":
    app.run(debug=True)