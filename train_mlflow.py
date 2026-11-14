import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("pkgcheck")

df = pd.read_csv("data/features.csv")
features = ["length", "digits", "dashes", "closest_score"]
X = df[features]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

params = {
    "n_estimators": 200,
    "min_samples_leaf": 5,
    "class_weight": "balanced",
    "random_state": 42,
}

with mlflow.start_run(run_name="random_forest"):
    model = RandomForestClassifier(**params)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    mlflow.log_params(params)
    mlflow.log_metric("precision_bad", precision_score(y_test, pred))
    mlflow.log_metric("recall_bad", recall_score(y_test, pred))
    mlflow.log_metric("accuracy", accuracy_score(y_test, pred))
    mlflow.sklearn.log_model(
        model, name="model", serialization_format="cloudpickle"
    )
    print("logged run")