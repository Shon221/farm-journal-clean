import streamlit as st
import pandas as pd
import os
from parser import parse_entry
from journal_utils import save_entry

DATA_FILE = "data/journal.csv"

st.title("🧠 יומן חקלאי חכם")

user_input = st.text_area("מה עשית היום בשטח?")

if st.button("נתח"):
    parsed = parse_entry(user_input)
    st.json(parsed)
    save_entry(parsed)
    st.success("המידע נשמר ביומן.")

# הצגת יומן עם אפשרות מחיקה
if os.path.exists(DATA_FILE):
    st.subheader("📅 יומן יומי עד עכשיו:")
    df = pd.read_csv(DATA_FILE)

    # הוספת כפתור מחיקה ליד כל שורה
    for i in df.index:
        col1, col2 = st.columns([10, 1])
        with col1:
            st.write(df.loc[i].to_dict())
        with col2:
            if st.button("🗑", key=f"delete_{i}"):
                df = df.drop(i).reset_index(drop=True)
                df.to_csv(DATA_FILE, index=False)
                st.success("הרשומה נמחקה בהצלחה.")
                st.experimental_rerun()
