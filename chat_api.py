from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app, supports_credentials=True)

SYSTEM_PROMPT = """
אתה עוזר להורים לתכנן מסיבת יום הולדת. אתה ממליץ אך ורק על ערכות מתוך האתר https://www.t-hafalot.co.il.
בשום אופן אל תזכיר אתרים חיצוניים. השאל את ההורים שאלות כדי להבין את הגיל, התחביבים, המקום והכמות.
"""

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    return response

@app.route("/api/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        # תשובה ידנית ל־preflight
        response = make_response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        return response

    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"reply": "שגיאה: לא התקבל טקסט מהמשתמש"}), 400

    try:
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
    except Exception as e:
        return jsonify({"reply": f"שגיאה בשרת: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
