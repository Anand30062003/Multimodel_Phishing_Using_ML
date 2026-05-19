from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # IMPORTANT for React connection

@app.route("/api/check", methods=["POST"])
def check_phishing():
    url = request.form.get("url")
    text = request.form.get("text")
    image = request.files.get("image")

    # Dummy logic (replace with your AI model)
    result = "PHISHING" if "verify" in (text or "").lower() else "LEGITIMATE"
    score = 85 if result == "PHISHING" else 15

    return jsonify({
        "result": result,
        "score": score,
        "message": "Phishing detection completed"
    })

if __name__ == "__main__":
    app.run(port=8000, debug=True)