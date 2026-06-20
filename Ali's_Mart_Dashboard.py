import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import hashlib
import datetime
import shutil
import uuid
from PIL import Image, ImageTk, ImageDraw, ImageFont

# ═════════════════════════════════════════════
#  DATABASE & COLORS
# ═════════════════════════════════════════════
DB_FILE = "mart_users.json"

BG = "#0d0d1a"
CARD = "#1a1a2e"
CARD2 = "#16213e"
TEXT = "#e8e8f0"
SUBTEXT = "#9999aa"
ENTRY_BG = "#1e1e35"
ACCENT = "#ff6b6b"
ACCENT2 = "#ff8787"
GREEN = "#39d98a"
GOLD = "#FFD700"
WHITE = "#ffffff"
CYAN = "#00d2ff"

CARD_COLORS = [
    {"bg": "#1a1035", "accent": "#ff6b6b", "btn": "#ff6b6b"},
    {"bg": "#0d2137", "accent": "#00d2ff", "btn": "#00d2ff"},
    {"bg": "#0d2a1f", "accent": "#39d98a", "btn": "#39d98a"},
    {"bg": "#2a1a0d", "accent": "#FF8C42", "btn": "#FF8C42"},
    {"bg": "#1e0d30", "accent": "#9b59b6", "btn": "#9b59b6"},
    {"bg": "#2a0d1a", "accent": "#f72585", "btn": "#f72585"},
    {"bg": "#0d1a2a", "accent": "#3A86FF", "btn": "#3A86FF"},
    {"bg": "#0d2a27", "accent": "#43b89c", "btn": "#43b89c"},
]

# ═════════════════════════════════════════════
#  CATEGORY STRUCTURE
# ═════════════════════════════════════════════
CATEGORIES_DATA = {
    "Electronics": {
        "cover_image": "assets/category_electronics.png",
        "emoji": "📱",
        "color": "#FF6B6B",
        "gradient": ("#FF6B6B", "#FF8E53"),
        "subcategories": {
            "Smartphones": {
                "emoji": "📱",
                "color": "#FF6B6B",
                "sub_subcategories": ["Android Phones", "iPhones", "Budget Phones", "Flagship Phones"]
            },
            "Computers": {
                "emoji": "💻",
                "color": "#FF8E53",
                "sub_subcategories": ["Laptops", "Desktop PCs", "All-in-One", "Workstations"]
            },
            "Gaming": {
                "emoji": "🎮",
                "color": "#e63946",
                "sub_subcategories": ["Gaming PCs", "Consoles", "Gaming Accessories", "VR Headsets"]
            }
        },
        "description": "Latest tech gadgets and electronics"
    },
    "Vehicles": {
        "cover_image": "assets/category_vehicles.png",
        "emoji": "🚗",
        "color": "#4ECDC4",
        "gradient": ("#4ECDC4", "#2BC0B4"),
        "subcategories": {
            "Bikes": {
                "emoji": "🏍️",
                "color": "#4ECDC4",
                "sub_subcategories": ["125cc Bikes", "70cc Bikes", "Sports Bikes", "Electric Bikes"]
            },
            "Cars": {
                "emoji": "🚗",
                "color": "#2BC0B4",
                "sub_subcategories": ["Sedans", "SUVs", "Hatchbacks", "Electric Cars"]
            }
        },
        "description": "Bikes, cars, and vehicles"
    },
    "Furniture": {
        "cover_image": "assets/category_furniture.png",
        "emoji": "🛋️",
        "color": "#95E1D3",
        "gradient": ("#95E1D3", "#56C596"),
        "subcategories": {
            "Seating": {
                "emoji": "🛋️",
                "color": "#95E1D3",
                "sub_subcategories": ["Sofa Sets", "Chairs", "Recliners", "Office Chairs"]
            },
            "Beds": {
                "emoji": "🛏️",
                "color": "#56C596",
                "sub_subcategories": ["Single Beds", "Double Beds", "King Size", "Bunk Beds"]
            }
        },
        "description": "Quality furniture for your home"
    },
    "Clothing": {
        "cover_image": "assets/category_clothing.png",
        "emoji": "👔",
        "color": "#F7DC6F",
        "gradient": ("#F7DC6F", "#F4A261"),
        "subcategories": {
            "Men's Clothing": {
                "emoji": "👔",
                "color": "#F7DC6F",
                "sub_subcategories": ["Formal Shirts", "Casual Wear", "Shalwar Kameez", "Jackets"]
            },
            "Women's Clothing": {
                "emoji": "👗",
                "color": "#F4A261",
                "sub_subcategories": ["Lawn Suits", "Formal Wear", "Party Dresses", "Abayas"]
            }
        },
        "description": "Fashion and apparel collection"
    },
    "Property": {
        "cover_image": "assets/category_property.png",
        "emoji": "🏠",
        "color": "#BB8FCE",
        "gradient": ("#BB8FCE", "#8E5BAF"),
        "subcategories": {
            "Houses": {
                "emoji": "🏠",
                "color": "#BB8FCE",
                "sub_subcategories": ["3 Marla", "5 Marla", "10 Marla", "1 Kanal"]
            },
            "Shops & Offices": {
                "emoji": "🏪",
                "color": "#8E5BAF",
                "sub_subcategories": ["Shops for Rent", "Shops for Sale", "Offices", "Plazas"]
            }
        },
        "description": "Real estate and properties"
    },
    "Pets": {
        "cover_image": "assets/category_pets.png",
        "emoji": "🐕",
        "color": "#F8B88B",
        "gradient": ("#F8B88B", "#E07A5F"),
        "subcategories": {
            "Dogs": {
                "emoji": "🐕",
                "color": "#F8B88B",
                "sub_subcategories": ["Puppies", "Adult Dogs", "Guard Dogs", "Toy Breeds"]
            },
            "Other Pets": {
                "emoji": "🐈",
                "color": "#E07A5F",
                "sub_subcategories": ["Cats", "Birds", "Fish", "Rabbits"]
            }
        },
        "description": "Pets and animal companions"
    },
    "Appliances": {
        "cover_image": "assets/category_appliances.png",
        "emoji": "❄️",
        "color": "#85C1E2",
        "gradient": ("#85C1E2", "#3A86FF"),
        "subcategories": {
            "Cooling": {
                "emoji": "❄️",
                "color": "#85C1E2",
                "sub_subcategories": ["Air Conditioners", "Fans", "Air Coolers", "Refrigerators"]
            },
            "Kitchen": {
                "emoji": "🍳",
                "color": "#3A86FF",
                "sub_subcategories": ["Microwaves", "Blenders", "Dishwashers", "Ovens"]
            }
        },
        "description": "Home appliances and electronics"
    },
    "Sports": {
        "cover_image": "assets/category_sports.png",
        "emoji": "🏃",
        "color": "#52BE80",
        "gradient": ("#52BE80", "#27AE60"),
        "subcategories": {
            "Cricket": {
                "emoji": "🏏",
                "color": "#52BE80",
                "sub_subcategories": ["Bats", "Balls", "Protective Gear", "Wickets"]
            },
            "Fitness": {
                "emoji": "🏋️",
                "color": "#27AE60",
                "sub_subcategories": ["Treadmills", "Dumbbells", "Yoga Mats", "Resistance Bands"]
            }
        },
        "description": "Sports equipment and fitness gear"
    }
}

# ═════════════════════════════════════════════
#  PRODUCTS DATA - DISTRIBUTED ACROSS ALL SUBCATEGORIES
# ═════════════════════════════════════════════
PRODUCTS = [
    # ELECTRONICS - Smartphones - Android Phones
    {"id": 1, "name": "Samsung Galaxy A54", "category": "Electronics", "subcategory": "Smartphones", "sub_subcategory": "Android Phones", "price": 45000, "stock": 12, "emoji": "📱", "description": "120Hz AMOLED display, 50MP camera", "rating": 4.5, "specs": "RAM: 8GB | Storage: 128GB", "image": "assets/samsung_galaxy_a54.png"},
    {"id": 2, "name": "OnePlus 11", "category": "Electronics", "subcategory": "Smartphones", "sub_subcategory": "Android Phones", "price": 65000, "stock": 8, "emoji": "📱", "description": "Fast performance with 5G", "rating": 4.6, "specs": "RAM: 12GB | Storage: 256GB", "image": "assets/oneplus_11.png"},
    
    # ELECTRONICS - Smartphones - iPhones
    {"id": 3, "name": "iPhone 13 (Used)", "category": "Electronics", "subcategory": "Smartphones", "sub_subcategory": "iPhones", "price": 85000, "stock": 5, "emoji": "📱", "description": "Gently used with 85% battery health", "rating": 4.8, "specs": "Storage: 128GB | Color: Midnight", "image": "assets/iphone_13_used.png"},
    {"id": 4, "name": "iPhone 14", "category": "Electronics", "subcategory": "Smartphones", "sub_subcategory": "iPhones", "price": 165000, "stock": 3, "emoji": "📱", "description": "Latest Apple technology", "rating": 4.9, "specs": "Storage: 256GB | Color: Blue", "image": "assets/iphone_14.png"},
    
    # ELECTRONICS - Smartphones - Budget Phones
    {"id": 5, "name": "Tecno Spark 10", "category": "Electronics", "subcategory": "Smartphones", "sub_subcategory": "Budget Phones", "price": 22000, "stock": 20, "emoji": "📱", "description": "7000mAh battery, 50MP camera", "rating": 4.1, "specs": "RAM: 4GB | Storage: 128GB", "image": "assets/tecno_spark10.png"},
    {"id": 6, "name": "Infinix Note 13", "category": "Electronics", "subcategory": "Smartphones", "sub_subcategory": "Budget Phones", "price": 28000, "stock": 15, "emoji": "📱", "description": "Good performance under budget", "rating": 4.2, "specs": "RAM: 8GB | Storage: 256GB", "image": "assets/infinix_note13.png"},
    
    # ELECTRONICS - Smartphones - Flagship Phones
    {"id": 7, "name": "Samsung Galaxy S23 Ultra", "category": "Electronics", "subcategory": "Smartphones", "sub_subcategory": "Flagship Phones", "price": 195000, "stock": 4, "emoji": "📱", "description": "200MP camera, S Pen included", "rating": 4.9, "specs": "RAM: 12GB | Storage: 256GB", "image": "assets/samsung_s23_ultra.png"},
    {"id": 8, "name": "iPhone 15 Pro Max", "category": "Electronics", "subcategory": "Smartphones", "sub_subcategory": "Flagship Phones", "price": 250000, "stock": 2, "emoji": "📱", "description": "Premium flagship phone", "rating": 5.0, "specs": "RAM: 8GB | Storage: 512GB", "image": "assets/iphone_15_pro.png"},
    
    # ELECTRONICS - Computers - Laptops
    {"id": 9, "name": "Dell Inspiron 15", "category": "Electronics", "subcategory": "Computers", "sub_subcategory": "Laptops", "price": 85000, "stock": 7, "emoji": "💻", "description": "Intel Core i5, 15.6 FHD display", "rating": 4.4, "specs": "RAM: 8GB | SSD: 512GB", "image": "assets/dell_inspiron15.png"},
    {"id": 10, "name": "HP Pavilion 14", "category": "Electronics", "subcategory": "Computers", "sub_subcategory": "Laptops", "price": 95000, "stock": 6, "emoji": "💻", "description": "Lightweight and powerful", "rating": 4.5, "specs": "RAM: 16GB | SSD: 512GB", "image": "assets/hp_pavilion14.png"},
    
    # ELECTRONICS - Computers - Desktop PCs
    {"id": 11, "name": "Gaming PC (RTX 3060)", "category": "Electronics", "subcategory": "Computers", "sub_subcategory": "Desktop PCs", "price": 120000, "stock": 6, "emoji": "💻", "description": "Ultimate gaming rig", "rating": 4.7, "specs": "CPU: i5-12400F | GPU: RTX 3060 | RAM: 16GB", "image": "assets/gaming_pc_rtx3060.png"},
    {"id": 12, "name": "Work Station PC", "category": "Electronics", "subcategory": "Computers", "sub_subcategory": "Desktop PCs", "price": 150000, "stock": 4, "emoji": "💻", "description": "Professional workstation", "rating": 4.6, "specs": "CPU: Ryzen 5 | RAM: 32GB | SSD: 1TB", "image": "assets/workstation_pc.png"},
    
    # ELECTRONICS - Computers - All-in-One
    {"id": 13, "name": "Apple iMac 24", "category": "Electronics", "subcategory": "Computers", "sub_subcategory": "All-in-One", "price": 280000, "stock": 2, "emoji": "💻", "description": "Beautiful all-in-one Mac", "rating": 4.8, "specs": "M3 Chip | RAM: 8GB | Storage: 512GB", "image": "assets/imac_24.png"},
    {"id": 14, "name": "Dell XPS 27", "category": "Electronics", "subcategory": "Computers", "sub_subcategory": "All-in-One", "price": 250000, "stock": 3, "emoji": "💻", "description": "Premium all-in-one PC", "rating": 4.7, "specs": "Intel i7 | RAM: 16GB | 4K Display", "image": "assets/dell_xps27.png"},
    
    # ELECTRONICS - Computers - Workstations
    {"id": 15, "name": "HP Z Workstation", "category": "Electronics", "subcategory": "Computers", "sub_subcategory": "Workstations", "price": 350000, "stock": 2, "emoji": "💻", "description": "Professional workstation for designers", "rating": 4.9, "specs": "Xeon CPU | 32GB RAM | RTX 4000", "image": "assets/hp_z_workstation.png"},
    {"id": 16, "name": "Lenovo ThinkStation", "category": "Electronics", "subcategory": "Computers", "sub_subcategory": "Workstations", "price": 320000, "stock": 3, "emoji": "💻", "description": "High performance workstation", "rating": 4.8, "specs": "Xeon Platinum | 64GB RAM | SSD: 2TB", "image": "assets/lenovo_thinkstation.png"},
    
    # ELECTRONICS - Gaming - Gaming PCs
    {"id": 17, "name": "ASUS ROG Gaming PC", "category": "Electronics", "subcategory": "Gaming", "sub_subcategory": "Gaming PCs", "price": 180000, "stock": 5, "emoji": "🎮", "description": "Extreme gaming performance", "rating": 4.8, "specs": "RTX 4070 | i7-13700K | 32GB RAM", "image": "assets/asus_rog_pc.png"},
    {"id": 18, "name": "Alienware Aurora", "category": "Electronics", "subcategory": "Gaming", "sub_subcategory": "Gaming PCs", "price": 200000, "stock": 4, "emoji": "🎮", "description": "Ultimate gaming beast", "rating": 4.9, "specs": "RTX 4080 | i9-13900K | 32GB RAM", "image": "assets/alienware_aurora.png"},
    
    # ELECTRONICS - Gaming - Consoles
    {"id": 19, "name": "PlayStation 5", "category": "Electronics", "subcategory": "Gaming", "sub_subcategory": "Consoles", "price": 150000, "stock": 3, "emoji": "🎮", "description": "4K gaming, ultra-fast SSD", "rating": 4.9, "specs": "Storage: 825GB | Resolution: 4K", "image": "assets/playstation5.png"},
    {"id": 20, "name": "Xbox Series X", "category": "Electronics", "subcategory": "Gaming", "sub_subcategory": "Consoles", "price": 145000, "stock": 3, "emoji": "🎮", "description": "Most powerful console", "rating": 4.8, "specs": "12 TFLOPS | 1TB Storage", "image": "assets/xbox_series_x.png"},
    
    # ELECTRONICS - Gaming - Gaming Accessories
    {"id": 21, "name": "Gaming Chair (RGB)", "category": "Electronics", "subcategory": "Gaming", "sub_subcategory": "Gaming Accessories", "price": 18000, "stock": 10, "emoji": "🎮", "description": "Ergonomic with RGB lighting", "rating": 4.3, "specs": "Max Weight: 120kg | PU Leather", "image": "assets/gaming_chair_rgb.png"},
    {"id": 22, "name": "Gaming Keyboard RGB", "category": "Electronics", "subcategory": "Gaming", "sub_subcategory": "Gaming Accessories", "price": 8000, "stock": 12, "emoji": "⌨️", "description": "Mechanical keyboard with RGB", "rating": 4.4, "specs": "USB | Customizable Lighting", "image": "assets/gaming_keyboard.png"},
    
    # ELECTRONICS - Gaming - VR Headsets
    {"id": 23, "name": "Meta Quest 3", "category": "Electronics", "subcategory": "Gaming", "sub_subcategory": "VR Headsets", "price": 65000, "stock": 4, "emoji": "🥽", "description": "Advanced VR experience", "rating": 4.7, "specs": "4K Display | 128GB Storage", "image": "assets/quest_3.png"},
    {"id": 24, "name": "PlayStation VR2", "category": "Electronics", "subcategory": "Gaming", "sub_subcategory": "VR Headsets", "price": 75000, "stock": 3, "emoji": "🥽", "description": "Next-gen VR for PS5", "rating": 4.8, "specs": "4K OLED | 110 degree FOV", "image": "assets/psvr2.png"},
    
    # VEHICLES - Bikes - 125cc Bikes
    {"id": 25, "name": "Yamaha YBR 125", "category": "Vehicles", "subcategory": "Bikes", "sub_subcategory": "125cc Bikes", "price": 290000, "stock": 5, "emoji": "🏍️", "description": "Powerful 125cc engine", "rating": 4.6, "specs": "Engine: 125cc | Mileage: 40km/L", "image": "assets/yamaha_ybr125.png"},
    {"id": 26, "name": "Honda CB 125R", "category": "Vehicles", "subcategory": "Bikes", "sub_subcategory": "125cc Bikes", "price": 280000, "stock": 6, "emoji": "🏍️", "description": "Reliable and stylish", "rating": 4.5, "specs": "Engine: 125cc | Fuel Tank: 15L", "image": "assets/honda_cb125.png"},
    
    # VEHICLES - Bikes - 70cc Bikes
    {"id": 27, "name": "Honda CD 70", "category": "Vehicles", "subcategory": "Bikes", "sub_subcategory": "70cc Bikes", "price": 175000, "stock": 3, "emoji": "🏍️", "description": "Pakistan's favorite bike", "rating": 4.7, "specs": "Engine: 4-Stroke | Fuel Tank: 8.5L", "image": "assets/honda_cd_70.png"},
    {"id": 28, "name": "Atlas Honda 70", "category": "Vehicles", "subcategory": "Bikes", "sub_subcategory": "70cc Bikes", "price": 172000, "stock": 4, "emoji": "🏍️", "description": "Fuel efficient commuter", "rating": 4.6, "specs": "Engine: 70cc | Transmission: 4-Speed", "image": "assets/atlas_honda_70.png"},
    
    # VEHICLES - Bikes - Sports Bikes
    {"id": 29, "name": "Super Power Hawk 200", "category": "Vehicles", "subcategory": "Bikes", "sub_subcategory": "Sports Bikes", "price": 420000, "stock": 2, "emoji": "🏍️", "description": "Aggressive sports bike", "rating": 4.5, "specs": "Engine: 200cc | Brakes: Disc", "image": "assets/sports_bike_200.png"},
    {"id": 30, "name": "Suzuki GSX-R150", "category": "Vehicles", "subcategory": "Bikes", "sub_subcategory": "Sports Bikes", "price": 380000, "stock": 3, "emoji": "🏍️", "description": "Sleek sports design", "rating": 4.6, "specs": "Engine: 150cc | Max Speed: 130km/h", "image": "assets/suzuki_gsxr.png"},
    
    # VEHICLES - Bikes - Electric Bikes
    {"id": 31, "name": "Sohrab Electric Bike", "category": "Vehicles", "subcategory": "Bikes", "sub_subcategory": "Electric Bikes", "price": 320000, "stock": 5, "emoji": "⚡", "description": "Eco-friendly electric", "rating": 4.4, "specs": "Battery: 60V | Range: 100km", "image": "assets/sohrab_ebike.png"},
    {"id": 32, "name": "Infineon EBike 3000", "category": "Vehicles", "subcategory": "Bikes", "sub_subcategory": "Electric Bikes", "price": 350000, "stock": 4, "emoji": "⚡", "description": "Premium electric bike", "rating": 4.7, "specs": "Motor: 3000W | Speed: 60km/h", "image": "assets/infineon_ebike.png"},
    
    # VEHICLES - Cars - Sedans
    {"id": 33, "name": "Toyota Corolla 2018", "category": "Vehicles", "subcategory": "Cars", "sub_subcategory": "Sedans", "price": 3200000, "stock": 1, "emoji": "🚗", "description": "Original condition, first owner", "rating": 4.9, "specs": "Engine: 1.3L VVTi | Mileage: 65,000 km", "image": "assets/toyota_corolla_2018.png"},
    {"id": 34, "name": "Honda Civic 2019", "category": "Vehicles", "subcategory": "Cars", "sub_subcategory": "Sedans", "price": 3800000, "stock": 1, "emoji": "🚗", "description": "Well maintained sedan", "rating": 4.8, "specs": "Engine: 1.8L | Mileage: 45,000 km", "image": "assets/honda_civic_2019.png"},
    
    # VEHICLES - Cars - SUVs
    {"id": 35, "name": "Toyota Fortuner", "category": "Vehicles", "subcategory": "Cars", "sub_subcategory": "SUVs", "price": 8500000, "stock": 1, "emoji": "🚗", "description": "4x4 SUV with 7 seats", "rating": 4.8, "specs": "Engine: 2.7L | Drive: 4WD", "image": "assets/toyota_fortuner.png"},
    {"id": 36, "name": "Honda CR-V", "category": "Vehicles", "subcategory": "Cars", "sub_subcategory": "SUVs", "price": 5200000, "stock": 1, "emoji": "🚗", "description": "Compact SUV, spacious", "rating": 4.7, "specs": "Engine: 1.5L | 5-Seater", "image": "assets/honda_crv.png"},
    
    # VEHICLES - Cars - Hatchbacks
    {"id": 37, "name": "Suzuki WagonR", "category": "Vehicles", "subcategory": "Cars", "sub_subcategory": "Hatchbacks", "price": 2200000, "stock": 2, "emoji": "🚗", "description": "Compact and efficient", "rating": 4.5, "specs": "Engine: 1.0L | Fuel Efficient", "image": "assets/suzuki_wagonr.png"},
    {"id": 38, "name": "Hyundai i10", "category": "Vehicles", "subcategory": "Cars", "sub_subcategory": "Hatchbacks", "price": 2400000, "stock": 2, "emoji": "🚗", "description": "Modern hatchback", "rating": 4.6, "specs": "Engine: 1.2L | 5-Seater", "image": "assets/hyundai_i10.png"},
    
    # VEHICLES - Cars - Electric Cars
    {"id": 39, "name": "Tesla Model 3", "category": "Vehicles", "subcategory": "Cars", "sub_subcategory": "Electric Cars", "price": 6500000, "stock": 1, "emoji": "⚡", "description": "Premium electric sedan", "rating": 5.0, "specs": "Range: 500km | Speed: 225km/h", "image": "assets/tesla_model3.png"},
    {"id": 40, "name": "BYD Qin", "category": "Vehicles", "subcategory": "Cars", "sub_subcategory": "Electric Cars", "price": 4800000, "stock": 1, "emoji": "⚡", "description": "Affordable electric car", "rating": 4.6, "specs": "Range: 400km | Battery: 80kWh", "image": "assets/byd_qin.png"},
    
    # FURNITURE - Seating - Sofa Sets
    {"id": 41, "name": "Sofa Set (5-Seater)", "category": "Furniture", "subcategory": "Seating", "sub_subcategory": "Sofa Sets", "price": 35000, "stock": 7, "emoji": "🛋️", "description": "Luxurious velvet sofa", "rating": 4.4, "specs": "Capacity: 5 | Frame: Acacia Wood", "image": "assets/sofa_set_5seater.png"},
    {"id": 42, "name": "L-Shape Sofa", "category": "Furniture", "subcategory": "Seating", "sub_subcategory": "Sofa Sets", "price": 45000, "stock": 5, "emoji": "🛋️", "description": "Modern L-shaped design", "rating": 4.5, "specs": "Capacity: 6 | Material: Fabric", "image": "assets/lshape_sofa.png"},
    
    # FURNITURE - Seating - Chairs
    {"id": 43, "name": "Dining Chair Set", "category": "Furniture", "subcategory": "Seating", "sub_subcategory": "Chairs", "price": 12000, "stock": 8, "emoji": "🪑", "description": "Set of 4 dining chairs", "rating": 4.3, "specs": "Material: Wood | Style: Modern", "image": "assets/dining_chair_set.png"},
    {"id": 44, "name": "Accent Chair", "category": "Furniture", "subcategory": "Seating", "sub_subcategory": "Chairs", "price": 8000, "stock": 10, "emoji": "🪑", "description": "Comfortable accent chair", "rating": 4.4, "specs": "Material: Fabric | Color: Gray", "image": "assets/accent_chair.png"},
    
    # FURNITURE - Seating - Recliners
    {"id": 45, "name": "Leather Recliner", "category": "Furniture", "subcategory": "Seating", "sub_subcategory": "Recliners", "price": 25000, "stock": 4, "emoji": "🛋️", "description": "Luxury leather recliner", "rating": 4.6, "specs": "Material: Genuine Leather", "image": "assets/leather_recliner.png"},
    {"id": 46, "name": "Electric Recliner", "category": "Furniture", "subcategory": "Seating", "sub_subcategory": "Recliners", "price": 32000, "stock": 3, "emoji": "🛋️", "description": "Power reclining chair", "rating": 4.7, "specs": "Power: Electric | Massage: Yes", "image": "assets/electric_recliner.png"},
    
    # FURNITURE - Seating - Office Chairs
    {"id": 47, "name": "Office Chair (Mesh)", "category": "Furniture", "subcategory": "Seating", "sub_subcategory": "Office Chairs", "price": 8500, "stock": 15, "emoji": "🪑", "description": "Ergonomic mesh chair", "rating": 4.2, "specs": "Material: Mesh | Adjustable: Yes", "image": "assets/office_chair_mesh.png"},
    {"id": 48, "name": "Executive Chair", "category": "Furniture", "subcategory": "Seating", "sub_subcategory": "Office Chairs", "price": 15000, "stock": 10, "emoji": "🪑", "description": "Premium executive chair", "rating": 4.5, "specs": "Material: Leather | Lumbar Support", "image": "assets/executive_chair.png"},
    
    # FURNITURE - Beds - Single Beds
    {"id": 49, "name": "Single Bed with Storage", "category": "Furniture", "subcategory": "Beds", "sub_subcategory": "Single Beds", "price": 12000, "stock": 6, "emoji": "🛏️", "description": "Space-saving with storage", "rating": 4.1, "specs": "Size: 3x6 ft | Material: Wood", "image": "assets/single_bed_storage.png"},
    {"id": 50, "name": "Simple Single Bed", "category": "Furniture", "subcategory": "Beds", "sub_subcategory": "Single Beds", "price": 10000, "stock": 8, "emoji": "🛏️", "description": "Basic single bed frame", "rating": 4.0, "specs": "Size: 3x6 ft | Solid Frame", "image": "assets/simple_single_bed.png"},
    
    # FURNITURE - Beds - Double Beds
    {"id": 51, "name": "Double Bed Standard", "category": "Furniture", "subcategory": "Beds", "sub_subcategory": "Double Beds", "price": 18000, "stock": 7, "emoji": "🛏️", "description": "Comfortable double bed", "rating": 4.3, "specs": "Size: 4.5x6.5 ft | Wood Frame", "image": "assets/double_bed_std.png"},
    {"id": 52, "name": "Premium Double Bed", "category": "Furniture", "subcategory": "Beds", "sub_subcategory": "Double Beds", "price": 24000, "stock": 5, "emoji": "🛏️", "description": "Premium quality bed", "rating": 4.5, "specs": "Size: 4.5x6.5 ft | Sheesham Wood", "image": "assets/premium_double_bed.png"},
    
    # FURNITURE - Beds - King Size
    {"id": 53, "name": "Wooden Bed (King)", "category": "Furniture", "subcategory": "Beds", "sub_subcategory": "King Size", "price": 28000, "stock": 4, "emoji": "🛏️", "description": "Premium king size bed", "rating": 4.6, "specs": "Size: 6x6.5 ft | Sheesham Wood", "image": "assets/wooden_bed_king.png"},
    {"id": 54, "name": "Luxury King Bed", "category": "Furniture", "subcategory": "Beds", "sub_subcategory": "King Size", "price": 35000, "stock": 3, "emoji": "🛏️", "description": "Ultra luxury king bed", "rating": 4.8, "specs": "Size: 6x6.5 ft | Upholstered", "image": "assets/luxury_king_bed.png"},
    
    # FURNITURE - Beds - Bunk Beds
    {"id": 55, "name": "Metal Bunk Bed", "category": "Furniture", "subcategory": "Beds", "sub_subcategory": "Bunk Beds", "price": 16000, "stock": 5, "emoji": "🛏️", "description": "Durable metal bunk", "rating": 4.2, "specs": "Material: Steel | Weight Capacity: 300kg", "image": "assets/metal_bunk_bed.png"},
    {"id": 56, "name": "Wooden Bunk Bed", "category": "Furniture", "subcategory": "Beds", "sub_subcategory": "Bunk Beds", "price": 20000, "stock": 4, "emoji": "🛏️", "description": "Solid wood bunk bed", "rating": 4.4, "specs": "Material: Wood | Storage Drawer", "image": "assets/wooden_bunk_bed.png"},
    
    # CLOTHING - Men's - Formal Shirts
    {"id": 57, "name": "Gents Dress Shirt", "category": "Clothing", "subcategory": "Men's Clothing", "sub_subcategory": "Formal Shirts", "price": 1800, "stock": 30, "emoji": "👔", "description": "100% cotton formal shirt", "rating": 4.2, "specs": "Material: Cotton | Fit: Slim", "image": "assets/gents_dress_shirt.png"},
    {"id": 58, "name": "Premium Business Shirt", "category": "Clothing", "subcategory": "Men's Clothing", "sub_subcategory": "Formal Shirts", "price": 2500, "stock": 20, "emoji": "👔", "description": "Premium business wear", "rating": 4.4, "specs": "Material: Egyptian Cotton | Sizes: S-XL", "image": "assets/business_shirt.png"},
    
    # CLOTHING - Men's - Casual Wear
    {"id": 59, "name": "Gents Casual T-Shirt", "category": "Clothing", "subcategory": "Men's Clothing", "sub_subcategory": "Casual Wear", "price": 850, "stock": 50, "emoji": "👕", "description": "Comfortable casual t-shirt", "rating": 4.0, "specs": "Material: Cotton | Colors: 10+", "image": "assets/gents_casual_tshirt.png"},
    {"id": 60, "name": "Casual Polo Shirt", "category": "Clothing", "subcategory": "Men's Clothing", "sub_subcategory": "Casual Wear", "price": 1200, "stock": 35, "emoji": "👕", "description": "Stylish polo shirt", "rating": 4.3, "specs": "Material: 100% Cotton | Sizes: M-XXL", "image": "assets/polo_shirt.png"},
    
    # CLOTHING - Men's - Shalwar Kameez
    {"id": 61, "name": "Gents Shalwar Kameez", "category": "Clothing", "subcategory": "Men's Clothing", "sub_subcategory": "Shalwar Kameez", "price": 2200, "stock": 25, "emoji": "👔", "description": "Traditional karandi", "rating": 4.4, "specs": "Fabric: Karandi | 2-Pc | Sizes: M-XXL", "image": "assets/gents_shalwar_kameez.png"},
    {"id": 62, "name": "Eid Shalwar Kameez", "category": "Clothing", "subcategory": "Men's Clothing", "sub_subcategory": "Shalwar Kameez", "price": 3000, "stock": 18, "emoji": "👔", "description": "Premium Eid wear", "rating": 4.6, "specs": "Fabric: Banarsi | Embroidered", "image": "assets/eid_shalwar_kameez.png"},
    
    # CLOTHING - Men's - Jackets
    {"id": 63, "name": "Casual Jacket", "category": "Clothing", "subcategory": "Men's Clothing", "sub_subcategory": "Jackets", "price": 4500, "stock": 12, "emoji": "🧥", "description": "Stylish casual jacket", "rating": 4.3, "specs": "Material: Cotton | Colors: Black, Blue", "image": "assets/casual_jacket.png"},
    {"id": 64, "name": "Leather Jacket", "category": "Clothing", "subcategory": "Men's Clothing", "sub_subcategory": "Jackets", "price": 8000, "stock": 8, "emoji": "🧥", "description": "Genuine leather jacket", "rating": 4.6, "specs": "Material: Leather | Classic Style", "image": "assets/leather_jacket.png"},
    
    # CLOTHING - Women's - Lawn Suits
    {"id": 65, "name": "Ladies Lawn Suit", "category": "Clothing", "subcategory": "Women's Clothing", "sub_subcategory": "Lawn Suits", "price": 2500, "stock": 20, "emoji": "👗", "description": "Designer lawn suit", "rating": 4.5, "specs": "Fabric: Lawn | 3-Pc | Digital Print", "image": "assets/ladies_lawn_suit.png"},
    {"id": 66, "name": "Premium Lawn Suit", "category": "Clothing", "subcategory": "Women's Clothing", "sub_subcategory": "Lawn Suits", "price": 3500, "stock": 15, "emoji": "👗", "description": "Luxury lawn collection", "rating": 4.7, "specs": "Fabric: Premium Lawn | Embroidered", "image": "assets/premium_lawn.png"},
    
    # CLOTHING - Women's - Formal Wear
    {"id": 67, "name": "Saree", "category": "Clothing", "subcategory": "Women's Clothing", "sub_subcategory": "Formal Wear", "price": 4000, "stock": 10, "emoji": "👗", "description": "Traditional saree", "rating": 4.4, "specs": "Fabric: Silk | Colors: Traditional", "image": "assets/saree.png"},
    {"id": 68, "name": "Formal Kurti", "category": "Clothing", "subcategory": "Women's Clothing", "sub_subcategory": "Formal Wear", "price": 2800, "stock": 12, "emoji": "👗", "description": "Formal occasion kurti", "rating": 4.5, "specs": "Fabric: Cotton | Embroidered", "image": "assets/formal_kurti.png"},
    
    # CLOTHING - Women's - Party Dresses
    {"id": 69, "name": "Ladies Party Dress", "category": "Clothing", "subcategory": "Women's Clothing", "sub_subcategory": "Party Dresses", "price": 5500, "stock": 12, "emoji": "👗", "description": "Elegant party wear", "rating": 4.7, "specs": "Fabric: Net | Heavy Embroidery", "image": "assets/ladies_party_dress.png"},
    {"id": 70, "name": "Bridal Dress", "category": "Clothing", "subcategory": "Women's Clothing", "sub_subcategory": "Party Dresses", "price": 15000, "stock": 5, "emoji": "👗", "description": "Luxury bridal collection", "rating": 4.9, "specs": "Fabric: Silk | Heavily Embellished", "image": "assets/bridal_dress.png"},
    
    # CLOTHING - Women's - Abayas
    {"id": 71, "name": "Simple Abaya", "category": "Clothing", "subcategory": "Women's Clothing", "sub_subcategory": "Abayas", "price": 2000, "stock": 25, "emoji": "👗", "description": "Classic black abaya", "rating": 4.3, "specs": "Fabric: Nida | One Size", "image": "assets/simple_abaya.png"},
    {"id": 72, "name": "Designer Abaya", "category": "Clothing", "subcategory": "Women's Clothing", "sub_subcategory": "Abayas", "price": 4500, "stock": 15, "emoji": "👗", "description": "Designer abaya", "rating": 4.6, "specs": "Fabric: Premium Nida | Embroidered", "image": "assets/designer_abaya.png"},
    
    # PROPERTY - Houses - 3 Marla
    {"id": 73, "name": "House 3 Marla (DHA)", "category": "Property", "subcategory": "Houses", "sub_subcategory": "3 Marla", "price": 5500000, "stock": 1, "emoji": "🏠", "description": "3 Marla house in DHA", "rating": 4.7, "specs": "Beds: 2 | Baths: 2 | Location: DHA", "image": "assets/house_3marla_dha.png"},
    {"id": 74, "name": "House 3 Marla (Gulshan)", "category": "Property", "subcategory": "Houses", "sub_subcategory": "3 Marla", "price": 4800000, "stock": 1, "emoji": "🏠", "description": "3 Marla in Gulshan", "rating": 4.6, "specs": "Beds: 2 | Baths: 2", "image": "assets/house_3marla_gulshan.png"},
    
    # PROPERTY - Houses - 5 Marla
    {"id": 75, "name": "Lahore House (5 Marla)", "category": "Property", "subcategory": "Houses", "sub_subcategory": "5 Marla", "price": 9500000, "stock": 1, "emoji": "🏠", "description": "5 Marla in DHA Rahbar", "rating": 4.9, "specs": "Beds: 3 | Baths: 4", "image": "assets/lahore_house_5marla.png"},
    {"id": 76, "name": "House 5 Marla (Askari)", "category": "Property", "subcategory": "Houses", "sub_subcategory": "5 Marla", "price": 8800000, "stock": 1, "emoji": "🏠", "description": "5 Marla in Askari", "rating": 4.8, "specs": "Beds: 3 | Baths: 3", "image": "assets/house_5marla_askari.png"},
    
    # PROPERTY - Houses - 10 Marla
    {"id": 77, "name": "Islamabad House (10 Marla)", "category": "Property", "subcategory": "Houses", "sub_subcategory": "10 Marla", "price": 22000000, "stock": 1, "emoji": "🏠", "description": "10 Marla in Bahria Town", "rating": 4.8, "specs": "Beds: 4 | Baths: 5", "image": "assets/islamabad_house_10marla.png"},
    {"id": 78, "name": "House 10 Marla (DHA Islamabad)", "category": "Property", "subcategory": "Houses", "sub_subcategory": "10 Marla", "price": 25000000, "stock": 1, "emoji": "🏠", "description": "10 Marla in DHA Islamabad", "rating": 4.9, "specs": "Beds: 4 | Baths: 4", "image": "assets/house_10marla_dha.png"},
    
    # PROPERTY - Houses - 1 Kanal
    {"id": 79, "name": "1 Kanal House (Cantt)", "category": "Property", "subcategory": "Houses", "sub_subcategory": "1 Kanal", "price": 45000000, "stock": 1, "emoji": "🏠", "description": "1 Kanal in Cantt", "rating": 4.9, "specs": "Beds: 5 | Baths: 6", "image": "assets/house_1kanal_cantt.png"},
    {"id": 80, "name": "1 Kanal House (DHA)", "category": "Property", "subcategory": "Houses", "sub_subcategory": "1 Kanal", "price": 50000000, "stock": 1, "emoji": "🏠", "description": "1 Kanal in DHA Phase 5", "rating": 5.0, "specs": "Beds: 5 | Baths: 6 | Modern", "image": "assets/house_1kanal_dha.png"},
    
    # PROPERTY - Shops & Offices - Shops for Rent
    {"id": 81, "name": "Shop for Rent (Saddar)", "category": "Property", "subcategory": "Shops & Offices", "sub_subcategory": "Shops for Rent", "price": 15000, "stock": 2, "emoji": "🏪", "description": "Ground floor shop in Saddar", "rating": 4.3, "specs": "Area: 150 Sq Ft | Foot Traffic: High", "image": "assets/shop_rent_saddar.png"},
    {"id": 82, "name": "Shop for Rent (Mall)", "category": "Property", "subcategory": "Shops & Offices", "sub_subcategory": "Shops for Rent", "price": 25000, "stock": 2, "emoji": "🏪", "description": "Shop in shopping mall", "rating": 4.5, "specs": "Area: 200 Sq Ft | Modern Mall", "image": "assets/shop_rent_mall.png"},
    
    # PROPERTY - Shops & Offices - Shops for Sale
    {"id": 83, "name": "Shop for Sale (Main Road)", "category": "Property", "subcategory": "Shops & Offices", "sub_subcategory": "Shops for Sale", "price": 3500000, "stock": 1, "emoji": "🏪", "description": "Prime shop for sale", "rating": 4.6, "specs": "Area: 250 Sq Ft | Prime Location", "image": "assets/shop_sale_mainroad.png"},
    {"id": 84, "name": "Retail Shop (Commercial)", "category": "Property", "subcategory": "Shops & Offices", "sub_subcategory": "Shops for Sale", "price": 5000000, "stock": 1, "emoji": "🏪", "description": "Commercial retail space", "rating": 4.7, "specs": "Area: 350 Sq Ft | Parking Available", "image": "assets/retail_shop.png"},
    
    # PROPERTY - Shops & Offices - Offices
    {"id": 85, "name": "Office Space (Gulberg)", "category": "Property", "subcategory": "Shops & Offices", "sub_subcategory": "Offices", "price": 45000, "stock": 2, "emoji": "🏢", "description": "Office in Gulberg", "rating": 4.5, "specs": "Area: 500 Sq Ft | 3rd Floor", "image": "assets/office_gulberg.png"},
    {"id": 86, "name": "Office Space (Blue Area)", "category": "Property", "subcategory": "Shops & Offices", "sub_subcategory": "Offices", "price": 60000, "stock": 1, "emoji": "🏢", "description": "Premium office in Blue Area", "rating": 4.7, "specs": "Area: 600 Sq Ft | Power Backup", "image": "assets/office_blue_area.png"},
    
    # PROPERTY - Shops & Offices - Plazas
    {"id": 87, "name": "Plaza Office Space", "category": "Property", "subcategory": "Shops & Offices", "sub_subcategory": "Plazas", "price": 80000, "stock": 1, "emoji": "🏢", "description": "Office in commercial plaza", "rating": 4.6, "specs": "Area: 1000 Sq Ft | Ground Floor", "image": "assets/plaza_office.png"},
    {"id": 88, "name": "Plaza Retail Unit", "category": "Property", "subcategory": "Shops & Offices", "sub_subcategory": "Plazas", "price": 35000, "stock": 2, "emoji": "🏢", "description": "Retail unit in plaza", "rating": 4.5, "specs": "Area: 300 Sq Ft | High Traffic", "image": "assets/plaza_retail.png"},
    
    # PETS - Dogs - Puppies
    {"id": 89, "name": "Puppy (Golden Retriever)", "category": "Pets", "subcategory": "Dogs", "sub_subcategory": "Puppies", "price": 12000, "stock": 3, "emoji": "🐕", "description": "Healthy vaccinated puppy", "rating": 4.9, "specs": "Age: 2 Months | Vet Checked", "image": "assets/puppy_golden_retriever.png"},
    {"id": 90, "name": "Puppy (Labrador)", "category": "Pets", "subcategory": "Dogs", "sub_subcategory": "Puppies", "price": 15000, "stock": 2, "emoji": "🐕", "description": "Friendly Labrador puppy", "rating": 4.8, "specs": "Age: 2 Months | Dewormed", "image": "assets/puppy_labrador.png"},
    
    # PETS - Dogs - Adult Dogs
    {"id": 91, "name": "Adult Golden Retriever", "category": "Pets", "subcategory": "Dogs", "sub_subcategory": "Adult Dogs", "price": 20000, "stock": 2, "emoji": "🐕", "description": "Gentle adult dog", "rating": 4.7, "specs": "Age: 2 Years | Well Trained", "image": "assets/adult_golden.png"},
    {"id": 92, "name": "Adult Poodle", "category": "Pets", "subcategory": "Dogs", "sub_subcategory": "Adult Dogs", "price": 18000, "stock": 2, "emoji": "🐕", "description": "Intelligent poodle", "rating": 4.6, "specs": "Age: 3 Years | Groomed", "image": "assets/adult_poodle.png"},
    
    # PETS - Dogs - Guard Dogs
    {"id": 93, "name": "German Shepherd (Guard Dog)", "category": "Pets", "subcategory": "Dogs", "sub_subcategory": "Guard Dogs", "price": 25000, "stock": 2, "emoji": "🐕", "description": "Trained guard dog", "rating": 4.8, "specs": "Age: 1 Year | Trained for Security", "image": "assets/german_shepherd.png"},
    {"id": 94, "name": "Rottweiler", "category": "Pets", "subcategory": "Dogs", "sub_subcategory": "Guard Dogs", "price": 28000, "stock": 1, "emoji": "🐕", "description": "Powerful guard dog", "rating": 4.7, "specs": "Age: 1.5 Years | Protective", "image": "assets/rottweiler.png"},
    
    # PETS - Dogs - Toy Breeds
    {"id": 95, "name": "Pug Puppy", "category": "Pets", "subcategory": "Dogs", "sub_subcategory": "Toy Breeds", "price": 10000, "stock": 4, "emoji": "🐕", "description": "Cute pug puppy", "rating": 4.5, "specs": "Age: 3 Months | Adorable", "image": "assets/pug_puppy.png"},
    {"id": 96, "name": "Chihuahua", "category": "Pets", "subcategory": "Dogs", "sub_subcategory": "Toy Breeds", "price": 8000, "stock": 5, "emoji": "🐕", "description": "Tiny chihuahua", "rating": 4.4, "specs": "Age: 2 Months | Pocket Sized", "image": "assets/chihuahua.png"},
    
    # PETS - Other Pets - Cats
    {"id": 97, "name": "Persian Cat", "category": "Pets", "subcategory": "Other Pets", "sub_subcategory": "Cats", "price": 8000, "stock": 4, "emoji": "🐈", "description": "Beautiful Persian cat", "rating": 4.7, "specs": "Age: 3 Months | White Color", "image": "assets/persian_cat.png"},
    {"id": 98, "name": "Siamese Cat", "category": "Pets", "subcategory": "Other Pets", "sub_subcategory": "Cats", "price": 9000, "stock": 3, "emoji": "🐈", "description": "Elegant Siamese", "rating": 4.6, "specs": "Age: 4 Months | Vaccinated", "image": "assets/siamese_cat.png"},
    
    # PETS - Other Pets - Birds
    {"id": 99, "name": "Cocktail Parrot", "category": "Pets", "subcategory": "Other Pets", "sub_subcategory": "Birds", "price": 3500, "stock": 6, "emoji": "🦜", "description": "Hand-tamed parrot", "rating": 4.5, "specs": "Age: 6 Months | Cage Included", "image": "assets/cocktail_parrot.png"},
    {"id": 100, "name": "Budgies (Pair)", "category": "Pets", "subcategory": "Other Pets", "sub_subcategory": "Birds", "price": 2000, "stock": 8, "emoji": "🦜", "description": "Pair of budgerigars", "rating": 4.3, "specs": "Age: 3 Months | Colors: Various", "image": "assets/budgies_pair.png"},
    
    # PETS - Other Pets - Fish
    {"id": 101, "name": "Aquarium Setup", "category": "Pets", "subcategory": "Other Pets", "sub_subcategory": "Fish", "price": 5000, "stock": 10, "emoji": "🐠", "description": "Complete aquarium kit", "rating": 4.4, "specs": "Tank: 2ft | Filter included", "image": "assets/aquarium_setup.png"},
    {"id": 102, "name": "Betta Fish", "category": "Pets", "subcategory": "Other Pets", "sub_subcategory": "Fish", "price": 800, "stock": 15, "emoji": "🐠", "description": "Colorful betta fish", "rating": 4.2, "specs": "Colors: Red, Blue, Yellow", "image": "assets/betta_fish.png"},
    
    # PETS - Other Pets - Rabbits
    {"id": 103, "name": "Bunny Rabbit", "category": "Pets", "subcategory": "Other Pets", "sub_subcategory": "Rabbits", "price": 4000, "stock": 5, "emoji": "🐰", "description": "Cute rabbit", "rating": 4.6, "specs": "Age: 3 Months | White/Brown", "image": "assets/bunny_rabbit.png"},
    {"id": 104, "name": "Angora Rabbit", "category": "Pets", "subcategory": "Other Pets", "sub_subcategory": "Rabbits", "price": 6000, "stock": 3, "emoji": "🐰", "description": "Fluffy Angora", "rating": 4.7, "specs": "Age: 4 Months | Long Fur", "image": "assets/angora_rabbit.png"},
    
    # APPLIANCES - Cooling - Air Conditioners
    {"id": 105, "name": "Air Conditioner 1.5 Ton", "category": "Appliances", "subcategory": "Cooling", "sub_subcategory": "Air Conditioners", "price": 55000, "stock": 9, "emoji": "❄️", "description": "DC Inverter AC", "rating": 4.5, "specs": "1.5 Ton | 4 Star Energy", "image": "assets/air_conditioner_1.5ton.png"},
    {"id": 106, "name": "Air Conditioner 2 Ton", "category": "Appliances", "subcategory": "Cooling", "sub_subcategory": "Air Conditioners", "price": 75000, "stock": 7, "emoji": "❄️", "description": "Premium 2 ton AC", "rating": 4.6, "specs": "2 Ton | Wifi Control", "image": "assets/air_conditioner_2ton.png"},
    
    # APPLIANCES - Cooling - Fans
    {"id": 107, "name": "Ceiling Fan", "category": "Appliances", "subcategory": "Cooling", "sub_subcategory": "Fans", "price": 3500, "stock": 20, "emoji": "🌬️", "description": "Modern ceiling fan", "rating": 4.2, "specs": "3 Blade | Speed Control", "image": "assets/ceiling_fan.png"},
    {"id": 108, "name": "Tower Fan", "category": "Appliances", "subcategory": "Cooling", "sub_subcategory": "Fans", "price": 5000, "stock": 15, "emoji": "🌬️", "description": "Space-saving tower fan", "rating": 4.3, "specs": "Oscillating | Remote Control", "image": "assets/tower_fan.png"},
    
    # APPLIANCES - Cooling - Air Coolers
    {"id": 109, "name": "Desert Cooler", "category": "Appliances", "subcategory": "Cooling", "sub_subcategory": "Air Coolers", "price": 12000, "stock": 8, "emoji": "❄️", "description": "Evaporative air cooler", "rating": 4.1, "specs": "Capacity: 50L | Eco-friendly", "image": "assets/desert_cooler.png"},
    {"id": 110, "name": "Portable Air Cooler", "category": "Appliances", "subcategory": "Cooling", "sub_subcategory": "Air Coolers", "price": 8000, "stock": 10, "emoji": "❄️", "description": "Portable cooling unit", "rating": 4.2, "specs": "Mobile | Energy Efficient", "image": "assets/portable_cooler.png"},
    
    # APPLIANCES - Cooling - Refrigerators
    {"id": 111, "name": "Refrigerator (Haier)", "category": "Appliances", "subcategory": "Cooling", "sub_subcategory": "Refrigerators", "price": 42000, "stock": 8, "emoji": "🧊", "description": "Digital Inverter fridge", "rating": 4.6, "specs": "15 Cu Ft | 10 Yr Warranty", "image": "assets/refrigerator_haier.png"},
    {"id": 112, "name": "Refrigerator (Dawlance)", "category": "Appliances", "subcategory": "Cooling", "sub_subcategory": "Refrigerators", "price": 48000, "stock": 6, "emoji": "🧊", "description": "Premium refrigerator", "rating": 4.7, "specs": "18 Cu Ft | NoFrost", "image": "assets/refrigerator_dawlance.png"},
    
    # APPLIANCES - Kitchen - Microwaves
    {"id": 113, "name": "Microwave Oven (Dawlance)", "category": "Appliances", "subcategory": "Kitchen", "sub_subcategory": "Microwaves", "price": 14000, "stock": 11, "emoji": "🍳", "description": "Solo microwave oven", "rating": 4.2, "specs": "20L | 700W | 5 Power Levels", "image": "assets/microwave_dawlance.png"},
    {"id": 114, "name": "Microwave Convection", "category": "Appliances", "subcategory": "Kitchen", "sub_subcategory": "Microwaves", "price": 22000, "stock": 8, "emoji": "🍳", "description": "Convection microwave", "rating": 4.4, "specs": "30L | 1000W | Multi-function", "image": "assets/microwave_convection.png"},
    
    # APPLIANCES - Kitchen - Blenders
    {"id": 115, "name": "Blender (Anex)", "category": "Appliances", "subcategory": "Kitchen", "sub_subcategory": "Blenders", "price": 3500, "stock": 18, "emoji": "🥤", "description": "3-in-1 blender", "rating": 4.1, "specs": "500W | 1.5L Jar", "image": "assets/blender_anex.png"},
    {"id": 116, "name": "High-Power Blender", "category": "Appliances", "subcategory": "Kitchen", "sub_subcategory": "Blenders", "price": 6500, "stock": 12, "emoji": "🥤", "description": "Professional blender", "rating": 4.5, "specs": "1000W | Multiple Functions", "image": "assets/blender_professional.png"},
    
    # APPLIANCES - Kitchen - Dishwashers
    {"id": 117, "name": "Dishwasher (IKEA)", "category": "Appliances", "subcategory": "Kitchen", "sub_subcategory": "Dishwashers", "price": 35000, "stock": 5, "emoji": "🍽️", "description": "Automatic dishwasher", "rating": 4.3, "specs": "Energy Efficient | 12 Place", "image": "assets/dishwasher_ikea.png"},
    {"id": 118, "name": "Premium Dishwasher", "category": "Appliances", "subcategory": "Kitchen", "sub_subcategory": "Dishwashers", "price": 45000, "stock": 4, "emoji": "🍽️", "description": "Premium dishwasher", "rating": 4.6, "specs": "Stainless Steel | Quiet", "image": "assets/dishwasher_premium.png"},
    
    # APPLIANCES - Kitchen - Ovens
    {"id": 119, "name": "Electric Oven", "category": "Appliances", "subcategory": "Kitchen", "sub_subcategory": "Ovens", "price": 8000, "stock": 10, "emoji": "🔥", "description": "Compact electric oven", "rating": 4.2, "specs": "45L | 2000W | Timer", "image": "assets/electric_oven.png"},
    {"id": 120, "name": "Convection Oven", "category": "Appliances", "subcategory": "Kitchen", "sub_subcategory": "Ovens", "price": 16000, "stock": 7, "emoji": "🔥", "description": "Convection baking oven", "rating": 4.5, "specs": "60L | Multi-function | Rotisserie", "image": "assets/convection_oven.png"},
    
    # SPORTS - Cricket - Bats
    {"id": 121, "name": "Cricket Bat (English)", "category": "Sports", "subcategory": "Cricket", "sub_subcategory": "Bats", "price": 3500, "stock": 15, "emoji": "🏏", "description": "Grade 1 English Willow", "rating": 4.8, "specs": "Weight: 2.7 lbs | Pre-knocked", "image": "assets/cricket_bat_english.png"},
    {"id": 122, "name": "Cricket Bat (Kashmir)", "category": "Sports", "subcategory": "Cricket", "sub_subcategory": "Bats", "price": 4500, "stock": 10, "emoji": "🏏", "description": "Kashmir willow bat", "rating": 4.6, "specs": "Weight: 2.8 lbs | Training Bat", "image": "assets/cricket_bat_kashmir.png"},
    
    # SPORTS - Cricket - Balls
    {"id": 123, "name": "Cricket Ball (Leather)", "category": "Sports", "subcategory": "Cricket", "sub_subcategory": "Balls", "price": 1200, "stock": 30, "emoji": "⚪", "description": "Premium red leather ball", "rating": 4.6, "specs": "Weight: 156g | Hand-stitched", "image": "assets/cricket_ball_leather.png"},
    {"id": 124, "name": "Cricket Ball (Synthetic)", "category": "Sports", "subcategory": "Cricket", "sub_subcategory": "Balls", "price": 600, "stock": 40, "emoji": "⚪", "description": "Synthetic cricket ball", "rating": 4.3, "specs": "Durable | Practice Ball", "image": "assets/cricket_ball_synthetic.png"},
    
    # SPORTS - Cricket - Protective Gear
    {"id": 125, "name": "Cricket Helmet & Pads Kit", "category": "Sports", "subcategory": "Cricket", "sub_subcategory": "Protective Gear", "price": 4500, "stock": 8, "emoji": "🏏", "description": "Complete protective set", "rating": 4.3, "specs": "Helmet, Pads, Gloves", "image": "assets/cricket_protective_gear.png"},
    {"id": 126, "name": "Batting Gloves", "category": "Sports", "subcategory": "Cricket", "sub_subcategory": "Protective Gear", "price": 2000, "stock": 12, "emoji": "🧤", "description": "Premium batting gloves", "rating": 4.4, "specs": "Leather | Comfortable Grip", "image": "assets/batting_gloves.png"},
    
    # SPORTS - Cricket - Wickets
    {"id": 127, "name": "Cricket Stumps Set", "category": "Sports", "subcategory": "Cricket", "sub_subcategory": "Wickets", "price": 1500, "stock": 20, "emoji": "🏏", "description": "Professional stumps set", "rating": 4.2, "specs": "Complete 3 Stumps | Bails", "image": "assets/cricket_stumps.png"},
    {"id": 128, "name": "Portable Cricket Set", "category": "Sports", "subcategory": "Cricket", "sub_subcategory": "Wickets", "price": 8000, "stock": 10, "emoji": "🏏", "description": "Portable cricket equipment", "rating": 4.3, "specs": "Bat, Ball, Stumps, Bag", "image": "assets/portable_cricket_set.png"},
    
    # SPORTS - Fitness - Treadmills
    {"id": 129, "name": "Treadmill (Motorised)", "category": "Sports", "subcategory": "Fitness", "sub_subcategory": "Treadmills", "price": 28000, "stock": 4, "emoji": "🏃", "description": "Home gym treadmill", "rating": 4.4, "specs": "2.5 HP | Max Weight: 110 kg", "image": "assets/treadmill_motorised.png"},
    {"id": 130, "name": "Foldable Treadmill", "category": "Sports", "subcategory": "Fitness", "sub_subcategory": "Treadmills", "price": 20000, "stock": 6, "emoji": "🏃", "description": "Space-saving treadmill", "rating": 4.3, "specs": "Foldable | Compact | 2 HP", "image": "assets/treadmill_foldable.png"},
    
    # SPORTS - Fitness - Dumbbells
    {"id": 131, "name": "Adjustable Dumbbells (20kg)", "category": "Sports", "subcategory": "Fitness", "sub_subcategory": "Dumbbells", "price": 5500, "stock": 12, "emoji": "🏋️", "description": "20kg dumbbell set", "rating": 4.5, "specs": "Cast Iron | Rubber Grip", "image": "assets/dumbbells_20kg.png"},
    {"id": 132, "name": "Heavy Dumbbell Set", "category": "Sports", "subcategory": "Fitness", "sub_subcategory": "Dumbbells", "price": 12000, "stock": 8, "emoji": "🏋️", "description": "Complete dumbbell set", "rating": 4.6, "specs": "5kg to 25kg | Professional", "image": "assets/dumbbell_set_heavy.png"},
    
    # SPORTS - Fitness - Yoga Mats
    {"id": 133, "name": "Yoga Mat Standard", "category": "Sports", "subcategory": "Fitness", "sub_subcategory": "Yoga Mats", "price": 2500, "stock": 20, "emoji": "🧘", "description": "Comfortable yoga mat", "rating": 4.2, "specs": "6mm Thick | Non-slip", "image": "assets/yoga_mat_standard.png"},
    {"id": 134, "name": "Premium Yoga Mat", "category": "Sports", "subcategory": "Fitness", "sub_subcategory": "Yoga Mats", "price": 4500, "stock": 15, "emoji": "🧘", "description": "Premium quality mat", "rating": 4.5, "specs": "8mm Thick | Eco-friendly", "image": "assets/yoga_mat_premium.png"},
    
    # SPORTS - Fitness - Resistance Bands
    {"id": 135, "name": "Resistance Band Set", "category": "Sports", "subcategory": "Fitness", "sub_subcategory": "Resistance Bands", "price": 3000, "stock": 25, "emoji": "💪", "description": "Complete band set", "rating": 4.3, "specs": "5 Levels | Multiple Colors", "image": "assets/resistance_bands.png"},
    {"id": 136, "name": "Power Loop Bands", "category": "Sports", "subcategory": "Fitness", "sub_subcategory": "Resistance Bands", "price": 1500, "stock": 30, "emoji": "💪", "description": "Loop resistance bands", "rating": 4.2, "specs": "Heavy Resistance | Durable", "image": "assets/power_loop_bands.png"},
]

def hash_pw(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_db():
    db = {"users": {}, "orders": [], "products": PRODUCTS}
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            try:
                loaded = json.load(f)
                for username in loaded.get("users", {}):
                    if "pw" in loaded["users"][username]:
                        loaded["users"][username]["password"] = loaded["users"][username]["pw"]
                        del loaded["users"][username]["pw"]
                db.update(loaded)
            except:
                pass
    return db

def save_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)

# ═════════════════════════════════════════════
#  MAIN APPLICATION CLASS
# ═════════════════════════════════════════════
class MartApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ali's Mart 🛒")
        self.geometry("480x580")
        self.config(bg=BG)
        
        self.db = load_db()
        try:
            self._ensure_assets()
        except Exception:
            pass
        
        self.current_user = None
        self.cart = []
        self.image_cache = {}
        
        self._show_login()

    def _ensure_assets(self):
        """Create assets folder and placeholder images"""
        assets_dir = os.path.join(os.getcwd(), "assets")
        os.makedirs(assets_dir, exist_ok=True)
        
        for cat, info in CATEGORIES_DATA.items():
            img_path = info.get("cover_image")
            if img_path:
                full_path = os.path.join(os.getcwd(), img_path)
                if not os.path.exists(full_path):
                    try:
                        w, h = 560, 320
                        img = Image.new("RGBA", (w, h), info.get("color", "#333333"))
                        draw = ImageDraw.Draw(img)
                        try:
                            fnt = ImageFont.truetype("seguiemj.ttf", 120)
                        except:
                            fnt = ImageFont.load_default()
                        emoji = info.get("emoji", "📁")
                        draw.text((20, 20), emoji, font=fnt, fill=(255,255,255,255))
                        os.makedirs(os.path.dirname(full_path), exist_ok=True)
                        img.save(full_path)
                    except:
                        pass
        
        for p in self.db.get("products", []):
            img_path = p.get("image")
            if img_path:
                full_path = os.path.join(os.getcwd(), img_path)
                if not os.path.exists(full_path):
                    try:
                        w, h = 300, 180
                        img = Image.new("RGBA", (w, h), "#2b2b3a")
                        draw = ImageDraw.Draw(img)
                        try:
                            fnt = ImageFont.truetype("seguiemj.ttf", 60)
                        except:
                            fnt = ImageFont.load_default()
                        emoji = p.get("emoji", "📦")
                        draw.text((10, 10), emoji, font=fnt, fill=(255,255,255,255))
                        os.makedirs(os.path.dirname(full_path), exist_ok=True)
                        img.save(full_path)
                    except:
                        pass

    def _clear(self):
        """Clear all widgets"""
        for widget in self.winfo_children():
            widget.destroy()

    def _ask_order_info(self):
        """Ask customer info and save for next time"""
        dialog = tk.Toplevel(self)
        dialog.title("Customer Information")
        dialog.config(bg=BG)
        dialog.geometry("420x320")
        dialog.transient(self)
        dialog.grab_set()
        
        tk.Label(dialog, text="Enter delivery details", font=("Segoe UI", 12, "bold"), bg=BG, fg=WHITE).pack(pady=(12,6))
        
        frm = tk.Frame(dialog, bg=BG)
        frm.pack(fill="both", expand=True, padx=12)
        
        tk.Label(frm, text="Mobile:", font=("Segoe UI", 10), bg=BG, fg=TEXT).pack(anchor="w", pady=(6,0))
        mobile_entry = tk.Entry(frm, font=("Segoe UI", 11), bg=ENTRY_BG, fg=WHITE, bd=0)
        mobile_entry.pack(fill="x", ipady=6)
        
        saved_info = {}
        if self.current_user and self.db.get("users", {}).get(self.current_user, {}).get("customer_info"):
            saved_info = self.db["users"][self.current_user]["customer_info"]
        if saved_info.get("mobile"):
            mobile_entry.insert(0, saved_info.get("mobile"))
        
        tk.Label(frm, text="Payment Method:", font=("Segoe UI", 10), bg=BG, fg=TEXT).pack(anchor="w", pady=(8,0))
        payment_cb = ttk.Combobox(frm, values=["Cash on Delivery", "Bank Transfer", "JazzCash/EasyPaisa", "Credit Card"], state="readonly")
        payment_cb.current(0)
        payment_cb.pack(fill="x", ipady=6)
        if saved_info.get("payment_method"):
            try:
                payment_cb.set(saved_info.get("payment_method"))
            except:
                pass
        
        tk.Label(frm, text="Address:", font=("Segoe UI", 10), bg=BG, fg=TEXT).pack(anchor="w", pady=(8,0))
        address_txt = tk.Text(frm, height=6, bg=ENTRY_BG, fg=WHITE, bd=0)
        address_txt.pack(fill="both", expand=True, pady=(4,0))
        if saved_info.get("address"):
            address_txt.insert("1.0", saved_info.get("address"))
        
        result = {}
        save_var = tk.BooleanVar(value=True if saved_info else False)
        chk = tk.Checkbutton(frm, text="Save this info to my account", variable=save_var, bg=BG, fg=WHITE, selectcolor=CARD, activebackground=BG)
        chk.pack(anchor="w", pady=(6,4))
        
        def on_submit():
            mobile = mobile_entry.get().strip()
            payment = payment_cb.get().strip()
            address = address_txt.get("1.0", "end").strip()
            if not mobile or not address:
                messagebox.showerror("Error", "Please provide mobile and address.")
                return
            result['mobile'] = mobile
            result['payment_method'] = payment
            result['address'] = address
            
            if save_var.get() and self.current_user:
                self.db.setdefault("users", {}).setdefault(self.current_user, {})
                self.db["users"][self.current_user]["customer_info"] = {
                    "mobile": mobile,
                    "payment_method": payment,
                    "address": address
                }
                save_db(self.db)
            dialog.destroy()
        
        def on_cancel():
            dialog.destroy()
        
        btn_fr = tk.Frame(dialog, bg=BG)
        btn_fr.pack(fill="x", pady=8, padx=12)
        tk.Button(btn_fr, text="Cancel", font=("Segoe UI", 10), bg=CARD2, fg=WHITE, bd=0, command=on_cancel).pack(side="right", padx=(6,0))
        tk.Button(btn_fr, text="Submit", font=("Segoe UI", 10, "bold"), bg=GREEN, fg=WHITE, bd=0, command=on_submit).pack(side="right")
        
        self.wait_window(dialog)
        return result if result else None

    def _get_product_image(self, product, size=(100, 80)):
        """Load product image with caching"""
        cache_key = f"prod_{product['id']}"
        if cache_key in self.image_cache:
            return self.image_cache[cache_key]
        
        img_path = product.get("image", "")
        if img_path and os.path.exists(img_path):
            try:
                img = Image.open(img_path).resize(size, Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.image_cache[cache_key] = photo
                return photo
            except:
                pass
        return None

    # ══════════════════════════════════════════
    #  LOGIN / REGISTER
    # ══════════════════════════════════════════
    def _show_login(self):
        self._clear()
        self.geometry("480x580")
        
        outer = tk.Frame(self, bg=BG)
        outer.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(outer, text="🛒", font=("Segoe UI Emoji", 48), bg=BG, fg=ACCENT).pack(pady=(0, 4))
        tk.Label(outer, text="Ali's Mart", font=("Segoe UI", 26, "bold"), bg=BG, fg=WHITE).pack()
        tk.Label(outer, text="Pakistan's Premium Online Marketplace", font=("Segoe UI", 9), bg=BG, fg=SUBTEXT).pack(pady=(2, 20))
        
        self.card = tk.Frame(outer, bg=CARD, padx=32, pady=28)
        self.card.pack(ipadx=10, ipady=4)
        
        self._render_login_fields()

    def _render_login_fields(self):
        """Render login form"""
        for w in self.card.winfo_children():
            w.destroy()
        
        tk.Label(self.card, text="Username", font=("Segoe UI", 11), bg=CARD, fg=TEXT).pack(anchor="w", pady=(0, 4))
        self.username_entry = tk.Entry(self.card, font=("Segoe UI", 12), bg=ENTRY_BG, fg=WHITE, insertbackground=WHITE, bd=0)
        self.username_entry.pack(fill="x", ipady=8, pady=(0, 15))
        
        tk.Label(self.card, text="Password", font=("Segoe UI", 11), bg=CARD, fg=TEXT).pack(anchor="w", pady=(0, 4))
        self.password_entry = tk.Entry(self.card, font=("Segoe UI", 12), show="*", bg=ENTRY_BG, fg=WHITE, insertbackground=WHITE, bd=0)
        self.password_entry.pack(fill="x", ipady=8, pady=(0, 20))
        
        btn_login = tk.Button(self.card, text="LOGIN", font=("Segoe UI", 12, "bold"), bg=ACCENT, fg=WHITE, bd=0, cursor="hand2", command=self._handle_login)
        btn_login.pack(fill="x", ipady=8, pady=(0, 10))
        
        btn_reg_switch = tk.Button(self.card, text="Don't have an account? Register here", font=("Segoe UI", 9, "underline"), bg=CARD, fg=GREEN, bd=0, cursor="hand2", command=self._render_register_fields)
        btn_reg_switch.pack(pady=(5, 0))

    def _render_register_fields(self):
        """Render register form"""
        for w in self.card.winfo_children():
            w.destroy()
        
        tk.Label(self.card, text="Choose Username", font=("Segoe UI", 11), bg=CARD, fg=TEXT).pack(anchor="w", pady=(0, 4))
        self.username_entry = tk.Entry(self.card, font=("Segoe UI", 12), bg=ENTRY_BG, fg=WHITE, insertbackground=WHITE, bd=0)
        self.username_entry.pack(fill="x", ipady=8, pady=(0, 15))
        
        tk.Label(self.card, text="Choose Password", font=("Segoe UI", 11), bg=CARD, fg=TEXT).pack(anchor="w", pady=(0, 4))
        self.password_entry = tk.Entry(self.card, font=("Segoe UI", 12), show="*", bg=ENTRY_BG, fg=WHITE, insertbackground=WHITE, bd=0)
        self.password_entry.pack(fill="x", ipady=8, pady=(0, 20))
        
        btn_register = tk.Button(self.card, text="REGISTER NOW", font=("Segoe UI", 12, "bold"), bg=GREEN, fg=WHITE, bd=0, cursor="hand2", command=self._handle_register)
        btn_register.pack(fill="x", ipady=8, pady=(0, 10))
        
        btn_login_switch = tk.Button(self.card, text="Already have an account? Login", font=("Segoe UI", 9, "underline"), bg=CARD, fg=ACCENT, bd=0, cursor="hand2", command=self._render_login_fields)
        btn_login_switch.pack(pady=(5, 0))

    def _handle_login(self):
        """Handle login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill all fields!")
            return
        
        users = self.db.get("users", {})
        if username in users:
            stored_hash = users[username].get("password", users[username].get("pw", ""))
            if stored_hash == hash_pw(password):
                self.current_user = username
                messagebox.showinfo("Success", f"Welcome back, {username}!")
                self._show_dashboard()
                return
        
        messagebox.showerror("Error", "Invalid username or password!")

    def _handle_register(self):
        """Handle register"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill all fields!")
            return
        
        if username in self.db["users"]:
            messagebox.showerror("Error", "Username already exists!")
            return
        
        self.db["users"][username] = {
            "password": hash_pw(password),
            "joined": str(datetime.date.today())
        }
        save_db(self.db)
        messagebox.showinfo("Success", "Registration successful! Please login.")
        self._render_login_fields()

    # ══════════════════════════════════════════
    #  MAIN DASHBOARD
    # ══════════════════════════════════════════
    def _show_dashboard(self):
        """Show main dashboard"""
        self._clear()
        self.geometry("1280x750")
        
        navbar = tk.Frame(self, bg="#12122a", height=72)
        navbar.pack(fill="x", side="top")
        navbar.pack_propagate(False)
        
        brand_frame = tk.Frame(navbar, bg="#12122a")
        brand_frame.pack(side="left", padx=18, pady=10)
        tk.Label(brand_frame, text="🛒", font=("Segoe UI Emoji", 20), bg="#12122a", fg=ACCENT).pack(side="left")
        tk.Label(brand_frame, text=" Ali's Mart", font=("Segoe UI", 18, "bold"), bg="#12122a", fg=WHITE).pack(side="left")
        
        btn_logout = tk.Button(navbar, text="🚪 Logout", font=("Segoe UI", 10, "bold"), bg=ACCENT, fg=WHITE, bd=0, padx=14, cursor="hand2", activebackground="#cc4444", command=self._show_login)
        btn_logout.pack(side="right", padx=10, pady=18)

        # Sell product button for customers to upload products
        btn_sell = tk.Button(navbar, text="➕ Sell", font=("Segoe UI", 10, "bold"), bg="#2a6f4d", fg=WHITE, bd=0, padx=12, cursor="hand2", activebackground="#3aa56a", command=self._open_sell_dialog)
        btn_sell.pack(side="right", padx=6, pady=18)

        btn_orders = tk.Button(navbar, text="📦 Orders", font=("Segoe UI", 10, "bold"), bg="#1e3a5f", fg=CYAN, bd=0, padx=14, cursor="hand2", activebackground="#2a4f7a", command=lambda: self._show_orders_view())
        btn_orders.pack(side="right", padx=6, pady=18)

        tk.Label(navbar, text=f"✨ {self.current_user}", font=("Segoe UI", 11, "bold"), bg="#12122a", fg=GOLD).pack(side="right", padx=16, pady=18)
        
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True)
        
        self._show_categories_view(body)

    def _show_categories_view(self, parent):
        """Display all categories"""
        for w in parent.winfo_children():
            w.destroy()
        
        banner = tk.Frame(parent, bg="#12122a", height=80)
        banner.pack(fill="x")
        banner.pack_propagate(False)
        hf = tk.Frame(banner, bg="#12122a")
        hf.pack(side="left", padx=24, pady=16)
        tk.Label(hf, text="🏪 Browse Categories", font=("Segoe UI", 22, "bold"), bg="#12122a", fg=WHITE).pack(anchor="w")
        tk.Label(hf, text="Pick a category and explore thousands of products", font=("Segoe UI", 10), bg="#12122a", fg=SUBTEXT).pack(anchor="w")
        
        canvas = tk.Canvas(parent, bg=BG, bd=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=BG)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        for idx, (cat_name, cat_info) in enumerate(CATEGORIES_DATA.items()):
            if idx % 2 == 0:
                row_frame = tk.Frame(scrollable_frame, bg=BG)
                row_frame.pack(fill="x", padx=18, pady=10)
            
            palette = CARD_COLORS[idx % len(CARD_COLORS)]
            card_bg = palette["bg"]
            acc_col = palette["accent"]
            btn_col = palette["btn"]
            
            border = tk.Frame(row_frame, bg=acc_col, padx=3)
            border.pack(side="left", fill="both", expand=True, padx=8)
            
            card = tk.Frame(border, bg=card_bg, padx=16, pady=16)
            card.pack(fill="both", expand=True)
            
            top_strip = tk.Frame(card, bg=acc_col, height=4)
            top_strip.pack(fill="x", pady=(0, 12))
            
            name_row = tk.Frame(card, bg=card_bg)
            name_row.pack(fill="x", pady=(0, 6))
            # Show category cover image if available, otherwise fallback to emoji
            img_path = cat_info.get("cover_image")
            if img_path and os.path.exists(img_path):
                try:
                    cat_img = Image.open(img_path).resize((56, 56), Image.Resampling.LANCZOS)
                    cat_photo = ImageTk.PhotoImage(cat_img)
                    self.image_cache[f"cat_{cat_name}"] = cat_photo
                    tk.Label(name_row, image=cat_photo, bg=card_bg).pack(side="left")
                except:
                    tk.Label(name_row, text=cat_info["emoji"], font=("Segoe UI Emoji", 32), bg=card_bg, fg=acc_col).pack(side="left")
            else:
                tk.Label(name_row, text=cat_info["emoji"], font=("Segoe UI Emoji", 32), bg=card_bg, fg=acc_col).pack(side="left")
            title_col = tk.Frame(name_row, bg=card_bg)
            title_col.pack(side="left", padx=10)
            tk.Label(title_col, text=cat_name, font=("Segoe UI", 14, "bold"), bg=card_bg, fg=WHITE).pack(anchor="w")
            tk.Label(title_col, text=cat_info["description"], font=("Segoe UI", 9), bg=card_bg, fg=SUBTEXT, wraplength=240, justify="left").pack(anchor="w")
            
            chips_frame = tk.Frame(card, bg=card_bg)
            chips_frame.pack(fill="x", pady=(8, 12))
            subcats = list(cat_info["subcategories"].keys())
            for sc in subcats[:3]:
                sc_info = cat_info["subcategories"][sc]
                chip = tk.Label(chips_frame, text=f"  {sc_info['emoji']} {sc}  ", font=("Segoe UI", 8, "bold"), bg=acc_col, fg=WHITE, padx=4, pady=2, relief="flat")
                chip.pack(side="left", padx=3, pady=2)
            if len(subcats) > 3:
                tk.Label(chips_frame, text=f"+{len(subcats)-3} more", font=("Segoe UI", 8), bg=card_bg, fg=acc_col).pack(side="left", padx=4)
            
            btn = tk.Button(card, text=f"Explore {cat_name}  →", font=("Segoe UI", 10, "bold"), bg=btn_col, fg=WHITE, bd=0, cursor="hand2", activebackground=acc_col, command=lambda c=cat_name: self._show_subcategories_view(c))
            btn.pack(fill="x", ipady=9)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _show_subcategories_view(self, category):
        """Display subcategories for selected category"""
        main_frame = self.winfo_children()[-1]
        for w in main_frame.winfo_children():
            w.destroy()
        
        cat_info = CATEGORIES_DATA[category]
        cat_color = cat_info.get("color", ACCENT)
        
        header = tk.Frame(main_frame, bg="#12122a", height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        hrow = tk.Frame(header, bg="#12122a")
        hrow.pack(side="left", padx=20, pady=12)
        btn_back = tk.Button(hrow, text="← Back", font=("Segoe UI", 10), bg="#1e1e35", fg=cat_color, bd=0, padx=10, cursor="hand2", command=lambda: self._show_categories_view(main_frame))
        btn_back.pack(side="left", padx=(0, 14))
        tk.Label(hrow, text=cat_info["emoji"], font=("Segoe UI Emoji", 20), bg="#12122a", fg=cat_color).pack(side="left")
        tk.Label(hrow, text=f" {category} — Choose Subcategory", font=("Segoe UI", 16, "bold"), bg="#12122a", fg=WHITE).pack(side="left")
        
        canvas = tk.Canvas(main_frame, bg=BG, bd=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        sf = tk.Frame(canvas, bg=BG)
        sf.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=sf, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        subcats = cat_info["subcategories"]
        sc_colors = ["#FF6B6B","#00d2ff","#39d98a","#FF8C42","#9b59b6","#f72585","#3A86FF","#43b89c"]
        
        for i, (subcat, sc_info) in enumerate(subcats.items()):
            sc_color = sc_info.get("color", sc_colors[i % len(sc_colors)])
            sc_emoji = sc_info.get("emoji", "📂")
            sub_subs = sc_info.get("sub_subcategories", [])
            
            card = tk.Frame(sf, bg="#1a1a2e", padx=16, pady=14)
            card.pack(fill="x", padx=30, pady=8)
            
            top_strip = tk.Frame(card, bg=sc_color, height=3)
            top_strip.pack(fill="x", pady=(0, 10))
            
            top_row = tk.Frame(card, bg="#1a1a2e")
            top_row.pack(fill="x")
            # Try to show category cover image for subcategory icon, fallback to emoji
            sc_img_path = cat_info.get("cover_image")
            if sc_img_path and os.path.exists(sc_img_path):
                try:
                    sc_img = Image.open(sc_img_path).resize((48, 48), Image.Resampling.LANCZOS)
                    sc_photo = ImageTk.PhotoImage(sc_img)
                    self.image_cache[f"subcat_{category}_{subcat}"] = sc_photo
                    tk.Label(top_row, image=sc_photo, bg="#1a1a2e").pack(side="left")
                except:
                    tk.Label(top_row, text=sc_emoji, font=("Segoe UI Emoji", 28), bg="#1a1a2e", fg=sc_color).pack(side="left")
            else:
                tk.Label(top_row, text=sc_emoji, font=("Segoe UI Emoji", 28), bg="#1a1a2e", fg=sc_color).pack(side="left")
            info_col = tk.Frame(top_row, bg="#1a1a2e")
            info_col.pack(side="left", padx=12)
            tk.Label(info_col, text=subcat, font=("Segoe UI", 13, "bold"), bg="#1a1a2e", fg=WHITE).pack(anchor="w")
            tk.Label(info_col, text=f"{len(sub_subs)} sub-subcategories", font=("Segoe UI", 9), bg="#1a1a2e", fg=SUBTEXT).pack(anchor="w")
            
            chips = tk.Frame(card, bg="#1a1a2e")
            chips.pack(fill="x", pady=(8, 10))
            for ss in sub_subs[:4]:
                chip = tk.Label(chips, text=f" {ss} ", font=("Segoe UI", 8), bg="#2a2a45", fg=sc_color, padx=4, pady=2)
                chip.pack(side="left", padx=3, pady=2)
            
            btn = tk.Button(card, text=f"View Sub-Subcategories →", font=("Segoe UI", 10, "bold"), bg=sc_color, fg=WHITE, bd=0, cursor="hand2", activebackground=cat_color, command=lambda c=category, s=subcat: self._show_sub_subcategories_view(c, s))
            btn.pack(fill="x", ipady=8)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _show_sub_subcategories_view(self, category, subcategory):
        """Display sub-subcategories for a subcategory"""
        main_frame = self.winfo_children()[-1]
        for w in main_frame.winfo_children():
            w.destroy()
        
        cat_info = CATEGORIES_DATA[category]
        sc_info = cat_info["subcategories"][subcategory]
        sc_color = sc_info.get("color", ACCENT)
        sc_emoji = sc_info.get("emoji", "📂")
        sub_subs = sc_info.get("sub_subcategories", [])
        
        header = tk.Frame(main_frame, bg="#12122a", height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        hrow = tk.Frame(header, bg="#12122a")
        hrow.pack(side="left", padx=20, pady=12)
        btn_back = tk.Button(hrow, text="← Back", font=("Segoe UI", 10), bg="#1e1e35", fg=sc_color, bd=0, padx=10, cursor="hand2", command=lambda: self._show_subcategories_view(category))
        btn_back.pack(side="left", padx=(0, 14))
        tk.Label(hrow, text=sc_emoji, font=("Segoe UI Emoji", 20), bg="#12122a", fg=sc_color).pack(side="left")
        tk.Label(hrow, text=f" {category}  ›  {subcategory} — Select Type", font=("Segoe UI", 15, "bold"), bg="#12122a", fg=WHITE).pack(side="left")
        
        canvas = tk.Canvas(main_frame, bg=BG, bd=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        sf = tk.Frame(canvas, bg=BG)
        sf.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=sf, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        sub_colors = ["#ff6b6b","#00d2ff","#39d98a","#FF8C42","#9b59b6","#f72585","#3A86FF","#43b89c"]
        
        for i, ss_name in enumerate(sub_subs):
            ss_color = sub_colors[i % len(sub_colors)]
            card = tk.Frame(sf, bg="#1a1a2e", padx=16, pady=14)
            card.pack(fill="x", padx=30, pady=8)
            
            strip = tk.Frame(card, bg=ss_color, height=3)
            strip.pack(fill="x", pady=(0, 10))
            
            row = tk.Frame(card, bg="#1a1a2e")
            row.pack(fill="x")
            tk.Label(row, text="📁", font=("Segoe UI Emoji", 24), bg="#1a1a2e", fg=ss_color).pack(side="left")
            info = tk.Frame(row, bg="#1a1a2e")
            info.pack(side="left", padx=12)
            tk.Label(info, text=ss_name, font=("Segoe UI", 12, "bold"), bg="#1a1a2e", fg=WHITE).pack(anchor="w")
            pcount = sum(1 for p in self.db["products"] if p.get("category") == category and p.get("subcategory") == subcategory and p.get("sub_subcategory", "") == ss_name)
            tk.Label(info, text=f"{pcount} products listed", font=("Segoe UI", 9), bg="#1a1a2e", fg=SUBTEXT).pack(anchor="w")
            
            btn = tk.Button(card, text=f"View Products  →", font=("Segoe UI", 10, "bold"), bg=ss_color, fg=WHITE, bd=0, cursor="hand2", activebackground=sc_color, command=lambda c=category, s=subcategory, ss=ss_name: self._show_products_view(c, s, ss))
            btn.pack(fill="x", ipady=8)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _show_products_view(self, category, subcategory, sub_subcategory=None):
        """Display products for selected sub-subcategory"""
        main_frame = self.winfo_children()[-1]
        for w in main_frame.winfo_children():
            w.destroy()
        
        cat_info = CATEGORIES_DATA.get(category, {})
        sc_info = cat_info.get("subcategories", {}).get(subcategory, {})
        sc_color = sc_info.get("color", ACCENT)
        
        header = tk.Frame(main_frame, bg="#12122a", height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        hrow = tk.Frame(header, bg="#12122a")
        hrow.pack(side="left", padx=20, pady=12)
        btn_back = tk.Button(hrow, text="← Back", font=("Segoe UI", 10), bg="#1e1e35", fg=sc_color, bd=0, padx=10, cursor="hand2", command=lambda: self._show_sub_subcategories_view(category, subcategory))
        btn_back.pack(side="left", padx=(0, 14))
        breadcrumb = f"{category}  ›  {subcategory}"
        if sub_subcategory:
            breadcrumb += f"  ›  {sub_subcategory}"
        tk.Label(hrow, text=breadcrumb, font=("Segoe UI", 14, "bold"), bg="#12122a", fg=WHITE).pack(side="left")
        
        content_frame = tk.Frame(main_frame, bg=BG)
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        filtered_products = [p for p in self.db["products"] if p["category"] == category and p["subcategory"] == subcategory and p.get("sub_subcategory", "") == sub_subcategory]
        
        if not filtered_products:
            empty_frame = tk.Frame(content_frame, bg=BG)
            empty_frame.pack(expand=True)
            tk.Label(empty_frame, text="🛒", font=("Segoe UI Emoji", 48), bg=BG).pack(pady=(40, 10))
            tk.Label(empty_frame, text="No products found here.", font=("Segoe UI", 14, "bold"), bg=BG, fg=SUBTEXT).pack()
            return
        
        canvas = tk.Canvas(content_frame, bg=BG, bd=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=BG)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        p_colors = ["#FF6B6B","#00d2ff","#39d98a","#FF8C42","#9b59b6","#f72585","#3A86FF","#43b89c"]
        
        row = 0
        col = 0
        for pidx, product in enumerate(filtered_products):
            if col == 3:
                col = 0
                row += 1
            pc = p_colors[pidx % len(p_colors)]
            
            p_card = tk.Frame(scrollable_frame, bg="#1a1a2e", padx=12, pady=12)
            p_card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            tk.Frame(p_card, bg=pc, height=4).pack(fill="x", pady=(0, 8))
            
            img = self._get_product_image(product, size=(110, 85))
            if img:
                img_lbl = tk.Label(p_card, image=img, bg="#1a1a2e")
                img_lbl.image = img
                img_lbl.pack(pady=4)
            else:
                tk.Label(p_card, text=product.get("emoji", "📦"), font=("Segoe UI Emoji", 38), bg="#1a1a2e", fg=pc).pack(pady=4)
            
            tk.Label(p_card, text=product["name"], font=("Segoe UI", 10, "bold"), bg="#1a1a2e", fg=WHITE, wraplength=130, justify="center").pack(pady=(4, 2))
            tk.Label(p_card, text=f"Rs. {product['price']:,}", font=("Segoe UI", 12, "bold"), bg="#1a1a2e", fg=GOLD).pack(pady=4)
            
            stars = "★" * int(product.get("rating", 0)) + "☆" * (5 - int(product.get("rating", 0)))
            tk.Label(p_card, text=stars, font=("Segoe UI", 10), bg="#1a1a2e", fg=GOLD).pack()
            
            tk.Label(p_card, text=f"Stock: {product['stock']}", font=("Segoe UI", 8), bg="#1a1a2e", fg=SUBTEXT).pack(pady=2)
            
            btn = tk.Button(p_card, text="🛒 Add to Cart", font=("Segoe UI", 9, "bold"), bg=pc, fg=WHITE, bd=0, cursor="hand2", activebackground=sc_color, command=lambda pid=product["id"]: self._add_to_cart(pid))
            btn.pack(fill="x", ipady=7, pady=(8, 0))
            col += 1
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _show_orders_view(self):
        """Display list of orders"""
        main_frame = self.winfo_children()[1]
        for w in main_frame.winfo_children():
            w.destroy()
        
        header = tk.Frame(main_frame, bg=BG)
        header.pack(fill="x", padx=20, pady=20)
        
        btn_back = tk.Button(header, text="← Back to Categories", font=("Segoe UI", 10), bg=CARD2, fg=ACCENT, bd=0, cursor="hand2", command=lambda: self._show_categories_view(main_frame))
        btn_back.pack(anchor="w")
        
        tk.Label(header, text="Your Orders", font=("Segoe UI", 18, "bold"), bg=BG, fg=WHITE).pack(anchor="w", pady=(10, 0))
        
        content = tk.Frame(main_frame, bg=BG)
        content.pack(fill="both", expand=True, padx=20, pady=10)
        
        orders = self.db.get("orders", [])
        if not orders:
            tk.Label(content, text="No orders placed yet.", font=("Segoe UI", 12), bg=BG, fg=SUBTEXT).pack(pady=40)
            return
        
        canvas = tk.Canvas(content, bg=BG, bd=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(content, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=BG)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for o in reversed(orders):
            oframe = tk.Frame(scrollable_frame, bg=CARD, padx=12, pady=12)
            oframe.pack(fill="x", pady=8)
            
            left = tk.Frame(oframe, bg=CARD)
            left.pack(side="left", fill="both", expand=True)
            tk.Label(left, text=f"Order #{o['order_id'][:8]}", font=("Segoe UI", 12, "bold"), bg=CARD, fg=WHITE).pack(anchor="w")
            tk.Label(left, text=f"User: {o.get('user')}", font=("Segoe UI", 9), bg=CARD, fg=SUBTEXT).pack(anchor="w")
            tk.Label(left, text=f"Date: {o.get('date')}", font=("Segoe UI", 9), bg=CARD, fg=SUBTEXT).pack(anchor="w")
            
            right = tk.Frame(oframe, bg=CARD)
            right.pack(side="right")
            tk.Label(right, text=f"Rs. {o.get('total',0):,}", font=("Segoe UI", 12, "bold"), bg=CARD, fg=GOLD).pack()
            tk.Button(right, text="Details", font=("Segoe UI", 9), bg=ACCENT2, fg=WHITE, bd=0, cursor="hand2", command=lambda ord=o: self._show_order_details(ord)).pack(pady=6)
            
            cm = o.get('customer', {})
            if cm:
                tk.Label(oframe, text=f"{cm.get('mobile','')} • {cm.get('payment_method','')}", font=("Segoe UI", 9), bg=CARD, fg=SUBTEXT).pack(anchor="w", pady=(6,0))
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _show_order_details(self, order):
        """Show order details"""
        detail = tk.Toplevel(self)
        detail.title(f"Order {order['order_id'][:8]}")
        detail.config(bg=BG)
        detail.geometry("400x400")
        
        tk.Label(detail, text=f"Order #{order['order_id'][:8]}", font=("Segoe UI", 14, "bold"), bg=BG, fg=WHITE).pack(pady=12)
        tk.Label(detail, text=f"Date: {order.get('date')}", font=("Segoe UI", 9), bg=BG, fg=SUBTEXT).pack()
        
        frame = tk.Frame(detail, bg=BG)
        frame.pack(fill="both", expand=True, padx=12, pady=12)
        
        for item in order.get('items', []):
            row = tk.Frame(frame, bg=BG)
            row.pack(fill="x", pady=6)
            tk.Label(row, text=item.get('name'), font=("Segoe UI", 10), bg=BG, fg=WHITE).pack(side="left", anchor="w")
            tk.Label(row, text=f"Rs. {item.get('price',0):,}", font=("Segoe UI", 10), bg=BG, fg=GOLD).pack(side="right")
        
        tk.Label(detail, text=f"Total: Rs. {order.get('total',0):,}", font=("Segoe UI", 12, "bold"), bg=BG, fg=GOLD).pack(pady=12)
        
        cust = order.get('customer', {})
        if cust:
            info_frame = tk.Frame(detail, bg=BG)
            info_frame.pack(fill="x", padx=12, pady=(4,12))
            tk.Label(info_frame, text="Customer Information", font=("Segoe UI", 11, "bold"), bg=BG, fg=WHITE).pack(anchor="w")
            tk.Label(info_frame, text=f"Mobile: {cust.get('mobile','')}", font=("Segoe UI", 9), bg=BG, fg=SUBTEXT).pack(anchor="w")
            tk.Label(info_frame, text=f"Payment: {cust.get('payment_method','')}", font=("Segoe UI", 9), bg=BG, fg=SUBTEXT).pack(anchor="w")
            tk.Label(info_frame, text=f"Address:", font=("Segoe UI", 9), bg=BG, fg=SUBTEXT).pack(anchor="w")
            addr = tk.Label(info_frame, text=cust.get('address',''), font=("Segoe UI", 9), bg=BG, fg=WHITE, wraplength=360, justify="left")
            addr.pack(anchor="w")

    def _ask_quantity(self, product):
        """Ask for quantity"""
        stock = product.get("stock", 0)
        if stock == 0:
            messagebox.showerror("Out of Stock", f"{product['name']} is currently out of stock!")
            return 0
        
        dialog = tk.Toplevel(self)
        dialog.title("Select Quantity")
        dialog.config(bg="#0d0d1a")
        dialog.geometry("380x320")
        dialog.transient(self)
        dialog.grab_set()
        
        result = {"qty": 0}
        
        hdr = tk.Frame(dialog, bg=ACCENT, height=6)
        hdr.pack(fill="x")
        
        tk.Label(dialog, text="🛒 Select Quantity", font=("Segoe UI", 14, "bold"), bg="#0d0d1a", fg=WHITE).pack(pady=(16, 4))
        tk.Label(dialog, text=product["name"], font=("Segoe UI", 11), bg="#0d0d1a", fg="#00d2ff", wraplength=320, justify="center").pack(pady=(0, 4))
        tk.Label(dialog, text=f"Rs. {product['price']:,} per item", font=("Segoe UI", 10, "bold"), bg="#0d0d1a", fg=GOLD).pack(pady=(0, 6))
        tk.Label(dialog, text=f"Available Stock: {stock} items", font=("Segoe UI", 9), bg="#0d0d1a", fg="#9999aa").pack()
        
        qty_frame = tk.Frame(dialog, bg="#0d0d1a")
        qty_frame.pack(pady=18)
        
        qty_var = tk.IntVar(value=1)
        
        def decr():
            if qty_var.get() > 1:
                qty_var.set(qty_var.get() - 1)
            update_total()
        
        def incr():
            if qty_var.get() < stock:
                qty_var.set(qty_var.get() + 1)
            update_total()
        
        def update_total():
            try:
                q = qty_var.get()
                total_lbl.config(text=f"Total: Rs. {product['price'] * q:,}")
            except:
                pass
        
        tk.Button(qty_frame, text=" − ", font=("Segoe UI", 14, "bold"), bg="#ff6b6b", fg=WHITE, bd=0, cursor="hand2", command=decr).pack(side="left", padx=8, ipady=4, ipadx=4)
        
        qty_entry = tk.Entry(qty_frame, textvariable=qty_var, font=("Segoe UI", 16, "bold"), width=4, justify="center", bg="#1e1e35", fg=WHITE, insertbackground=WHITE, bd=0)
        qty_entry.pack(side="left", ipady=6)
        qty_entry.bind("<KeyRelease>", lambda e: update_total())
        
        tk.Button(qty_frame, text=" + ", font=("Segoe UI", 14, "bold"), bg="#39d98a", fg=WHITE, bd=0, cursor="hand2", command=incr).pack(side="left", padx=8, ipady=4, ipadx=4)
        
        total_lbl = tk.Label(dialog, text=f"Total: Rs. {product['price']:,}", font=("Segoe UI", 12, "bold"), bg="#0d0d1a", fg=GOLD)
        total_lbl.pack(pady=(0, 16))
        
        def on_confirm():
            try:
                q = int(qty_var.get())
            except:
                q = 0
            if q < 1:
                messagebox.showerror("Invalid", "Please enter at least 1.", parent=dialog)
                return
            if q > stock:
                messagebox.showerror("Exceeds Stock", f"Only {stock} items available!", parent=dialog)
                return
            result["qty"] = q
            dialog.destroy()
        
        def on_cancel():
            result["qty"] = 0
            dialog.destroy()
        
        btn_row = tk.Frame(dialog, bg="#0d0d1a")
        btn_row.pack(fill="x", padx=24, pady=(0, 16))
        tk.Button(btn_row, text="Cancel", font=("Segoe UI", 10), bg="#1e1e35", fg=WHITE, bd=0, padx=14, cursor="hand2", command=on_cancel).pack(side="right", padx=(8, 0), ipady=6)
        tk.Button(btn_row, text="✅ Add to Cart", font=("Segoe UI", 10, "bold"), bg=GREEN, fg=WHITE, bd=0, padx=14, cursor="hand2", command=on_confirm).pack(side="right", ipady=6)
        
        self.wait_window(dialog)
        return result["qty"]

    def _add_to_cart(self, product_id):
        """Add product to cart"""
        product = next((p for p in self.db["products"] if p["id"] == product_id), None)
        if not product:
            return
        
        qty = self._ask_quantity(product)
        if qty <= 0:
            return
        
        for _ in range(qty):
            self.cart.append(product)
        
        total_item = product["price"] * qty
        placed_now = messagebox.askyesno(
            "Added to Cart 🛒",
            f"✅ {qty}x {product['name']} added to cart!\nItem Total: Rs. {total_item:,}\nCart Total: Rs. {sum(p.get('price',0) for p in self.cart):,}\n\nPlace order now?"
        )
        if placed_now:
            self._place_order()

    def _place_order(self):
        """Place order and save to DB"""
        if not self.cart:
            messagebox.showwarning("No items", "Your cart is empty.")
            return
        
        info = self._ask_order_info()
        if info is None:
            return
        
        total = sum(item.get("price", 0) for item in self.cart)
        confirm = messagebox.askyesno(
            "Confirm Order",
            f"Place order for {len(self.cart)} item(s)\nTotal: Rs. {total:,}\n\nProceed?"
        )
        if not confirm:
            return
        
        from collections import Counter
        qty_map = Counter(item.get("id") for item in self.cart)
        for prod_id, qty in qty_map.items():
            prod = next((p for p in self.db.get("products", []) if p.get("id") == prod_id), None)
            if prod and isinstance(prod.get("stock"), int):
                prod["stock"] = max(0, prod["stock"] - qty)
        
        order = {
            "order_id": str(uuid.uuid4()),
            "user": self.current_user or "guest",
            "items": [
                {"id": i.get("id"), "name": i.get("name"), "price": i.get("price"), "qty": qty_map.get(i.get("id"), 1)}
                for i in {item["id"]: item for item in self.cart}.values()
            ],
            "total": total,
            "date": str(datetime.datetime.now()),
            "customer": {
                "address": info.get("address", ""),
                "mobile": info.get("mobile", ""),
                "payment_method": info.get("payment_method", "")
            }
        }
        
        self.db.setdefault("orders", []).append(order)
        save_db(self.db)
        messagebox.showinfo(
            "Order Placed ✅",
            f"Order #{order['order_id'][:8]} placed successfully!\nItems: {len(self.cart)}\nTotal: Rs. {total:,}"
        )
        self.cart = []
        try:
            self._show_orders_view()
        except:
            pass

    def _open_sell_dialog(self):
        """Allow a customer to add/upload a new product"""
        dialog = tk.Toplevel(self)
        dialog.title("Sell a Product")
        dialog.config(bg=BG)
        dialog.geometry("520x560")
        dialog.transient(self)
        dialog.grab_set()

        tk.Label(dialog, text="➕ Sell Your Product", font=("Segoe UI", 14, "bold"), bg=BG, fg=WHITE).pack(pady=(12,6))

        frm = tk.Frame(dialog, bg=BG)
        frm.pack(fill="both", expand=True, padx=12)

        def labeled_entry(label_text, default=""):
            tk.Label(frm, text=label_text, font=("Segoe UI", 10), bg=BG, fg=TEXT).pack(anchor="w", pady=(8,0))
            e = tk.Entry(frm, font=("Segoe UI", 11), bg=ENTRY_BG, fg=WHITE, bd=0)
            e.pack(fill="x", ipady=6)
            if default:
                e.insert(0, default)
            return e

        name_e = labeled_entry("Product Name:")

        # Category selection
        tk.Label(frm, text="Category:", font=("Segoe UI", 10), bg=BG, fg=TEXT).pack(anchor="w", pady=(8,0))
        categories = list(CATEGORIES_DATA.keys())
        cat_cb = ttk.Combobox(frm, values=categories, state="readonly")
        cat_cb.pack(fill="x", ipady=6)
        if categories:
            cat_cb.current(0)

        tk.Label(frm, text="Subcategory:", font=("Segoe UI", 10), bg=BG, fg=TEXT).pack(anchor="w", pady=(8,0))
        subcat_cb = ttk.Combobox(frm, values=[], state="readonly")
        subcat_cb.pack(fill="x", ipady=6)

        tk.Label(frm, text="Type (sub-subcategory):", font=("Segoe UI", 10), bg=BG, fg=TEXT).pack(anchor="w", pady=(8,0))
        ssub_cb = ttk.Combobox(frm, values=[], state="readonly")
        ssub_cb.pack(fill="x", ipady=6)

        def update_subcats(evt=None):
            cat = cat_cb.get()
            subs = list(CATEGORIES_DATA.get(cat, {}).get("subcategories", {}).keys())
            subcat_cb.config(values=subs)
            if subs:
                subcat_cb.current(0)
                update_ssubs()

        def update_ssubs(evt=None):
            cat = cat_cb.get()
            sc = subcat_cb.get()
            ssubs = CATEGORIES_DATA.get(cat, {}).get("subcategories", {}).get(sc, {}).get("sub_subcategories", [])
            ssub_cb.config(values=ssubs)
            if ssubs:
                ssub_cb.current(0)

        cat_cb.bind("<<ComboboxSelected>>", update_subcats)
        subcat_cb.bind("<<ComboboxSelected>>", update_ssubs)
        update_subcats()

        price_e = labeled_entry("Price (Rs):")
        stock_e = labeled_entry("Stock (quantity):", default="1")
        emoji_e = labeled_entry("Emoji (e.g. 📦):", default="📦")

        tk.Label(frm, text="Description:", font=("Segoe UI", 10), bg=BG, fg=TEXT).pack(anchor="w", pady=(8,0))
        desc_txt = tk.Text(frm, height=4, bg=ENTRY_BG, fg=WHITE, bd=0)
        desc_txt.pack(fill="x", pady=(4,0))

        img_path_var = tk.StringVar(value="")
        def choose_image():
            fp = filedialog.askopenfilename(title="Choose product image", filetypes=[("Image files","*.png;*.jpg;*.jpeg;*.gif" )])
            if fp:
                img_path_var.set(fp)
                img_lbl.config(text=os.path.basename(fp))

        tk.Button(frm, text="Choose Image", font=("Segoe UI", 10), bg=CARD2, fg=WHITE, bd=0, cursor="hand2", command=choose_image).pack(pady=(8,4))
        img_lbl = tk.Label(frm, text="No image selected", font=("Segoe UI", 9), bg=BG, fg=SUBTEXT)
        img_lbl.pack()

        def on_submit():
            name = name_e.get().strip()
            cat = cat_cb.get().strip()
            subcat = subcat_cb.get().strip()
            ssub = ssub_cb.get().strip()
            try:
                price = int(price_e.get().strip())
            except:
                messagebox.showerror("Invalid", "Please enter a valid numeric price.")
                return
            try:
                stock = int(stock_e.get().strip())
            except:
                messagebox.showerror("Invalid", "Please enter a valid stock number.")
                return
            emoji = emoji_e.get().strip() or "📦"
            desc = desc_txt.get("1.0", "end").strip()

            if not name or not cat or not subcat:
                messagebox.showerror("Missing", "Please provide product name, category and subcategory.")
                return

            # Prepare image
            final_img_path = ""
            chosen = img_path_var.get()
            if chosen and os.path.exists(chosen):
                ext = os.path.splitext(chosen)[1]
                new_name = f"userprod_{uuid.uuid4().hex[:8]}{ext}"
                dest = os.path.join(os.getcwd(), "assets", new_name)
                try:
                    shutil.copy(chosen, dest)
                    final_img_path = os.path.join("assets", new_name)
                except Exception as e:
                    messagebox.showwarning("Image", f"Could not copy image: {e}")

            # assign new id
            existing = self.db.get("products", [])
            max_id = max((p.get("id", 0) for p in existing), default=0)
            new_id = max_id + 1

            new_prod = {
                "id": new_id,
                "name": name,
                "category": cat,
                "subcategory": subcat,
                "sub_subcategory": ssub,
                "price": price,
                "stock": stock,
                "emoji": emoji,
                "description": desc,
                "rating": 0,
                "specs": "",
                "image": final_img_path or ""
            }

            self.db.setdefault("products", []).append(new_prod)
            save_db(self.db)
            messagebox.showinfo("Success", f"Product '{name}' uploaded successfully!")
            dialog.destroy()

            # refresh products view if currently viewing matching category
            try:
                self._show_products_view(cat, subcat, ssub)
            except:
                pass

        btn_row = tk.Frame(dialog, bg=BG)
        btn_row.pack(fill="x", pady=10, padx=12)
        tk.Button(btn_row, text="Cancel", font=("Segoe UI", 10), bg="#1e1e35", fg=WHITE, bd=0, padx=14, cursor="hand2", command=dialog.destroy).pack(side="right", padx=(8,0))
        tk.Button(btn_row, text="Upload Product", font=("Segoe UI", 10, "bold"), bg=GREEN, fg=WHITE, bd=0, padx=14, cursor="hand2", command=on_submit).pack(side="right")

        self.wait_window(dialog)

if __name__ == "__main__":
    app = MartApp()
    app.mainloop()
