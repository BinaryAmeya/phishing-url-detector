import sys
import os
import streamlit as st

# Ensure the project root is on the Python path (so Streamlit Cloud finds src/)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from src.predict import predict_url

st.title("Phishing URL Detector")

url = st.text_input("Enter a URL to check:")

if st.button("Check"):
    result = predict_url(url)
    st.write("Result:", result)
