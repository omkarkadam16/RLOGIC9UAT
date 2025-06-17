import pandas as pd

data = {
    "Document": ["Delivery", "Delivery"],
    "OrganizationLocation": ["Mumbai", "Mumbai"],
    "StartNo": [1001, 2000],
    "EndNo": [1999, 2999],
    "Prefix": ["MUM", "MUM"],
    "Suffix": ["BKG", "BKG"],
    "SeriesName": ["MUMBAI - 1001 To 1999", "MUMBAI - 2000 To 2999"],
    "Seperator": ["--", "--"],
    "DocumentNoLength": [6, 6],
    "YearCode": ["2023 - 2024", "2023 - 2024"],
}


df = pd.DataFrame(data)
df.to_excel("UID 1.xlsx", index=False, engine="openpyxl")
print("Excel file created successfully.")
