import os
from flask import Flask, request, jsonify, send_from_path
import google.generativeai as genai
from dotenv import load_dotenv
from data_manager import DataManager

# Load environment variables from .env if present
load_dotenv()

app = Flask(__name__, static_folder=".")

# Embed the default fallback key (matching index.html) to keep it running out-of-the-box
DEFAULT_API_KEY = "AIzaSyCEIeNfyQFj_wG0tiXf7wNXx-wX5sDs1qo"
API_KEY = os.environ.get("GEMINI_API_KEY", DEFAULT_API_KEY)

# Configure Gemini
genai.configure(api_key=API_KEY)

# Load dynamic database content
data_manager = DataManager()
SYSTEM_INSTRUCTION = data_manager.generate_system_instruction()

@app.route("/")
def serve_frontend():
    return send_from_path(".", "index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data or "contents" not in data:
            return jsonify({"error": "Missing 'contents' in request body"}), 400
        
        contents = data["contents"]
        
        # Initialize Gemini 2.0 Flash (latest recommended model)
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            system_instruction=SYSTEM_INSTRUCTION
        )
        
        response = model.generate_content(contents)
        
        return jsonify({
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {"text": response.text}
                        ]
                    }
                }
            ]
        })
    except Exception as e:
        app.logger.error(f"Error calling Gemini: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "127.0.0.1")
    print(f"IETE-SF Chatbot backend running on http://{host}:{port}")
    app.run(host=host, port=port, debug=True)
