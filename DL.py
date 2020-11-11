import pandas as pd
df= pd.read_csv("D:\\DrivingLicense\\file2.csv")
df["ID"]=df.ID.astype(str)
ids=df["ID"].values

ids

#print(ids)
