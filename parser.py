# parser.py
import openai
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def parse_entry(text):
    prompt = f"""
    אתה עוזר חקלאי חכם. המשתמש מתאר מה עשה היום בשדה.
    תחלץ מתוך זה:
    - פעולות שביצע
    - זמן עבודה משוער (בשעות)
    - עלות משוערת בש"ח

    החזר תשובה בפורמט JSON. הנה הטקסט:

    "{text}"
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    reply = response.choices[0].message.content

    try:
        parsed = eval(reply)
        parsed["תיאור"] = text
        parsed["תאריך"] = datetime.now().strftime("%Y-%m-%d")
        return parsed
    except Exception as e:
        return {
            "שגיאה": f"שגיאה בניתוח GPT: {e}",
            "תיאור": text,
            "תאריך": datetime.now().strftime("%Y-%m-%d")
        }

