import os
from openai import OpenAI, RateLimitError
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def parse_entry(text):
    prompt = f"""
    אתה עוזר חקלאי חכם. המשתמש מתאר מה עשה היום בשטח.
    תחלץ מתוך זה:
    - רשימת פעולות
    - זמן עבודה משוער (בשעות)
    - עלות משוערת (בש"ח)

    החזר תשובה בפורמט JSON בלבד.

    הטקסט הוא:
    "{text}"
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        reply = response.choices[0].message.content

        parsed = eval(reply)
        parsed["תיאור"] = text
        parsed["תאריך"] = datetime.now().strftime("%Y-%m-%d")
        return parsed

    except RateLimitError:
        return {
            "שגיאה": "חרגת ממכסת השימוש במפתח OpenAI. נסה שוב בעוד מספר דקות.",
            "תיאור": text,
            "תאריך": datetime.now().strftime("%Y-%m-%d")
        }

    except Exception as e:
        return {
            "שגיאה": f"שגיאה בלתי צפויה: {e}",
            "תיאור": text,
            "תאריך": datetime.now().strftime("%Y-%m-%d")
        }
