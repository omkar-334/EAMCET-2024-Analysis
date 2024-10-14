import pandas as pd

sheets_dict = pd.read_excel("colleges.xlsx", sheet_name=None)

data = []

for college, df in sheets_dict.items():
    df["College"] = college
    data.append(df)

condf = pd.concat(data, ignore_index=True)
condf.to_excel("concolleges.xlsx", index=False)
