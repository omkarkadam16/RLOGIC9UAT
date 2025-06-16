import pandas as pd

# Original data
data = {
    "SeriesN": [
        "510851~510900",
        "39251~39300",
        "41051~41100",
        "43651~43700",
        "46001~46050",
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Split 'SeriesN' into 'Start' and 'End'
df[["Start", "End"]] = df["SeriesN"].str.split("~", expand=True)

# Convert to integers
df["Start"] = df["Start"].astype(int)
df["End"] = df["End"].astype(int)

# Save to Excel
df.to_excel("series_ranges.xlsx", index=False)

print("Excel file 'series_ranges.xlsx' saved successfully.")
