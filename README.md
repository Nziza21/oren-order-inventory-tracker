# ORÉN Order & Inventory Tracker

A web app for ORÉN RWANDA LTD to track stock, record customer orders, and follow payment and fulfillment status.

## Problem
ORÉN's orders and stock were tracked in WhatsApp chats and from memory, which caused missed orders, overselling, and payments that couldn't be matched to an order.

## Tech stack
Python (Flask), SQLite, HTML/CSS, Flask-Login

## Features
- Admin login (password stored outside the repo in a `.env` file)
- Products: add, edit, update stock, and delete (deleting is blocked if the product is in an existing order)
- Low-stock flagging for items under 5 units
- Multi-item orders with automatic stock reduction
- Checks that block overselling, zero or negative quantities, and the same product repeated across rows
- Order status (new, packed, delivered) and payment status (paid, unpaid)
- Order detail page with items, prices, and subtotal
- Order cancellation that returns stock (blocked for delivered orders)
- Search orders by customer name, and a customer order history page
- Sales summary showing revenue from paid orders only, and units sold per product
- Stock history log recording every stock change with its date and reason

## Status
Core features are built and tested locally with real ORÉN products and orders. Not deployed yet.

## Screenshots

**Products, with low-stock flags**

![Products page](screenshots/products.png)

**Order detail**

![Order detail page](screenshots/order-detail.png)

**Sales summary (paid orders only)**

![Sales summary page](screenshots/sales-summary.png)

## Testing
Testing was done by hand against real data, and it found and fixed these bugs:
- Orders could sell more than was in stock
- An order could be saved with zero items
- Deleting a product silently erased the contents of orders that included it
- The same product repeated in one order bypassed the stock check
- The sales summary counted unpaid orders as revenue

## Known limitations and next steps
- No live MoMo integration: the admin marks orders as paid by hand
- CSRF protection is not added yet
- Feedback from real use at ORÉN is still to come

## Documentation
A step-by-step guide is in [USER_GUIDE.md](USER_GUIDE.md).

## Setup
1. Clone the repo and create a virtual environment
2. `pip install flask flask-login python-dotenv werkzeug`
3. Create a `.env` file with `ADMIN_PASSWORD=yourpassword`
4. Run `python3 init_db.py` once to create the database
5. Run `python3 app.py`