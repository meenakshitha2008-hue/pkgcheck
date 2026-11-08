import json
from difflib import SequenceMatcher

import joblib
import pandas as pd
from fastapi import FastAPI

app = FastAPI(title="pkgcheck")

model = joblib.load("models/model.joblib")
with open("models/popular.json") as f:
    info = json.load(f)
features = info["features"]
popular = info["popular"]


def clean(name):
    return name.lower().replace("_", "-").replace(".", "-")


def closest(n):
    best, best_name = 0.0, ""
    for p in popular:
        if p != n:
            score = SequenceMatcher(None, n, p).ratio()
            if score > best:
                best, best_name = score, p
    return round(best, 3), best_name


@app.get("/check")
def check(name: str):
    n = clean(name)
    if n in popular:
        return {"name": name, "verdict": "SAFE", "risk_score": 0.0,
                "reasons": ["one of the 500 most popular packages"]}

    score, similar_to = closest(n)
    row = [[len(n), sum(c.isdigit() for c in n), n.count("-"), score]]
    X = pd.DataFrame(row, columns=features)
    risk = float(model.predict_proba(X)[0][1])

    reasons = []
    if score >= 0.85:
        reasons.append(f"name is very similar to popular package '{similar_to}'")
    if row[0][1] >= 3:
        reasons.append("name has many digits")
    if risk >= 0.5 and not reasons:
        reasons.append("name pattern looks like known bad packages")

    return {"name": name, "verdict": "RISKY" if risk >= 0.5 else "SAFE",
            "risk_score": round(risk, 2), "reasons": reasons}