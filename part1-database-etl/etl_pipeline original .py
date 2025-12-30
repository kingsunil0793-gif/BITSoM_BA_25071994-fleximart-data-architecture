"""
FlexiMart ETL Pipeline (Task 1.1)
--------------------------------
Reads raw CSV files, cleans data quality issues,
and loads data into MySQL/PostgreSQL database.
"""

import pandas as pd
import re
from sqlalchemy import create_engine
from datetime import datetime

# ================= DATABASE CONFIG =================
# Update username, password, host, and database name
DB_URI = "mysql+pymysql://username:password@localhost/fleximart"
engine = create_engine(DB_URI)

# ================= HELPER FUNCTIONS =================
def standardize_phone(phone):
    """Convert phone numbers to +91-XXXXXXXXXX format"""
    if pd.isna(phone):
        return None
    digits = re.sub(r"\D", "", str(phone))
    if len(digits) == 10:
        return f"+91-{digits}"
    if len(digits) == 12 and digits.startswith("91"):
        return f"+91-{digits[2:]}"
    return None


def parse_date(date_value):
    """Convert multiple date formats to YYYY-MM-DD"""
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(str(date_value), fmt).date()
        except ValueError:
            continue
    return None


def standardize_category(category):
    """Standardize category names"""
    if pd.isna(category):
        return None
    return category.strip().capitalize()


# ================= EXTRACT =================
customers_df = pd.read_csv("customers_raw.csv")
products_df = pd.read_csv("products_raw.csv")
sales_df = pd.read_csv("sales_raw.csv")

report_lines = []

# ================= TRANSFORM: CUSTOMERS =================
initial_customers = len(customers_df)
customers_df.drop_duplicates(inplace=True)

missing_email_count = customers_df['email'].isna().sum()
customers_df = customers_df.dropna(subset=['email'])

customers_df['phone'] = customers_df['phone'].apply(standardize_phone)
customers_df['registration_date'] = customers_df['registration_date'].apply(parse_date)

final_customers = len(customers_df)
report_lines.append(
    f"Customers: Processed={initial_customers}, "
    f"Duplicates Removed={initial_customers - final_customers}, "
    f"Missing Emails Removed={missing_email_count}, "
    f"Loaded={final_customers}"
)

# ================= TRANSFORM: PRODUCTS =================
initial_products = len(products_df)
products_df.drop_duplicates(inplace=True)

missing_price_count = products_df['price'].isna().sum()
products_df['price'].fillna(products_df['price'].median(), inplace=True)

missing_stock_count = products_df['stock_quantity'].isna().sum()
products_df['stock_quantity'].fillna(0, inplace=True)

products_df['category'] = products_df['category'].apply(standardize_category)

final_products = len(products_df)
report_lines.append(
    f"Products: Processed={initial_products}, "
    f"Missing Prices Filled={missing_price_count}, "
    f"Missing Stock Filled={missing_stock_count}, "
    f"Loaded={final_products}"
)

# ================= TRANSFORM: SALES =================
initial_sales = len(sales_df)
sales_df.drop_duplicates(inplace=True)

missing_customer_ids = sales_df['customer_id'].isna().sum()
missing_product_ids = sales_df['product_id'].isna().sum()
sales_df = sales_df.dropna(subset=['customer_id', 'product_id'])

sales_df['transaction_date'] = sales_df['transaction_date'].apply(parse_date)
sales_df['subtotal'] = sales_df['quantity'] * sales_df['unit_price']

final_sales = len(sales_df)
report_lines.append(
    f"Sales: Processed={initial_sales}, "
    f"Duplicates Removed={initial_sales - final_sales}, "
    f"Missing Customer IDs Removed={missing_customer_ids}, "
    f"Missing Product IDs Removed={missing_product_ids}, "
    f"Loaded={final_sales}"
)

# ================= LOAD =================
customers_df.to_sql("customers", engine, if_exists="append", index=False)
products_df.to_sql("products", engine, if_exists="append", index=False)

orders_df = sales_df[['customer_id', 'transaction_date', 'status']].copy()
orders_df['total_amount'] = sales_df.groupby('customer_id')['subtotal'].transform('sum')
orders_df.drop_duplicates(inplace=True)

orders_df.rename(columns={'transaction_date': 'order_date'}, inplace=True)
orders_df.to_sql("orders", engine, if_exists="append", index=False)

order_items_df = sales_df[['product_id', 'quantity', 'unit_price', 'subtotal']].copy()
order_items_df.to_sql("order_items", engine, if_exists="append", index=False)

# ================= DATA QUALITY REPORT =================
with open("data_quality_report.txt", "w") as report_file:
    for line in report_lines:
        report_file.write(line + "\n")

print("ETL Pipeline executed successfully.")
