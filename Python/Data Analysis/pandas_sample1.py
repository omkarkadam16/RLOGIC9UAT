import pandas as pd

df =  pd.read_excel("sample.xlsx") #df = pd.read_csv("sample.csv")

pune_df = df[df["City"].str.strip().str.lower() == "pune"]

print(pune_df["PartyName"].to_list()) #


