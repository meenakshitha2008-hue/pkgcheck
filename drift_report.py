import json
from difflib import SequenceMatcher

import pandas as pd
import psycopg2
from evidently import Report
from evidently.presets import DataDriftPreset

DB_URL = "postgresql://postgres:pkgpass@localhost:5432/pkgcheck"
features = ["length", "digits", "dashes", "closest_score"]

with open("models/popular.json") as f:
    popular = json.load(f)["popular"]


def clean(name):
    return name.lower().replace("_", "-").replace(".", "-")


def make_row(name):
    n = clean(name)
    best = 0.0
    for p in popular:
        if p != n:
            s = SequenceMatcher(None, n, p).ratio()
            if s > best:
                best = s
    return [len(n), sum(c.isdigit() for c in n), n.count("-"), round(best, 3)]


conn = psycopg2.connect(DB_URL)
cur = conn.cursor()
cur.execute("SELECT name FROM predictions")
names = [r[0] for r in cur.fetchall()]
conn.close()

print("checks in database:", len(names))
if len(names) < 30:
    print("Too few checks for a meaningful drift test (need about 30 or more).")
else:
    current = pd.DataFrame([make_row(n) for n in names], columns=features)
    reference = pd.read_csv("data/features.csv")[features]
    report = Report([DataDriftPreset()])
    result = report.run(current, reference)
    result.save_html("drift_report.html")
    print("saved drift_report.html")