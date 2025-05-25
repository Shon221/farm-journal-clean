import streamlit as st
import pandas as pd
import os
from parser import parse_entry
from journal_utils import save_entry
from datetime import datetime

DATA_FILE = "data/journal.csv"

st.set_page_config(page_title="יומן חקלאי חכם", layout="wide")
st.title("🧠 יומן חקלאי חכם")

# --- קלט משתמש ---
st.markdown("#### מה עשית היום בשטח?")
user_input = st.text_area("רשום כאן את הפעולות שביצעת היום", height=100)
if st.button("✅ נתח ושמור"):
    parsed = parse_entry(user_input)
    save_entry(parsed)
    st.success("✔️ הפעולה נותחה ונשמרה בהצלחה!")
    st.rerun()
# --- הצגת טבלה עם אפשרות מחיקה ---
if os.path.exists(DATA_FILE):
    st.markdown("### 📅 יומן יומי")
    df = pd.read_csv(DATA_FILE)

    # סידור עמודות אם קיימות
    expected_cols = ["תיאור", "פעולות", "הערכת זמן", "תאריך"]
    for col in expected_cols:
        if col not in df.columns:
            df[col] = ""
    df = df[expected_cols]

    # הצגת טבלה עם מחיקה
    for i in df.index:
        cols = st.columns([8, 1])
        with cols[0]:
            st.write(f"**{df.loc[i, 'תאריך']}** — {df.loc[i, 'פעולות']} ({df.loc[i, 'הערכת זמן']})")
            st.caption(df.loc[i, 'תיאור'])
        with cols[1]:
            if st.button("🗑", key=f"delete_{i}"):
                df = df.drop(i).reset_index(drop=True)
                df.to_csv(DATA_FILE, index=False)
                st.success("הרשומה נמחקה בהצלחה.")
                st.rerun()
    # סיכום יומי כולל שעות עבודה
    if len(df) > 0:
        st.markdown("---")
        st.markdown("#### ⏱️ סיכום שעות עבודה")
        hours = df["הערכת זמן"].str.extract(r'(\d+(\.\d+)?)')[0].astype(float)
        st.metric("סה""כ שעות מתועדות", f"{hours.sum():.1f} שעות")

else:
    st.info("היומן עדיין ריק. תתחיל לרשום מה עשית היום!")
