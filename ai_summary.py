# ai_summary.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_ai_summary_and_risks(df):
    prompt = f"""
You're a financial AI assistant. Analyze the following data:

{df.to_string(index=False)}

1. Summarize overall financial performance.
2. Mention any significant trends or changes over time.
3. Identify any risks or red flags (e.g., high debt, losses).
4. Suggest at least 2 improvements.

Write 4 short paragraphs. Be clear and concise.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
        )
        full_response = response.choices[0].message.content
        return full_response, extract_red_flags(full_response)
    except Exception as e:
        return f"AI Summary Error: {e}", ""

def extract_red_flags(text):
    for paragraph in text.split("\n\n"):
        if "risk" in paragraph.lower() or "red flag" in paragraph.lower():
            return paragraph
    return "No critical red flags found."
