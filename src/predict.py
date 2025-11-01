import joblib
import pandas as pd
from feature_extraction import extract_features

def predict_url(url):
    model = joblib.load("models/phishing_model.pkl")
    df = pd.DataFrame({"url": [url]})
    df = extract_features(df)
    X = df[["url_length", "dot_count", "https", "suspicious_words"]]
    pred = model.predict(X)[0]
    return "Phishing" if pred == 1 else "Safe"

if __name__ == "__main__":
    url = input("Enter URL: ")
    print("Result:", predict_url(url))
