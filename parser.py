import os
import openai
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def parse_entry(text):
    prompt = f"""
    אתה עוזר חקלאי חכם. המשתמש מתאר מה עשה היום בשטח.
    תחלץ מתוך זה:
    - רשימת פעולות
    - זמן עבודה משוער
    - עלות משוערת
    החזר תשובה בפורמט JSON בלבד.

    טקסט: "{text}"
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
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
