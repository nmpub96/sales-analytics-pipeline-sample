import pandas as pd
import duckdb
import pantab
import os

# -----------------------------
# Configuration
# -----------------------------
INPUT_FILE = "data/raw/Product-Sales-Region.xlsx"
OUTPUT_HYPER = "output/cleansed_sales_data.hyper"

# Create output directory
os.makedirs("output", exist_ok=True)

# -----------------------------
# Step 1: Load Data
# -----------------------------
print("Loading dataset...")
df = pd.read_excel(INPUT_FILE)
print(f"Dataset loaded: {df.shape[0]:,} rows, {df.shape[1]} columns")

# -----------------------------
# Step 2: Data Inspection
# -----------------------------
print("\nData Info:")
print(df.info())

# -----------------------------
# Step 3: Convert & Standardize Data Types
# -----------------------------
df = df.convert_dtypes()

# String conversion for better consistency
string_columns = ['Region', 'Product', 'StoreLocation', 'CustomerType', 
                 'Salesperson', 'PaymentMethod', 'Promotion', 'OrderID', 
                 'CustomerName', 'RegionManager']

for col in string_columns:
    if col in df.columns:
        df[col] = df[col].astype("string")

print("\nData types after standardization:")
print(df.dtypes)

# -----------------------------
# Step 4: DuckDB SQL Transformations
# -----------------------------
print("\nPerforming SQL transformations with DuckDB...")

result = duckdb.query("""
    SELECT
        Date,
        Region,
        Product,
        Quantity,
        UnitPrice,
        StoreLocation,
        CustomerType,
        Discount,
        Salesperson,
        PaymentMethod,
        Promotion,
        Returned,
        OrderDate,
        DeliveryDate,
        RegionManager,
        
        Quantity * UnitPrice AS Revenue,
        IFNULL(Promotion, 'None') AS Promo,
        
        CASE 
            WHEN Quantity < 10 THEN 'Low'
            ELSE 'High'
        END AS VolumeCategory,
        
        DATE_DIFF('day', OrderDate, DeliveryDate) AS DeliveryLeadTimeDays

    FROM df
    WHERE Quantity IS NOT NULL 
      AND UnitPrice > 0
""").to_df()

print(f"Transformed dataset: {result.shape[0]:,} rows, {result.shape[1]} columns")

# -----------------------------
# Step 5: Export to Tableau Hyper File
# -----------------------------
print(f"\nExporting to Tableau Hyper format: {OUTPUT_HYPER}")
pantab.frame_to_hyper(result, OUTPUT_HYPER, table="clean_sales")

print("Data cleansed")
