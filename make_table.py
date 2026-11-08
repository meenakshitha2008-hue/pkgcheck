import json
import pandas as pd

with open("data/bad_names.json") as f:
    bad = json.load(f)
with open("data/good_names.json") as f:
    good = json.load(f)

df = pd.DataFrame({"name": bad + good, "label": [1] * len(bad) + [0] * len(good)})
df["length"] = df["name"].str.len()
df["digits"] = df["name"].str.count(r"[0-9]")
df["dashes"] = df["name"].str.count(r"[-_.]")

print(df.shape)
print(df.groupby("label")[["length", "digits", "dashes"]].mean())
df.to_csv("data/features.csv", index=False)