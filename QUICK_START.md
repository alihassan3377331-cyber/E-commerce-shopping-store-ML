# 🚀 Ali's Mart - Quick Start (5 Minutes)

## All-in-One Setup Commands

### For Windows Users

Open Command Prompt (Win + R, type `cmd`) and run these commands one by one:

```bash
pip install --upgrade pillow
python bikroy_mart_fixed.py
```

### For Mac Users

Open Terminal (Cmd + Space, type Terminal) and run:

```bash
pip3 install --upgrade pillow
python3 bikroy_mart_fixed.py
```

### For Linux Users

Open Terminal and run:

```bash
pip3 install --upgrade pillow
python3 bikroy_mart_fixed.py
```

## Using requirements.txt (Optional)

If you want to install everything at once:

```bash
pip install -r requirements.txt
python bikroy_mart_fixed.py
```

## First Login Credentials

**Test Account (if you want to register first):**
- Username: `testuser`
- Password: `test123`

Or just create your own account by clicking "Register here"

## What You'll See

1. **Login Screen** - Register or login with username/password
2. **Dashboard** - See 8 colorful category cards (Electronics, Vehicles, Furniture, etc.)
3. **Category Browse** - Click any category to see subcategories
4. **Products** - View all products with prices and ratings
5. **Cart** - Add products and place orders
6. **Orders** - View your order history

## Main Features to Try

✅ **Register** - Create new account
✅ **Browse** - Click categories to explore 136 products
✅ **Search** - View products organized by type
✅ **Cart** - Add products with quantity selection
✅ **Order** - Place order with address and phone
✅ **Save Info** - Remember customer details for next order
✅ **History** - View all your past orders

## Folder Setup (First Time Only)

The app creates these automatically:
- `assets/` - For product and category images
- `mart_users.json` - Database for users and orders

## If Something Goes Wrong

### Python not found
```bash
# Add Python to PATH and try again
# Or reinstall Python with "Add to PATH" checked
```

### Pillow error
```bash
pip install --upgrade pillow
# or
pip3 install --upgrade pillow
```

### Port or file errors
- Delete `mart_users.json` to reset database
- Close other Python applications
- Run as Administrator (Windows only)

## System Requirements

- **OS**: Windows, Mac, or Linux
- **Python**: 3.7 or higher
- **RAM**: 512 MB
- **Disk Space**: 50 MB
- **Internet**: Not required (offline app)

## Running from VS Code

1. Open VS Code
2. Open the folder containing `bikroy_mart_fixed.py`
3. Click the file
4. Press `F5` or click Run button
5. Or press Ctrl + ` to open terminal and run:
   ```bash
   python bikroy_mart_fixed.py
   ```

## Password Reset

There's no built-in password reset. If you forget:
1. Delete `mart_users.json`
2. Run app again
3. Register with new account

All previous data will be lost!

---

**That's it! The app is ready to use.** 🎉

Start registering, browsing products, and placing orders!
