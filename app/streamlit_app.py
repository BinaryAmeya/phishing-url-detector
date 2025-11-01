import streamlit as st
from src.predict import predict_url

st.title("Phishing URL Detector")
url = st.text_input("Enter a URL to check:")

if st.button("Check"):
    result = predict_url(url)
    st.write("Result:", result)
