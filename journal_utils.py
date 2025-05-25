# journal_utils.py
import pandas as pd
import os

FILE_PATH = "data/journal.csv"

def save_entry(entry):
    # הפוך ל־DataFrame עם עמודות קבועות
    df = pd.DataFrame([{
        "תאריך": entry.get("תאריך", ""),
        "תיאור": entry.get("תיאור", ""),
        "פעולות": ", ".join(entry.get("פעולות", [])),
        "הערכת זמן": entry.get("הערכת זמן", ""),
        "עלות משוערת": entry.get("עלות משוערת", "")
    }])

    # ודא שהתיקייה קיימת
    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)

    # אם הקובץ כבר קיים – הוסף שורה בלי כותרת, אחרת צור קובץ עם כותרת
    if os.path.exists(FILE_PATH):
        df.to_csv(FILE_PATH, mode='a', header=False, index=False)
    else:
        df.to_csv(FILE_PATH, mode='w', header=True, index=False)
# journal_utils.py
import pandas as pd
from datetime import datetime
import os

FILE_PATH = "data/journal.csv"

def save_entry(entry):
    df = pd.DataFrame([entry])
    if os.path.exists(FILE_PATH):
        df.to_csv(FILE_PATH, mode='a', header=False, index=False)
    else:
        df.to_csv(FILE_PATH, index=False)
