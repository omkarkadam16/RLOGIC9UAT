import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Step 1: Load Excel file
df = pd.read_excel("sample1.xlsx")

# Optional: View first few rows to confirm
print(df.head())

# Step 2: Create a barplot - Total Booking by Billing Client
plt.figure(figsize=(12,6))  # Wider chart
sns.barplot(x="Total Booking", y="Billing Client", data=df, palette="Blues_d")

# Step 3: Add chart title and labels
plt.title("Total Bookings by Billing Client", fontsize=14)
plt.xlabel("Total Bookings", fontsize=12)
plt.ylabel("Billing Client", fontsize=12)

# Step 4: Show the chart
plt.tight_layout()
plt.show()
