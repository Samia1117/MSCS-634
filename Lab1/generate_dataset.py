"""
Generates a synthetic retail sales dataset for MSCS 634 Lab 1.
Includes intentional missing values and outliers so the preprocessing
steps in the lab (missing value handling, outlier detection) have
real issues to work with.
"""

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

n = 1000

regions = ["North", "South", "East", "West"]
categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Toys"]

# base price per category so revenue makes sense
category_price = {
    "Electronics": 220,
    "Clothing": 45,
    "Home & Garden": 80,
    "Sports": 60,
    "Toys": 30,
}

dates = pd.date_range("2024-01-01", "2025-06-30", freq="D")
order_dates = rng.choice(dates, size=n)

category_choice = rng.choice(categories, size=n)
region_choice = rng.choice(regions, size=n)

units_sold = rng.poisson(lam=6, size=n) + 1

unit_price = np.array([
    category_price[c] * rng.uniform(0.85, 1.2) for c in category_choice
]).round(2)

discount_percent = rng.uniform(0, 30, size=n).round(1)
customer_age = rng.integers(18, 71, size=n)

sales_revenue = (units_sold * unit_price * (1 - discount_percent / 100)).round(2)

df = pd.DataFrame({
    "Order_ID": np.arange(1001, 1001 + n),
    "Order_Date": pd.to_datetime(order_dates),
    "Region": region_choice,
    "Product_Category": category_choice,
    "Units_Sold": units_sold,
    "Unit_Price": unit_price,
    "Discount_Percent": discount_percent,
    "Customer_Age": customer_age,
    "Sales_Revenue": sales_revenue,
})

df = df.sort_values("Order_Date").reset_index(drop=True)

# --- inject missing values ---
missing_age_idx = rng.choice(df.index, size=int(n * 0.05), replace=False)
df.loc[missing_age_idx, "Customer_Age"] = np.nan

missing_discount_idx = rng.choice(df.index, size=int(n * 0.04), replace=False)
df.loc[missing_discount_idx, "Discount_Percent"] = np.nan

missing_region_idx = rng.choice(df.index, size=int(n * 0.02), replace=False)
df.loc[missing_region_idx, "Region"] = np.nan

# --- inject outliers ---
outlier_idx = rng.choice(df.index, size=8, replace=False)
df.loc[outlier_idx, "Units_Sold"] = rng.integers(150, 400, size=8)
df.loc[outlier_idx, "Sales_Revenue"] = (
    df.loc[outlier_idx, "Units_Sold"]
    * df.loc[outlier_idx, "Unit_Price"]
    * (1 - df.loc[outlier_idx, "Discount_Percent"].fillna(0) / 100)
).round(2)

df.to_csv("data/retail_sales.csv", index=False)
print(df.shape)
print(df.head())
print(df.isna().sum())
