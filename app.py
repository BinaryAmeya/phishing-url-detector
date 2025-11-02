# app.py
import os
import urllib.request
import joblib
import streamlit as st
from src.feature_extraction import extract_features

# --- CONFIG ---
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "phishing_model.pkl")

# Replace this with the raw download URL of your GitHub Release asset (see step B)
# Example: "https://github.com/BinaryAmeya/phishing-url-detector/releases/download/v0.1.0/phishing_model.pkl"
MODEL_URL = os.getenv("MODEL_URL", "")  # Streamlit Cloud: set this in Secrets or leave empty and set below

# If you prefer to hardcode temporarily, set:
# MODEL_URL = "https://github.com/YourUser/your-repo/releases/download/v0.1.0/phishing_model.pkl"

os.makedirs(MODEL_DIR, exist_ok=True)

def ensure_model():
    if os.path.exists(MODEL_PATH):
        return True
    if not MODEL_URL:
        return False
    try:
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
        return True
    except Exception as e:
        st.error(f"Failed to download model: {e}")
        return False

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

st.set_page_config(page_title="Phishing URL Detector", layout="centered")
st.title("Phishing URL Detector")

# Ensure model is present (download from release if not)
if not os.path.exists(MODEL_PATH):
    st.info("Model not found locally. Attempting to download...")
    ok = ensure_model()
    if not ok:
        st.error("Model unavailable. Upload the model to a GitHub Release and set MODEL_URL. See README.")
        st.stop()

# Load model
try:
    model = load_model()
except Exception as e:
    st.error(f"Model load error: {e}")
    st.stop()

url = st.text_input("Enter a URL to check", "")

if st.button("Check URL"):
    if not url.strip():
        st.warning("Enter a URL.")
    else:
        # extract features from single URL
        df = extract_features(__import__("pandas").DataFrame({"url":[url]}))
        X = df[["url_length","dot_count","https","suspicious_words","host_entropy"]]
        pred = model.predict(X)[0]
        proba = None
        if hasattr(model, "predict_proba"):
            proba = float(model.predict_proba(X)[0][1])
        label = "Phishing" if int(pred)==1 else "Safe"
        st.write("**Result:**", label)
        if proba is not None:
            st.write(f"**Phishing probability:** {proba:.3f}")
        st.write("**Features:**")
        st.json(X.iloc[0].to_dict())
