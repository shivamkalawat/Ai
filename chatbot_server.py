from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests

app = Flask(__name__, static_folder="frontend", static_url_path="")
CORS(app)

# Serve index.html at root
@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

# Your Together API chat route
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    response = requests.post(
        "https://api.together.xyz/v1/chat/completions",
        headers={
            "Authorization": f"7fa95995b057444430ffdc95993b6c04be59554cea7ae059db0a81b6c09a49f7",
            "Content-Type": "application/json"
        },
        json={
            "model": "meta-llama/Llama-3-8b-chat-hf",
            "messages": [{"role": "user", "content": user_message}]
        }
    )

    try:
        reply = response.json()["choices"][0]["message"]["content"]
    except:
        reply = "Sorry, something went wrong."

    return jsonify({"reply": reply})
