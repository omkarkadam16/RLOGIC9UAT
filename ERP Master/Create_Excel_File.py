import pandas as pd

# Define data
data = {
    "Commodity Name": ["TEST16", "TEST12", "TEST13", "TEST14", "TEST15"],
    "Commodity Code": ["T16", "T12", "T13", "T14", "T15"],
}

# Create a DataFrame
df = pd.DataFrame(data)

# Save as an Excel file
df.to_excel("test_data.xlsx", index=False)

print("✅ Excel file 'test_data.xlsx' created successfully!")
