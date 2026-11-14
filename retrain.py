import json
from difflib import SequenceMatcher

import joblib
import pandas as pd
import psycopg2
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score
from sklearn.model_selection import train_test_split

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
cur.execute("SELECT name, verdict FROM predictions WHERE wrong_alert = TRUE")
rows = cur.fetchall()
conn.close()
print("wrong-alert rows found:", len(rows))

df = pd.read_csv("data/features.csv")
X = df[features]
y = df["label"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

fb_X = pd.DataFrame([make_row(n) for n, v in rows], columns=features)
fb_y = pd.Series([0 if v == "RISKY" else 1 for n, v in rows], dtype=int)

if len(rows) > 0:
    X_train = pd.concat([X_train, fb_X], ignore_index=True)
    y_train = pd.concat([y_train.reset_index(drop=True), fb_y], ignore_index=True)

new_model = RandomForestClassifier(
    n_estimators=200, class_weight="balanced", min_samples_leaf=5, random_state=42
)
new_model.fit(X_train, y_train)
old_model = joblib.load("models/model.joblib")


def show(label, m):
    pred = m.predict(X_test)
    print(
        label,
        "precision_bad:", round(precision_score(y_test, pred), 2),
        "recall_bad:", round(recall_score(y_test, pred), 2),
    )


show("current model:  ", old_model)
show("candidate model:", new_model)

if len(rows) > 0:
    old_ok = int((old_model.predict(fb_X.values) == fb_y.values).sum())
    new_ok = int((new_model.predict(fb_X.values) == fb_y.values).sum())
    print("feedback rows answered correctly: current", old_ok, "of", len(rows),
          "| candidate", new_ok, "of", len(rows))

joblib.dump(new_model, "models/model_candidate.joblib")
print("saved models/model_candidate.joblib")