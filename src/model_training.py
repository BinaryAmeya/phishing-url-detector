import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

def train_model():
    df = pd.read_csv("data/processed/features.csv")
    X = df[["url_length", "dot_count", "https", "suspicious_words"]]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    joblib.dump(model, "models/phishing_model.pkl")

    print(f"Model trained. Accuracy: {acc:.3f}")
    print("Saved as models/phishing_model.pkl")

if __name__ == "__main__":
    train_model()
