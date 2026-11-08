import pandas as pd
from difflib import SequenceMatcher

df = pd.read_csv("data/features.csv")

def clean(name):
    return name.lower().replace("_", "-").replace(".", "-")

popular = [clean(n) for n in df[df["label"] == 0]["name"][:500]]

def closest(name):
    n = clean(name)
    best = 0.0
    for p in popular:
        if p != n:
            score = SequenceMatcher(None, n, p).ratio()
            if score > best:
                best = score
    return round(best, 3)

df["closest_score"] = df["name"].apply(closest)

print(df.groupby("label")["closest_score"].mean())
df.to_csv("data/features.csv", index=False)