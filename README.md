# 🛒 Ali's Mart Dashboard

Welcome to **Ali's Mart Dashboard**, a complete Desktop E-commerce Application built with Python and Tkinter. This application provides a full shopping experience with categories, products, cart functionality, and order management.

## ✨ Features

- **User Authentication:** Secure Login and Registration system.
- **Rich Product Catalog:** Browse 136 products across 8 main categories (Electronics, Vehicles, Furniture, Clothing, Property, Pets, Appliances, Sports).
- **Interactive Cart System:** Add products to cart, select quantities, and review before ordering.
- **Order Management:** Place orders, save customer details for future use, and view complete order history.
- **Stock Management:** Real-time stock updates upon order placement.
- **Beautiful UI:** A modern, dark-themed, and responsive interface built entirely with Python.
- **Offline Database:** Uses a local JSON database (`mart_users.json`) to store users, orders, and products.

## 🛠️ System Requirements

- **OS:** Windows, Mac, or Linux
- **Python:** 3.7 or higher
- **Libraries:** `tkinter` (built-in with Python) and `Pillow` (for images)

## 🚀 Quick Start Guide

### 1. Installation

Ensure you have Python installed. Open your terminal or command prompt and install the required image processing library:

```bash
pip install -r requirements.txt
# OR manually:
pip install Pillow
```

### 2. Running the Application

Navigate to the project folder and run the main script:

**Windows:**
```bash
python "Ali's_Mart_Dashboard.py"
```

**Mac/Linux:**
```bash
python3 "Ali's_Mart_Dashboard.py"
```

*(Note: If you are using an older version of the script named `bikroy_mart_fixed.py` as mentioned in some guides, use that filename instead).*

### 3. First Use

1. On the login screen, click **"Don't have an account? Register here"** to create a test account.
2. Login with your new credentials.
3. Browse products through categories, add items to your cart (🛒), and proceed to checkout.

## 📁 Project Structure

- `Ali's_Mart_Dashboard.py` - The main application script.
- `mart_users.json` - Local database file (auto-generated).
- `assets/` - Folder for product and UI images.
- `requirements.txt` - Project dependencies.
- Documentation: `QUICK_START.md`, `SETUP_GUIDE.md`, `USER_MANUAL.md`.

## ❓ Troubleshooting

- **`No module named 'tkinter'`**: Reinstall Python and ensure "tcl/tk" is checked during installation.
- **`No module named 'PIL'`**: Make sure to run `pip install Pillow`.
- **Reset Database**: Delete `mart_users.json` to wipe all accounts, orders, and reset the inventory.

---
Enjoy shopping at Ali's Mart! 🎉
