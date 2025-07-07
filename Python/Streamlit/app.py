# file: app.py
import streamlit as st
import pandas as pd

# Sample data
data = {
    "Address": ["Vadodara", "tyd", "Vadodara"],
    "Pincode": ["123456", "486464", "123456"],
    "Mobile Number": ["8980843332", "5656565565", "8980843332"],
    "Email": ["Microsoft12@GMAIL.COM", "kohli4@gmail.com", "microsoft4@gmail.com"],
    "PAN Number": ["AAACM5586C", "ANVPU7700M", "AYMPS6006N"],
    "GST Number": ["06AAACM5586C1ZL", "27ACUPT0038M1ZX", "27ACUPT0038M1ZX"]
}

df = pd.DataFrame(data)

# Page title
st.set_page_config(page_title="Fleet Lynk - Customer Profile", layout="wide")
st.title("🚛 Fleet Lynk - Customer Profiles")

# Sidebar
st.sidebar.header("Navigation")
st.sidebar.button("Master")
st.sidebar.button("Company")
st.sidebar.button("Transactions")

# Add new profile
if st.button("➕ Add New"):
    st.info("Add new customer modal would appear (placeholder)")

# Table
st.dataframe(df, use_container_width=True)

# Footer
st.markdown("---")
st.caption("Automation Tester • Streamlit Demo • July 2025")
