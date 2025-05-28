import os
import groq
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import re

def extract_content(raw_response):
    closing_tag = "</think>\n\n"
    index = raw_response.find(closing_tag)
    
    if index != -1:
        return raw_response[index + len(closing_tag):].strip()
    return raw_response.strip()

load_dotenv()
client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    response = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=[{"role": "user", "content": user_message}]
    )
    
    response = response.choices[0].message.content

    return jsonify({"response": extract_content(response)})

if __name__ == "__main__":
    app.run(debug=True)