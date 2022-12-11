import pandas as pd
df = pd.read_csv(r"new\n.csv")
print(df["str_best_position"].unique())
