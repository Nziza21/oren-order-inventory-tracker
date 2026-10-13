# ORÉN Order & Inventory Tracker

A web app for ORÉN RWANDA LTD to track stock, record customer orders, and follow payment and fulfillment status.

## Problem
ORÉN's orders and stock were tracked in chats and from memory, which caused missed orders and unclear stock.

## Tech stack
Python (Flask), SQLite, HTML/CSS, Flask-Login

## Features
- Admin login (password-protected, stored outside the repo as an environment variable)
- Add products and update stock levels
- Low-stock flagging
- Record customer orders, including multi-item orders
- Automatic stock reduction, with checks against overselling and zero-quantity orders
- Order status (new, packed, delivered) and payment status (paid, unpaid)
- Order detail page with items, price, and subtotal
- Sales summary showing total revenue and units sold per product
- Search orders by customer name
- Shared navigation across all pages

## Status
Weeks 1-5 in progress. Core product, order, and reporting features built and tested with real ORÉN data.

## Setup
1. Clone the repo and create a virtual environment
2. `pip install -r requirements.txt`
3. Create a `.env` file with `ADMIN_PASSWORD=yourpassword`
4. Run `python3 init_db.py` once
5. Run `python3 app.py`