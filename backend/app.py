from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/api/analyze-resume", methods=["POST"])
def analyze_resume():
    data = request.get_json() or {}
    resume = data.get("resume", "").lower()
    job = data.get("job", "").lower()

    if not resume or not job:
        return jsonify({"error": "resume and job fields are required"}), 400

    # super simple keyword-based scoring (no external AI, works on Render)
    score = 50
    bonuses = 0

    keywords = [
        "react",
        "javascript",
        "python",
        "flask",
        "django",
        "api",
        "json",
        "git",
        "linux",
        "ai",
        "llm",
        "cloud",
    ]

    for kw in keywords:
        if kw in resume and kw in job:
            bonuses += 3

    score = min(90, score + bonuses)

    strengths = []
    improvements = []

    for kw in ["react", "javascript", "python", "flask", "django"]:
        if kw in resume:
            strengths.append(kw)
        elif kw in job:
            improvements.append(kw)

    strengths_text = (
        "Mentions: " + ", ".join(sorted(set(strengths)))
        if strengths
        else "General web dev skills."
    )
    improvements_text = (
        "Consider adding: " + ", ".join(sorted(set(improvements)))
        if improvements
        else "You already mention most of the core technologies from the posting."
    )

    summary = (
        "Heuristic resume analysis without external AI. "
        "Score is based on overlapping keywords between the resume and job posting."
    )

    return jsonify(
        {
            "match_score": score,
            "summary": summary,
            "strengths": strengths_text,
            "improvements": improvements_text,
        }
    )


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    messages = data.get("messages", [])

    if not isinstance(messages, list) or not messages:
        return jsonify({"error": "messages field must be a non-empty list"}), 400

    # get last user message
    last_user = ""
    for m in reversed(messages):
        if m.get("role") == "user":
            last_user = m.get("content", "")
            break

    text = last_user.lower()

    # simple rule-based responses (no external AI, works on Render)
    if "stack" in text or "tech" in text:
        reply = (
            "Tej mainly works with React, JavaScript, Python, Flask, Git, and basic cloud platforms. "
            "He also has growing experience with AI/LLM-powered tools."
        )
    elif "project" in text:
        reply = (
            "This portfolio showcases an AI-powered resume analyzer and a student Q&A agent, "
            "built with a React frontend and a Python/Flask backend."
        )
    elif "ai" in text or "llm" in text:
        reply = (
            "This deployment uses a simple rules-based backend, but the local version of the project "
            "is wired to experiment with LLMs via a separate environment."
        )
    else:
        reply = (
            "Hi! I'm a lightweight assistant running on Tej's portfolio backend. "
            "Ask me about his tech stack, projects, or experience as a student developer."
        )

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)