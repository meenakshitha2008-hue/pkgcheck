import json, os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv("data/features.csv")
features = ["length", "digits", "dashes", "closest_score"]
X = df[features]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(
    n_estimators=200, class_weight="balanced", min_samples_leaf=5, random_state=42
)
model.fit(X_train, y_train)

def clean(name):
    return name.lower().replace("_", "-").replace(".", "-")

popular = [clean(n) for n in df[df["label"] == 0]["name"][:500]]

os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/model.joblib")
with open("models/popular.json", "w") as f:
    json.dump({"features": features, "popular": popular}, f)

print("saved", os.path.getsize("models/model.joblib") // 1024, "KB")

m = joblib.load("models/model.joblib")
print(m.predict(X_test.head(3)))