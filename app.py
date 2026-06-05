import streamlit as st
import pandas as pd
import plotly.express as px

from database import authenticate
from logger import save_log
from backend import *

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

# ---------- LOGIN SYSTEM ----------

def login():

    st.title("🔐 E-Commerce Dashboard Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        success, role = authenticate(username, password)

        if success:
            st.session_state.logged_in = True
            st.session_state.role = role

            save_log(username, "Login")

            st.success("Login Successful")
            st.rerun()

        else:
            st.error("Invalid Username or Password")

# Session state
if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None    

# Show login page if not logged in
if not st.session_state.logged_in:
    login()
    st.stop()

# Page Config
st.set_page_config(page_title="E-Commerce Analytics", layout="wide")

# Custom CSS (Premium UI)
st.markdown("""
    <style>
    body {
        background-color: #0E1117;
        color: white;
    }
    .stMetric {
        background-color: #1c1f26;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🛒 E-Commerce Sales Analytics Dashboard")

# Logout Button
if st.button("🚪 Logout"):

    save_log(st.session_state.username,"Logout")

    st.session_state.logged_in = False
    st.rerun()

# Load Data
df = load_data()

# Sidebar Filters
st.sidebar.header("🔍 Filters")

region_filter = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

category_filter = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

# Filter Data
filtered_df = df[
    (df["Region"].isin(region_filter)) &
    (df["Category"].isin(category_filter))
]

# KPIs
total_sales_value = total_sales(filtered_df)
total_profit_value = total_profit(filtered_df)
total_orders_value = total_orders(filtered_df)

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Sales", total_sales_value)
col2.metric("📈 Total Profit", total_profit_value)
col3.metric("📦 Total Orders", total_orders_value)

# Sales Trend
st.subheader("📊 Monthly Sales Trend")
filtered_df["OrderDate"] = pd.to_datetime(filtered_df["OrderDate"])
monthly = filtered_df.groupby(filtered_df["OrderDate"].dt.to_period("M"))["Sales"].sum().reset_index()
monthly["OrderDate"] = monthly["OrderDate"].astype(str)

fig1 = px.line(monthly, x="OrderDate", y="Sales", title="Monthly Sales")
st.plotly_chart(fig1, use_container_width=True)

# Category Sales
col4, col5 = st.columns(2)

with col4:
    st.subheader("🛍 Category Sales")
    cat = filtered_df.groupby("Category")["Sales"].sum().reset_index()
    fig2 = px.bar(cat, x="Category", y="Sales", color="Category")
    st.plotly_chart(fig2, use_container_width=True)

with col5:
    st.subheader("🌍 Region Sales")
    reg = filtered_df.groupby("Region")["Sales"].sum().reset_index()
    fig3 = px.pie(reg, names="Region", values="Sales")
    st.plotly_chart(fig3, use_container_width=True)

# Top Products
st.subheader("🔥 Top Products")
top_products = filtered_df.groupby("Product")["Sales"].sum().sort_values(ascending=False).head(10)
st.dataframe(top_products)

# Customer Analysis
st.subheader("👤 Top Customers")
customers = filtered_df.groupby("Customer")["Sales"].sum().sort_values(ascending=False).head(10)
st.dataframe(customers)

# Full Data
st.subheader("📂 Full Dataset")
st.dataframe(filtered_df)

st.subheader("📥 Download Reports")

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="Download Sales Report",
    data=csv,
    file_name="sales_report.csv",
    mime="text/csv"
)

if st.session_state.role == "admin":

    st.subheader("🛠 Admin Panel")

    logs = pd.read_csv("logs.csv")

    st.write("User Activity Logs")

    st.dataframe(logs)