import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import matplotlib.pyplot as plt

# SQL Server connection details
server = 'DESKTOP-CU1U7Q0'
database = 'DemoDB'
username = 'Omkar'
password = 'Om12345@'  # Replace with your password
port = 1433

# Connection string for SQLAlchemy + pyodbc
conn_str = (
    f"mssql+pyodbc://{username}:{password}@{server}:{port}/{database}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
)

# Create SQLAlchemy engine
engine = create_engine(conn_str)

# Query your view
query = "SELECT * FROM DepartmentSalaryView"

# Load data into pandas DataFrame
df = pd.read_sql(query, engine)

# Print columns to check names (remove or comment after confirming)
st.write("Columns in DataFrame:", df.columns.tolist())
print("Columns:", df.columns.tolist())

# Adjust column names here based on output
# Example: If column is 'Department' instead of 'DeptName'
department_col = 'DeptName'  # change to your actual column name from the view

# Check if the department_col exists, if not, pick the first string column as fallback
if department_col not in df.columns:
    # Try to find a likely column automatically
    string_cols = df.select_dtypes(include='object').columns
    if len(string_cols) > 0:
        department_col = string_cols[0]
    else:
        st.error(f"Department column '{department_col}' not found and no fallback available.")
        st.stop()

# Calculate average salary by department
avg_salary = df.groupby(department_col)['Salary'].mean().reset_index()

# Streamlit visualization
st.title("Department Salary Dashboard")

st.write("Average Salary by Department")
st.bar_chart(data=avg_salary.set_index(department_col))

# Optional: show raw data
if st.checkbox("Show raw data"):
    st.write(df)
