import sys
import os

# Force add project root to Python path (works locally + Streamlit Cloud)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from src.predict import predict_url

import streamlit as st
from src.predict import predict_url

st.title("Phishing URL Detector")
url = st.text_input("Enter a URL to check:")

if st.button("Check"):
    result = predict_url(url)
    st.write("Result:", result)
