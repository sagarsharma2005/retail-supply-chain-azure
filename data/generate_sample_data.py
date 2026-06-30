"""
Retail Supply Chain Analytics Platform
Sample Data Generator

Generates realistic CSV files for: store_locations, suppliers, products,
inventory, and orders. Uses only Python standard library — no external
dependencies required.

Usage:
    python generate_sample_data.py

Output:
    ./output/store_locations.csv
    ./output/suppliers.csv
    ./output/products.csv
    ./output/inventory.csv
    ./output/orders.csv
"""

import csv
import random
import os
from datetime import datetime, timedelta

random.seed(42)  # reproducible output — same data every run

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# 1. STORE LOCATIONS
# ---------------------------------------------------------------------------
REGIONS = {
    "Northeast": ["New York", "Boston", "Philadelphia"],
    "Southeast": ["Atlanta", "Miami", "Charlotte"],
    "Midwest": ["Chicago", "Detroit", "Minneapolis"],
    "West": ["Los Angeles", "Seattle", "Denver"],
    "South": ["Houston", "Dallas", "Austin"],
}
STATE_BY_CITY = {
    "New York": "NY", "Boston": "MA", "Philadelphia": "PA",
    "Atlanta": "GA", "Miami": "FL", "Charlotte": "NC",
    "Chicago": "IL", "Detroit": "MI", "Minneapolis": "MN",
    "Los Angeles": "CA", "Seattle": "WA", "Denver": "CO",
    "Houston": "TX", "Dallas": "TX", "Austin": "TX",
}

stores = []
store_id_counter = 1
for region, cities in REGIONS.items():
    for city in cities:
        # 1-2 stores per city for variety
        for n in range(random.randint(1, 2)):
            store_id = f"STR-{store_id_counter:04d}"
            stores.append({
                "store_id": store_id,
                "store_name": f"{city} {'Downtown' if n == 0 else 'Mall'} Store",
                "city": city,
                "state": STATE_BY_CITY[city],
                "region": region,
            })
            store_id_counter += 1

with open(f"{OUTPUT_DIR}/store_locations.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["store_id", "store_name", "city", "state", "region"])
    writer.writeheader()
    writer.writerows(stores)

print(f"store_locations.csv  -> {len(stores)} rows")

# ---------------------------------------------------------------------------
# 2. SUPPLIERS
# ---------------------------------------------------------------------------
SUPPLIER_NAMES = [
    "Global Textiles Inc", "Pacific Electronics Co", "FreshFoods Distributors",
    "HomeStyle Manufacturing", "Apex Sporting Goods", "Urban Furniture Group",
    "BrightTech Components", "Greenleaf Organics", "Sterling Houseware",
    "Velocity Auto Parts",
]
COUNTRIES = ["USA", "China", "Vietnam", "Mexico", "India", "Germany"]

suppliers = []
for i, name in enumerate(SUPPLIER_NAMES, start=1):
    suppliers.append({
        "supplier_id": f"SUP-{i:03d}",
        "supplier_name": name,
        "country": random.choice(COUNTRIES),
        "lead_time_days": random.choice([3, 5, 7, 10, 14, 21, 30]),
    })

with open(f"{OUTPUT_DIR}/suppliers.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["supplier_id", "supplier_name", "country", "lead_time_days"])
    writer.writeheader()
    writer.writerows(suppliers)

print(f"suppliers.csv        -> {len(suppliers)} rows")

# ---------------------------------------------------------------------------
# 3. PRODUCTS
# ---------------------------------------------------------------------------
CATEGORIES = {
    "Electronics": ["Headphones", "Smartphones", "Laptops", "Cameras"],
    "Apparel": ["Shirts", "Jeans", "Jackets", "Shoes"],
    "Home & Kitchen": ["Cookware", "Furniture", "Bedding", "Decor"],
    "Groceries": ["Beverages", "Snacks", "Dairy", "Produce"],
    "Sports": ["Fitness Equipment", "Outdoor Gear", "Team Sports", "Cycling"],
}

PRODUCT_ADJECTIVES = ["Premium", "Classic", "Pro", "Essential", "Deluxe", "Compact", "Ultra"]

products = []
product_id_counter = 1
for category, sub_categories in CATEGORIES.items():
    for sub_cat in sub_categories:
        # 3-4 products per sub-category
        for _ in range(random.randint(3, 4)):
            adjective = random.choice(PRODUCT_ADJECTIVES)
            supplier = random.choice(suppliers)
            # price ranges differ realistically by category
            price_ranges = {
                "Electronics": (49.99, 1299.99),
                "Apparel": (14.99, 149.99),
                "Home & Kitchen": (9.99, 399.99),
                "Groceries": (1.99, 24.99),
                "Sports": (12.99, 599.99),
            }
            low, high = price_ranges[category]
            products.append({
                "product_id": f"PRD-{product_id_counter:05d}",
                "product_name": f"{adjective} {sub_cat[:-1] if sub_cat.endswith('s') else sub_cat}",
                "category": category,
                "sub_category": sub_cat,
                "supplier_id": supplier["supplier_id"],
                "unit_price": round(random.uniform(low, high), 2),
            })
            product_id_counter += 1

with open(f"{OUTPUT_DIR}/products.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f, fieldnames=["product_id", "product_name", "category", "sub_category", "supplier_id", "unit_price"]
    )
    writer.writeheader()
    writer.writerows(products)

print(f"products.csv         -> {len(products)} rows")

# ---------------------------------------------------------------------------
# 4. INVENTORY (daily snapshots over a date range)
# ---------------------------------------------------------------------------
INVENTORY_START_DATE = datetime(2024, 1, 1)
INVENTORY_END_DATE = datetime(2024, 3, 31)  # 3 months of daily snapshots

inventory_rows = []
inventory_id_counter = 1

# To keep file size reasonable, we snapshot every 7 days (weekly) rather than
# daily for every product/store combo. Real systems often do this too —
# full daily granularity for millions of SKUs is expensive to store.
current_date = INVENTORY_START_DATE
while current_date <= INVENTORY_END_DATE:
    for store in stores:
        # Each store stocks a random subset of products, not all of them
        stocked_products = random.sample(products, k=min(40, len(products)))
        for product in stocked_products:
            inventory_rows.append({
                "inventory_id": f"INV-{inventory_id_counter:07d}",
                "product_id": product["product_id"],
                "store_id": store["store_id"],
                "stock_quantity": random.randint(0, 250),  # 0 = stockout, realistic!
                "snapshot_date": current_date.strftime("%Y-%m-%d"),
            })
            inventory_id_counter += 1
    current_date += timedelta(days=7)

with open(f"{OUTPUT_DIR}/inventory.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f, fieldnames=["inventory_id", "product_id", "store_id", "stock_quantity", "snapshot_date"]
    )
    writer.writeheader()
    writer.writerows(inventory_rows)

print(f"inventory.csv        -> {len(inventory_rows)} rows")

# ---------------------------------------------------------------------------
# 5. ORDERS (transactional data with realistic seasonality)
# ---------------------------------------------------------------------------
ORDER_START_DATE = datetime(2024, 1, 1)
ORDER_END_DATE = datetime(2024, 3, 31)
ORDER_STATUSES = ["Completed", "Completed", "Completed", "Completed", "Cancelled", "Returned"]
# weighted so ~67% Completed, ~17% Cancelled, ~17% Returned

orders = []
order_id_counter = 1

current_date = ORDER_START_DATE
while current_date <= ORDER_END_DATE:
    # Simulate seasonality: more orders on weekends, fewer on Mondays
    weekday = current_date.weekday()  # 0=Monday, 6=Sunday
    if weekday in (5, 6):  # weekend
        daily_order_count = random.randint(80, 130)
    elif weekday == 0:  # Monday — slow day
        daily_order_count = random.randint(30, 60)
    else:
        daily_order_count = random.randint(50, 90)

    for _ in range(daily_order_count):
        product = random.choice(products)
        store = random.choice(stores)
        quantity = random.randint(1, 5)
        status = random.choice(ORDER_STATUSES)
        total = round(product["unit_price"] * quantity, 2)

        orders.append({
            "order_id": f"ORD-{order_id_counter:08d}",
            "product_id": product["product_id"],
            "store_id": store["store_id"],
            "order_date": current_date.strftime("%Y-%m-%d"),
            "quantity": quantity,
            "total_amount": total,
            "order_status": status,
        })
        order_id_counter += 1

    current_date += timedelta(days=1)

with open(f"{OUTPUT_DIR}/orders.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f, fieldnames=["order_id", "product_id", "store_id", "order_date", "quantity", "total_amount", "order_status"]
    )
    writer.writeheader()
    writer.writerows(orders)

print(f"orders.csv            -> {len(orders)} rows")

print("\nAll files generated successfully in ./output/")
print("Total simulated business: Jan 1, 2024 - Mar 31, 2024 (Q1)")
