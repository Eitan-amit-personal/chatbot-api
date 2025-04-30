# chat_api.py
from flask import Flask, request, jsonify
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# פרומפט קבוע כדי להגביל המלצות רק לערכות באתר שלך
SYSTEM_PROMPT = """
אתה עוזר להורים לתכנן מסיבת יום הולדת. אתה ממליץ אך ורק על ערכות להפעלה מתוך האתר https://www.t-hafalot.co.il. 
בשום אופן אל תזכיר אתרים אחרים. השאל את ההורים שאלות כדי להבין את הגיל, התחביבים, המקום והכמות.
"""

@app.route("/api/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        max_tokens=600
    )
    reply = response.choices[0].message["content"]
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
