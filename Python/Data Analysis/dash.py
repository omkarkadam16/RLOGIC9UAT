# dashboard_app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("📊 Booking Dashboard")

# Upload Excel file or use default
df = pd.read_excel("sample1.xlsx")

# Top 5 Clients by Total Booking
top5_df = df.sort_values(by="Total Booking", ascending=False).head(5)

st.subheader("Top 5 Clients by Total Booking")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="Total Booking", y="Billing Client", data=top5_df, palette="Blues_d", ax=ax)
ax.set_title("Top 5 Clients by Total Booking")
st.pyplot(fig)