import pandas as pd
import numpy as np

df = pd.read_csv("hospital_data.csv")
df.dropna(axis=0, inplace=True)
df.to_csv("hospital_data_full.csv", index=False)