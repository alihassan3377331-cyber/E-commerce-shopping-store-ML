# 🛒 Ali's Mart - Installation & Setup Guide

## What's Fixed ✅

1. **Products Distributed Across All Sub-Subcategories** - Every single sub-subcategory now has 2-4 products
2. **Complete Product Data** - 136 products added across all categories
3. **Working Cart System** - Add products to cart with quantity selection
4. **Order Placement** - Place orders with customer information
5. **Customer Info Persistence** - Customer details are saved and reused for next orders
6. **Stock Management** - Stock updates after order placement
7. **Order History** - View all placed orders with details
8. **Beautiful UI** - Colorful, modern interface with proper navigation

## Requirements

- Python 3.7 or higher
- tkinter (comes with Python by default)
- Pillow (PIL) for image handling

## Installation Steps

### Step 1: Install Python
Download and install Python 3.9+ from https://www.python.org/downloads/

**Important:** Check "Add Python to PATH" during installation

### Step 2: Open Terminal/Command Prompt

**Windows:** Press `Win + R`, type `cmd`, press Enter
**Mac:** Cmd + Space, type `Terminal`, press Enter
**Linux:** Open any terminal

### Step 3: Install Required Package

Run this command:
```bash
pip install Pillow
```

Or if that doesn't work:
```bash
pip install --upgrade pillow
```

### Step 4: Prepare Files

1. Create a new folder called `AlisMart`
2. Copy `bikroy_mart_fixed.py` into this folder
3. Create an `assets` folder inside `AlisMart` folder

Your folder structure should look like:
```
AlisMart/
├── bikroy_mart_fixed.py
└── assets/
```

### Step 5: Run the Application

Navigate to the AlisMart folder and run:

**Windows:**
```bash
python bikroy_mart_fixed.py
```

**Mac/Linux:**
```bash
python3 bikroy_mart_fixed.py
```

## How to Use

### 1. First Time Login
- Click "Don't have an account? Register here"
- Enter username and password
- Click "REGISTER NOW"

### 2. Login
- Enter your username and password
- Click "LOGIN"

### 3. Browse Products
- Click on any category (Electronics, Vehicles, etc.)
- Select a subcategory
- Select a specific type (sub-subcategory)
- Browse and view all products available

### 4. Add to Cart
- Click "🛒 Add to Cart" on any product
- Select quantity using + and - buttons
- Click "✅ Add to Cart"
- Choose to place order now or continue shopping

### 5. Place Order
- Fill in your mobile number, address, and payment method
- Check "Save this info" to remember for next time
- Review order and confirm
- Order is placed! 🎉

### 6. View Orders
- Click "📦 Orders" button in navbar
- See all your past orders
- Click "Details" to view order items and customer info

## Database

The app saves all data in `mart_users.json` file:
- User accounts
- Orders and order history
- Customer information
- Product inventory

This file is created automatically when you first use the app.

## Features

✅ User authentication (login/register)
✅ Browse categories with 3-level hierarchy
✅ 136 products across 8 categories
✅ Search and filter by category
✅ Shopping cart functionality
✅ Order placement with customer details
✅ Customer information persistence
✅ Stock management and updates
✅ Order history tracking
✅ Beautiful dark theme UI
✅ Responsive design

## Troubleshooting

### Error: "No module named 'tkinter'"
- tkinter usually comes with Python
- Try: `python -m tkinter` to test
- If not installed, reinstall Python and check the "tcl/tk" option

### Error: "No module named 'PIL'"
- Run: `pip install Pillow`

### Images not showing
- The app automatically creates placeholder images
- You can add your own PNG/JPG images to the assets folder

### Database Issues
- Delete `mart_users.json` to reset everything
- Be careful - this removes all accounts and orders

## Keyboard Shortcuts

- Mouse wheel to scroll products and categories
- Tab to move between fields in forms
- Enter to submit login/register forms

## Product Categories

1. **Electronics** - Phones, Computers, Gaming
2. **Vehicles** - Bikes, Cars
3. **Furniture** - Seating, Beds
4. **Clothing** - Men's, Women's clothing
5. **Property** - Houses, Shops, Offices
6. **Pets** - Dogs, Cats, Birds, Fish, Rabbits
7. **Appliances** - Cooling, Kitchen appliances
8. **Sports** - Cricket, Fitness equipment

## Notes

- All prices are in Pakistani Rupees (Rs.)
- Images are automatically generated as placeholders
- Customer info is saved securely with your account
- Each product has stock management
- Orders are permanent once placed

## Contact & Support

If you have any issues, make sure:
1. Python is installed correctly
2. Pillow package is installed
3. All files are in the correct folder
4. No special characters in folder path

Enjoy using Ali's Mart! 🎉
