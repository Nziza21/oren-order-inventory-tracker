# ORÉN Order & Inventory Tracker

A web app for ORÉN RWANDA LTD to track stock, record customer orders, and follow payment and fulfillment status.

## Problem
ORÉN's orders and stock were tracked in chats and from memory, which caused missed orders and unclear stock.

## Tech stack
Python (Flask), SQLite, HTML/CSS, Flask-Login

## Features
- Admin login (password-protected, password stored outside the repo as an environment variable)
- Add products and update stock levels
- Low-stock flagging (highlights items below a set threshold)
- Record customer orders, including orders with multiple products
- Automatic stock reduction when an order is placed, with a check to prevent overselling
- Order status tracking (new, packed, delivered) and payment status (paid, unpaid)
- Search orders by customer name

## Status
Weeks 1-3 complete. Core product, stock, and order features are built and tested, including login and multi-item orders. Week 4 will focus on further testing with real ORÉN data and additional refinements.

## Setup
1. Clone the repo and create a virtual environment
2. `pip install -r requirements.txt` (or install flask, flask-login, python-dotenv, werkzeug individually)
3. Create a `.env` file with `ADMIN_PASSWORD=yourpassword`
4. Run `python3 init_db.py` once to set up the database
5. Run `python3 app.py` to start the app