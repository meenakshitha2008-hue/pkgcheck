import json
from difflib import SequenceMatcher

import joblib
import numpy as np
from fastapi import FastAPI

from db import init_db, log_prediction, mark_wrong

app = FastAPI(title="pkgcheck")

model = joblib.load("models/model.joblib")
with open("models/popular.json") as f:
    info = json.load(f)
features = info["features"]
popular = info["popular"]

try:
    init_db()
except Exception as e:
    print("Database not ready:", e)


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


def save(name, verdict, risk, reasons):
    try:
        return log_prediction(name, verdict, risk, reasons)
    except Exception as e:
        print("Could not save to database:", e)
        return None


@app.get("/check")
def check(name: str):
    n = clean(name)
    if n in popular:
        reasons = ["one of the 500 most popular packages"]
        check_id = save(name, "SAFE", 0.0, reasons)
        return {"id": check_id, "name": name, "verdict": "SAFE",
                "risk_score": 0.0, "reasons": reasons}

    score, similar_to = closest(n)
    row = [[len(n), sum(c.isdigit() for c in n), n.count("-"), score]]
    risk = round(float(model.predict_proba(np.array(row))[0][1]), 2)

    reasons = []
    if score >= 0.85:
        reasons.append(f"name is very similar to popular package '{similar_to}'")
    if row[0][1] >= 3:
        reasons.append("name has many digits")
    if risk >= 0.5 and not reasons:
        reasons.append("name pattern looks like known bad packages")

    verdict = "RISKY" if risk >= 0.5 else "SAFE"
    check_id = save(name, verdict, risk, reasons)
    return {"id": check_id, "name": name, "verdict": verdict,
            "risk_score": risk, "reasons": reasons}


@app.post("/feedback")
def feedback(check_id: int):
    try:
        changed = mark_wrong(check_id)
    except Exception as e:
        print("Could not save feedback:", e)
        return {"ok": False, "message": "database not available"}
    if changed == 0:
        return {"ok": False, "message": "no check with that id"}
    return {"ok": True, "message": "thanks, marked as wrong alert"}