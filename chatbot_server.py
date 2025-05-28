from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import requests

app = Flask(__name__, static_folder="frontend", static_url_path="")
CORS(app)

TOGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY")
TOGETHER_MODEL = "meta-llama/Llama-3-8b-chat-hf"
@app.route("/")
def home():
    return "Backend is running"

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    res = requests.post(
        "https://api.together.xyz/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {7fa95995b057444430ffdc95993b6c04be59554cea7ae059db0a81b6c09a49f7}",
            "Content-Type": "application/json"
        },
        json={
            "model": TOGETHER_MODEL,
            "messages": [{"role": "user", "content": user_message}],
            "temperature": 0.7
        }
    )

    res_json = res.json()
    print("API response:", res_json)  # Debug print

    try:
        reply = res_json["choices"][0]["message"]["content"]
    except Exception as e:
        print("Error extracting reply:", e)
        reply = "Sorry, something went wrong."

    return jsonify({ "reply": reply })
