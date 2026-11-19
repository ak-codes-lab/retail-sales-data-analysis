
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Retail Sales Dashboard",
    layout="wide"
)

st.title("Retail Sales Analysis Dashboard")
st.write("Welcome to the Retail Sales Dashboard!")

# Load cleaned dataset
df = pd.read_csv("data/processed/retail_sales_cleaned.csv")

# Calculate KPIs
total_revenue = df["total_price"].sum()
total_units = df["quantity"].sum()
total_transactions = df["order_id"].nunique()
total_products = df["product_name"].nunique()
average_order = total_revenue / total_transactions

# Display KPIs
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Revenue", f"₹{total_revenue:,.2f}")
col2.metric("Units Sold", total_units)
col3.metric("Transactions", total_transactions)
col4.metric("Unique Products", total_products)
col5.metric("Average Order Value", f"₹{average_order:,.2f}")

st.divider()

# Sales by Region
st.subheader("Sales by Region")
region_sales = df.groupby("customer_region")["total_price"].sum()
st.bar_chart(region_sales)

# Sales by Category
st.subheader("Sales by Product Category")
category_sales = df.groupby("category")["total_price"].sum()
st.bar_chart(category_sales)

# Top 5 Products
st.subheader("Top 5 Best-Selling Products")
top_products = df.groupby("product_name")["quantity"].sum().nlargest(5)
st.bar_chart(top_products)

# Monthly Sales Trend
st.subheader("Monthly Sales Trend")
df["order_date"] = pd.to_datetime(df["order_date"], dayfirst=True)
df["month"] = df["order_date"].dt.to_period("M").astype(str)

monthly_sales = df.groupby("month")["total_price"].sum()
st.line_chart(monthly_sales)
