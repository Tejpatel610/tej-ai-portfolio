from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import os

app = Flask(__name__)
CORS(app)

# Groq API settings
GROQ_MODEL = "llama-3.1-8b-instant"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


def call_groq(messages, temperature=0.7):
    """
    Call Groq chat completion API with given messages.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set in environment variables")

    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": temperature,
    }

    try:
        response = requests.post(
            GROQ_API_URL,
            headers={"Authorization": f"Bearer {api_key}"},
            json=payload,
            timeout=20,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        print("Groq API error:", e)
        raise


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Chat endpoint for your AI assistant on the portfolio website.
    Always returns 200, even if Groq fails, so frontend never breaks.
    """
    data = request.get_json() or {}
    messages = data.get("messages", [])

    if not isinstance(messages, list) or not messages:
        return jsonify({"error": "messages field must be a non-empty list"}), 400

    # System message injected BEFORE user messages
    system_msg = {
        "role": "system",
        "content": (
            "You are an AI assistant embedded in Tej Patel's developer portfolio. "
            "You explain his projects, tech stack, experience, and student life at "
            "Algonquin College. Keep answers friendly, concise, and helpful."
        ),
    }

    groq_messages = [system_msg]

    # Forward messages from frontend
    for m in messages:
        role = m.get("role")
        content = m.get("content", "")
        if role in ("user", "assistant") and content:
            groq_messages.append({"role": role, "content": content})

    # Try calling Groq
    try:
        reply_text = call_groq(groq_messages)
        return jsonify({"reply": reply_text}), 200

    # If Groq fails → return safe fallback so UI doesn't break
    except Exception as e:
        print("Groq API error in /api/chat:", e)
        fallback_reply = (
            "I'm having trouble reaching the cloud AI service right now, "
            "but here's something about Tej: He works with React, JavaScript, Python, "
            "Flask, REST APIs, SQL, and Git, and studies at Algonquin College. "
            "Ask me anything about his projects!"
        )
        return jsonify({"reply": fallback_reply}), 200


@app.route("/api/analyze-resume", methods=["POST"])
def analyze_resume():
    """
    Resume analysis using Groq — returns structured JSON.
    """
    data = request.get_json() or {}
    resume = data.get("resume", "")
    job = data.get("job", "")

    if not resume or not job:
        return jsonify({"error": "resume and job fields are required"}), 400

    system_msg = {
        "role": "system",
        "content": (
            "You are a resume analysis assistant. Compare the resume to the job posting. "
            "Respond ONLY with a JSON object in this structure:\n"
            "{\n"
            '  "match_score": number (0-100),\n'
            '  "summary": string,\n'
            '  "strengths": string,\n'
            '  "improvements": string\n'
            "}\n"
            "Do not include backticks, markdown, or extra text."
        ),
    }

    user_msg = {
        "role": "user",
        "content": (
            f"JOB POSTING:\n{job}\n\nRESUME:\n{resume}\n\n"
            "Return ONLY the JSON now."
        ),
    }

    try:
        content = call_groq([system_msg, user_msg], temperature=0.1)
        result = json.loads(content)
        return jsonify(result), 200

    except Exception as e:
        print("Groq error in analyze-resume:", e)
        # safe fallback JSON
        return jsonify(
            {
                "match_score": 60,
                "summary": "Fallback analysis used. AI JSON output was invalid or unavailable.",
                "strengths": "Some relevant technical experience is visible.",
                "improvements": "Add clearer alignment with job keywords.",
            }
        ), 200


if __name__ == "__main__":
    # Local development
    app.run(host="0.0.0.0", port=5000, debug=True)
