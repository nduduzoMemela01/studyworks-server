from flask import Flask, request, jsonify
import os
import groq
from dotenv import load_dotenv
import uuid
from datetime import datetime

def extract_content(raw_response):
    closing_tag = "</think>\n\n"
    index = raw_response.find(closing_tag)
    
    if index != -1:
        return raw_response[index + len(closing_tag):].strip()
    return raw_response.strip()

# Load API key
load_dotenv()
client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API is live!"})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True)
    
    print(f"Received data: {data}")

    # # Validate request format
    # if not data or "content" not in data:
    #     return jsonify({"error": "Invalid request format"}), 400

    user_message = data["content"]
    
    print(f"User message: {user_message}")

    # Call Groq DeepSeek AI
    response = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=[{"role": "user", "content": user_message}]
    )

    ai_response_content = response.choices[0].message.content
    ai_response_content = extract_content(ai_response_content)
    print(f"AI response content: {ai_response_content}")

    # Construct expected AIResponse format for Android
    ai_response = {
        "responseContent": ai_response_content,
        "timestamp": datetime.utcnow().isoformat()
    }

    return jsonify(ai_response)

if __name__ == "__main__":
    app.run(debug=True)