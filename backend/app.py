from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import json

app = Flask(__name__)
CORS(app)

GROQ_MODEL = "llama-3.1-8b-instant"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


def call_groq(messages, temperature=0.7):
    """
    Call Groq chat completion API with given messages.
    messages: list of {"role": "user"|"assistant"|"system", "content": "..."}
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set")

    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": temperature,
    }

    resp = requests.post(
        GROQ_API_URL,
        headers={"Authorization": f"Bearer {api_key}"},
        json=payload,
        timeout=20,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"]


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/api/analyze-resume", methods=["POST"])
def analyze_resume():
    data = request.get_json() or {}
    resume = data.get("resume", "")
    job = data.get("job", "")

    if not resume or not job:
        return jsonify({"error": "resume and job fields are required"}), 400

    system_msg = {
        "role": "system",
        "content": (
            "You are a resume analysis assistant helping a student tailor their resume "
            "for a specific job posting. You must ONLY respond with valid JSON using "
            "this schema:\n"
            "{\n"
            '  \"match_score\": number between 0 and 100,\n'
            '  \"summary\": string,\n'
            '  \"strengths\": string,\n'
            '  \"improvements\": string\n'
            "}\n"
            "Do not include markdown, backticks, or any additional text."
        ),
    }

    user_msg = {
        "role": "user",
        "content": f"JOB POSTING:\n{job}\n\nRESUME:\n{resume}\n\nReturn only the JSON now.",
    }

    try:
        content = call_groq([system_msg, user_msg], temperature=0.1)
        result = json.loads(content)
    except (RuntimeError, requests.RequestException) as e:
        print("Groq API error in analyze-resume:", e)
        return jsonify({"error": "AI analysis backend error"}), 500
    except json.JSONDecodeError:
        print("Failed to parse JSON from Groq for analyze-resume")
        # simple safe fallback
        return jsonify(
            {
                "match_score": 65,
                "summary": "Fallback heuristic because AI JSON parsing failed.",
                "strengths": "Mentions some relevant technical and academic experience.",
                "improvements": "Add clearer links between skills and job posting keywords.",
            }
        )

    # sanity defaults
    match_score = int(result.get("match_score", 70))
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
    data = request.get_json() or {}
    messages = data.get("messages", [])

    if not isinstance(messages, list) or not messages:
        return jsonify({"error": "messages field must be a non-empty list"}), 400

    # Add a system message to shape the assistant's personality
    system_msg = {
        "role": "system",
        "content": (
            "You are an AI assistant embedded in Tej Patel's developer portfolio website. "
            "You help answer questions about Tej's skills, projects, experience as an "
            "Algonquin College student, and beginner-friendly programming questions. "
            "Keep answers concise, friendly, and encouraging."
        ),
    }

    groq_messages = [system_msg]

    # forward through user/assistant messages from frontend
    for m in messages:
        role = m.get("role")
        content = m.get("content", "")
        if role in ("user", "assistant") and content:
            groq_messages.append({"role": role, "content": content})

    try:
        reply_text = call_groq(groq_messages, temperature=0.7)
    except (RuntimeError, requests.RequestException) as e:
        print("Groq API error in chat:", e)
        return jsonify(
            {
                "reply": (
                    "I'm having trouble reaching the cloud AI service right now. "
                    "Please try again in a moment."
                )
            }
        ), 500

    return jsonify({"reply": reply_text})


if __name__ == "__main__":
    # local dev only; Render will use gunicorn
    app.run(host="0.0.0.0", port=5000, debug=True)
