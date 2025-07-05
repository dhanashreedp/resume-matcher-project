import streamlit as st
import requests

st.markdown("<h1 style='text-align: center; font-size: 40px;'>🧠 AI Resume Parser + <span style='color:#4CAF50;'>Job Matcher</span></h1>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

if uploaded_file:
    files = {'resume': uploaded_file.getvalue()}
    
    with st.spinner('Parsing Resume & Finding Matches...'):
        response = requests.post("http://localhost:5000/parse_and_match", files=files)
        
    if response.status_code == 200:
        result = response.json()
        st.success("Resume parsed successfully!")
        st.write("### Candidate Info:", result.get("candidate_info"))
        st.write("### Matched Jobs:", result.get("matched_jobs"))
    else:
        st.error("Error: " + response.text)
