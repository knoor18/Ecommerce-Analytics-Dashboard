import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from io import BytesIO

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime
from reportlab.lib.styles import getSampleStyleSheet

import init_db
import insert_users

from database import authenticate
from logger import save_log
from backend import *

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

def generate_pdf(total_sales, total_profit, total_orders):

    pdf = SimpleDocTemplate("sales_report.pdf")

    styles = getSampleStyleSheet()

    elements = []

    # Title
    elements.append(
        Paragraph(
            "E-Commerce Sales Analytics Dashboard Report",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 20))

    # Date
    elements.append(
        Paragraph(
            f"Generated On: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 12))

    # Executive Summary
    elements.append(
        Paragraph(
            "Executive Summary",
            styles["Heading2"]
        )
    )

    elements.append(
        Paragraph(
            "This report provides an overview of sales performance, profit analysis, "
            "and order statistics generated from the E-Commerce Analytics Dashboard.",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 15))

    # Dashboard Highlights
    elements.append(
        Paragraph(
            "Dashboard Highlights",
            styles["Heading2"]
        )
    )

    elements.append(
        Paragraph(
            "• Sales Performance Tracking<br/>"
            "• Profit Analysis<br/>"
            "• Order Monitoring<br/>"
            "• Customer Insights<br/>"
            "• Region-wise Analysis",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 15))

    # KPI Table
    data = [
        ["Metric", "Value"],
        ["Total Sales", f"₹ {total_sales:,.2f}"],
        ["Total Profit", f"₹ {total_profit:,.2f}"],
        ["Total Orders", str(total_orders)]
    ]

    table = Table(data, colWidths=[220, 180])

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER')
    ]))

    elements.append(table)

    elements.append(Spacer(1, 20))

    # Conclusion
    elements.append(
        Paragraph(
            "Conclusion",
            styles["Heading2"]
        )
    )

    elements.append(
        Paragraph(
            "The dashboard helps businesses analyze sales trends, monitor profits, "
            "and track order activity. These insights support better decision-making "
            "and business growth.",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 20))

    # Footer
    elements.append(
        Paragraph(
            "Generated using E-Commerce Sales Analytics Dashboard",
            styles["Italic"]
        )
    )

    pdf.build(elements)

    return "sales_report.pdf"

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
            st.session_state.username = username

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

st.write("Sales:", total_sales_value)
st.write("Profit:", total_profit_value)
st.write("Orders:", total_orders_value)

pdf_file = generate_pdf(
    total_sales_value,
    total_profit_value,
    total_orders_value
)


with open(pdf_file, "rb") as f:
    st.download_button(
        label="Download PDF Report",
        data=f,
        file_name="sales_report.pdf",
        mime="application/pdf"
    )

if st.session_state.role == "admin":

    st.subheader("🛠 Admin Panel")
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(DISTINCT username) FROM Users")
    total_users = cursor.fetchone()[0]

    conn.close()

    st.metric("👥 Total Users", total_users)

    st.subheader("➕ Add New User")

    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    new_role = st.selectbox("Role", ["user", "admin"])

    if st.button("Create User"):

        if new_username.strip() == "":
            st.error("Username cannot be empty")

    elif len(new_password) < 6:
        st.error("Password must be at least 6 characters")

    else:

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM Users WHERE username=?",
            (new_username,)
        )

        existing_user = cursor.fetchone()

        if existing_user:
            st.error("Username already exists")

        else:
            cursor.execute(
                "INSERT INTO Users (username, password, role) VALUES (?, ?, ?)",
                (new_username, new_password, new_role)
            )

            conn.commit()
            st.success("User Created Successfully ✅")

        conn.close()

    st.subheader("👥 Users Database")

    conn = sqlite3.connect("database.db")

    users_df = pd.read_sql_query(
        "SELECT username, role FROM Users",
        conn
    )

    st.dataframe(users_df)

    conn.close()    

    logs = pd.read_csv("logs.csv")

    st.write("User Activity Logs")

    logs = pd.read_csv("logs.csv")   # Read latest logs every time
    st.dataframe(logs)

        

    