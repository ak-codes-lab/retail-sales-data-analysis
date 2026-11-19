print("Retail Sales Data Analysis Project")
print("Project started successfully!")
print("Using Python for Data Analysis")
import pandas as pd

# Load the retail sales dataset
df = pd.read_csv("data/raw/retail_sales.csv")

# Display dataset information
print("\nDataset loaded successfully!")

print("\nFirst 5 records:")
print(df.head())

print("\nDataset shape:")
print(df.shape)

print("\nColumn names:")
print(df.columns.tolist())
# Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Check duplicate records
print("\nDuplicate Records:")
print(df.duplicated().sum())

# Check data types
print("\nData Types:")
print(df.dtypes)
# Statistical summary
print("\nStatistical Summary:")
print(df.describe())

# Sales by region
print("\nSales by Region:")
print(df.groupby("customer_region")["total_price"].sum())

# Total sales
print("\nTotal Sales:")
print(df["total_price"].sum())

# Data Cleaning and Validation

print("\n--- DATA CLEANING CHECKS ---")

# Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Check duplicate records
print("\nDuplicate Records:")
print(df.duplicated().sum())

# Check invalid dates
dates = pd.to_datetime(
    df["order_date"],
    format="%d-%m-%Y",
    errors="coerce"
)
print("\nInvalid Dates:")
print(dates.isnull().sum())

# Check negative quantities
print("\nNegative Quantities:")
print((df["quantity"] < 0).sum())

# Check invalid prices
print("\nZero or Negative Prices:")
print((df["unit_price"] <= 0).sum())

# Check negative sales
print("\nNegative Sales:")
print((df["total_price"] < 0).sum())

# Inspect invalid prices

print("\nRecords with zero or negative prices:")

print(df[df["unit_price"] <= 0])
# Check invalid price records

invalid_prices = df[df["unit_price"] <= 0]

print("\nInvalid Price Details:")
print(invalid_prices[[
    "order_id",
    "product_name",
    "unit_price",
    "quantity",
    "total_price"
]].to_string(index=False))

# Check price calculation

invalid_prices["expected_total"] = (
    invalid_prices["unit_price"] *
    invalid_prices["quantity"]
)

print("\nPrice Comparison:")
print(invalid_prices[[
    "order_id",
    "unit_price",
    "quantity",
    "total_price",
    "expected_total"
]].to_string(index=False))

# Create a cleaned dataset

cleaned_df = df[df["unit_price"] > 0].copy()

# Save cleaned dataset
cleaned_df.to_csv(
    "data/processed/retail_sales_cleaned.csv",
    index=False
)

print("\nCleaned dataset saved successfully!")
print("Original records:", len(df))
print("Cleaned records:", len(cleaned_df))
print("Removed records:", len(df) - len(cleaned_df))
import matplotlib.pyplot as plt

# Sales by region
region_sales = cleaned_df.groupby(
    "customer_region"
)["total_price"].sum()

plt.figure(figsize=(8, 5))
region_sales.plot(kind="bar")

plt.title("Total Sales by Region")
plt.xlabel("Region")
plt.ylabel("Total Sales")
plt.tight_layout()

plt.savefig("outputs/sales_by_region.png")
plt.show()
# Sales by Category

category_sales = cleaned_df.groupby(
    "category"
)["total_price"].sum()

plt.figure(figsize=(8, 5))
category_sales.plot(kind="pie", autopct="%1.1f%%")

plt.title("Sales by Product Category")
plt.ylabel("")

plt.tight_layout()
plt.savefig("outputs/sales_by_category.png")
plt.show()
# Top 5 Best-Selling Products

product_sales = cleaned_df.groupby(
    "product_name"
)["quantity"].sum().sort_values(ascending=False).head(5)

plt.figure(figsize=(8, 5))
product_sales.plot(kind="bar")

plt.title("Top 5 Best-Selling Products")
plt.xlabel("Product")
plt.ylabel("Quantity Sold")

plt.tight_layout()
plt.savefig("outputs/top_5_products.png")
plt.show()

# Monthly Sales Trend

cleaned_df["order_date"] = pd.to_datetime(
    cleaned_df["order_date"]
)

monthly_sales = cleaned_df.groupby(
    cleaned_df["order_date"].dt.to_period("M")
)["total_price"].sum()

monthly_sales.index = monthly_sales.index.astype(str)

plt.figure(figsize=(10, 5))

plt.plot(
    monthly_sales.index,
    monthly_sales.values,
    marker="o"
)

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")

plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("outputs/monthly_sales_trend.png")
plt.show()

# KPI Calculation

# 1. Total Revenue
total_revenue = cleaned_df["total_price"].sum()

# 2. Total Units Sold
total_units = cleaned_df["quantity"].sum()

# 3. Total Transactions
total_transactions = cleaned_df["order_id"].nunique()

# 4. Total Unique Products
total_products = cleaned_df["product_name"].nunique()

# 5. Average Order Value
average_order_value = total_revenue / total_transactions

# Display KPIs
print("\n========== SALES KPI SUMMARY ==========")

print("Total Revenue:", round(total_revenue, 2))
print("Total Units Sold:", total_units)
print("Total Transactions:", total_transactions)
print("Total Unique Products:", total_products)
print("Average Order Value:", round(average_order_value, 2))
