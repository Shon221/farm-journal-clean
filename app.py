# app.py
import streamlit as st
from parser import parse_entry
from journal_utils import save_entry
import pandas as pd
import os

st.title("🧠 יומן חקלאי חכם")

user_input = st.text_area("מה עשית היום בשטח?")

if st.button("נתח"):
    parsed = parse_entry(user_input)
    st.json(parsed)
    save_entry(parsed)
    if os.path.exists("data/journal.csv"):
        st.subheader("📅 יומן יומי עד עכשיו:")
        df = pd.read_csv("data/journal.csv")
        st.dataframe(df)
    st.success("המידע נשמר ביומן.")
