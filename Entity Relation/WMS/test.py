import pandas as pd

# List all sheet names in the Excel file
excel_file = "JV(Cash & Bank).xlsx"
sheet_names = pd.ExcelFile(excel_file).sheet_names
print(f"Sheet names available in the file: {sheet_names}")
