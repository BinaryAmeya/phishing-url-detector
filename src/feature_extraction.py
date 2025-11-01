import pandas as pd
from urllib.parse import urlparse

def extract_features(df):
    def url_length(u): return len(u)
    def dot_count(u): return u.count(".")
    def has_https(u): return 1 if u.lower().startswith("https") else 0
    def has_suspicious_words(u):
        words = ["login", "verify", "update", "secure", "account", "bank"]
        return int(any(w in u.lower() for w in words))

    df["url_length"] = df["url"].apply(url_length)
    df["dot_count"] = df["url"].apply(dot_count)
    df["https"] = df["url"].apply(has_https)
    df["suspicious_words"] = df["url"].apply(has_suspicious_words)
    return df

if __name__ == "__main__":
    data = pd.read_csv("data/processed/cleaned_data.csv")
    df = extract_features(data)
    df.to_csv("data/processed/features.csv", index=False)
    print("Saved features to data/processed/features.csv")
