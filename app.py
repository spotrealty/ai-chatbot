from flask import Flask, request, jsonify
import openai
import os

# Initialize Flask app
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "AI Chatbot is running!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Get OpenAI API key from environment variables
        openai_api_key = os.getenv("OPENAI_API_KEY")

        if not openai_api_key:
            return jsonify({"error": "OpenAI API key is missing"}), 500

        # Create OpenAI client
        client = openai.OpenAI(api_key=openai_api_key)

        # Call OpenAI's latest API format
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful real estate assistant."},
                {"role": "user", "content": user_message}
            ]
        )

        # Extract response correctly
        bot_reply = response.choices[0].message.content

        return jsonify({"reply": bot_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render’s dynamic port
    app.run(host="0.0.0.0", port=port)
