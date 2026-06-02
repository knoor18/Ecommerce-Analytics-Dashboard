import pandas as pd

def load_data():
    return pd.read_csv("sales_data.csv")

def total_sales(df):
    return int(df["Sales"].sum())

def total_profit(df):
    return int(df["Profit"].sum())

def total_orders(df):
    return df["OrderID"].count()

def top_products(df):
    return df.groupby("Product")["Sales"].sum().sort_values(ascending=False).head(10)

def top_customers(df):
    return df.groupby("Customer")["Sales"].sum().sort_values(ascending=False).head(10)