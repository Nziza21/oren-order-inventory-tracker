import sqlite3
from flask import Flask

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


if __name__ == "__main__":
    app.run(debug=True)