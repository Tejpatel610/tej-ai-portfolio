import os
import json
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# You can override these via environment variables later if you want
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")


def call_ollama_chat(messages, expect_json=False):
    """
    Helper to call the local Ollama /api/chat endpoint.
    If expect_json=True, we ask the model to return JSON and try to parse it.
    """
    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False,  # single JSON response instead of stream :contentReference[oaicite:2]{index=2}
    }

    # When expect_json is True, we tell Ollama to format the response as JSON
    if expect_json:
        payload["format"] = "json"  # Ollama can enforce JSON formatting :contentReference[oaicite:3]{index=3}

    try:
        resp = requests.post(
            f"{OLLAMA_BASE_URL}/api/chat", json=payload, timeout=60
        )
        resp.raise_for_status()
    except requests.RequestException as e:
        print("Error calling Ollama:", e)
        raise

    data = resp.json()
    content = data.get("message", {}).get("content", "")

    if expect_json:
        # content itself should be valid JSON when format="json"
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Fallback if the model returns something weird
            print("Failed to parse JSON from model, raw content:", content)
            return None

    return content


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/api/analyze-resume", methods=["POST"])
def analyze_resume():
    payload = request.get_json() or {}
    resume = payload.get("resume", "").strip()
    job = payload.get("job", "").strip()

    if not resume or not job:
        return jsonify({"error": "resume and job fields are required"}), 400

    system_message = {
        "role": "system",
        "content": (
            "You are an assistant helping a student tailor their resume to a job posting. "
            "Analyze the resume against the job description and respond ONLY as JSON "
            "with the following keys:\n"
            "match_score (integer 0-100),\n"
            "summary (short string),\n"
            "strengths (short string),\n"
            "improvements (short string).\n"
            "Do not include any extra keys or text."
        ),
    }

    user_message = {
        "role": "user",
        "content": (
            f"JOB POSTING:\n{job}\n\n"
            f"RESUME:\n{resume}\n\n"
            "Now provide the JSON analysis."
        ),
    }

    try:
        result = call_ollama_chat(
            [system_message, user_message],
            expect_json=True,
        )
    except Exception:
        return jsonify(
            {
                "error": "Failed to contact local AI model. Is Ollama running?",
            }
        ), 500

    # If JSON parsing failed, fall back to a simple heuristic
    if not isinstance(result, dict):
        return jsonify(
            {
                "match_score": 60,
                "summary": "AI analysis failed to return valid JSON; using fallback.",
                "strengths": "Shows relevant technical and academic experience.",
                "improvements": "Explicitly mention AI, LLMs, React, and cloud projects.",
            }
        )

    # Safely pull fields with defaults
    match_score = int(result.get("match_score", 65))
    summary = result.get("summary", "No summary provided.")
    strengths = result.get("strengths", "No strengths provided.")
    improvements = result.get("improvements", "No improvements provided.")

    return jsonify(
        {
            "match_score": match_score,
            "summary": summary,
            "strengths": strengths,
            "improvements": improvements,
        }
    )


@app.route("/api/chat", methods=["POST"])
def chat():
    payload = request.get_json() or {}
    messages = payload.get("messages", [])

    if not isinstance(messages, list) or not messages:
        return jsonify({"error": "messages field must be a non-empty list"}), 400

    # Add a system prompt at the beginning to steer the assistant
    system_prompt = {
        "role": "system",
        "content": (
            "You are an AI assistant embedded in Tej Patel's portfolio website. "
            "Answer questions about his skills, projects, and general programming or "
            "student life. Keep answers concise and friendly."
        ),
    }

    # Ensure the system prompt is the first message
    ollama_messages = [system_prompt] + [
        m for m in messages if m.get("role") in ("user", "assistant")
    ]

    try:
        reply_text = call_ollama_chat(ollama_messages, expect_json=False)
    except Exception:
        return jsonify(
            {
                "reply": "I couldn't reach the local AI model. "
                "Please make sure Ollama is running."
            }
        ), 500

    return jsonify({"reply": reply_text})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
