import { useState } from "react";
import axios from "axios";

export default function ResumeAnalyzer() {
  const [resumeText, setResumeText] = useState("");
  const [jobText, setJobText] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleAnalyze = async () => {
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const response = await axios.post("http://127.0.0.1:5000/api/analyze-resume", {
        resume: resumeText,
        job: jobText,
      });
      setResult(response.data);
    } catch (err) {
      console.error(err);
      setError("Something went wrong talking to the backend. Is Flask running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2 style={{ marginTop: 0 }}>AI resume & job match analyzer</h2>
      <p style={{ fontSize: "0.95rem", color: "#d1d5db" }}>
        Paste your resume and the AI Hub job posting to get a structured analysis of your match,
        missing skills, and wording suggestions.
      </p>

      <div style={{ display: "grid", gap: "1rem", marginTop: "1rem" }}>
        <div>
          <label style={{ fontSize: "0.85rem" }}>Resume text</label>
          <textarea
            className="textarea"
            rows={5}
            value={resumeText}
            onChange={(e) => setResumeText(e.target.value)}
            placeholder="Paste your resume here..."
          />
        </div>
        <div>
          <label style={{ fontSize: "0.85rem" }}>Job posting</label>
          <textarea
            className="textarea"
            rows={5}
            value={jobText}
            onChange={(e) => setJobText(e.target.value)}
            placeholder="Paste the AI Accelerator Hub posting or another job ad here..."
          />
        </div>
        <div>
          <button className="button" onClick={handleAnalyze} disabled={loading}>
            {loading ? "Analyzing..." : "Analyze match"}
          </button>
        </div>
        {error && (
          <p style={{ color: "#fca5a5", fontSize: "0.9rem" }}>
            {error}
          </p>
        )}
        {result && (
          <div
            style={{
              marginTop: "1rem",
              padding: "1rem",
              borderRadius: "0.75rem",
              background: "rgba(15,23,42,0.9)",
            }}
          >
            <p><strong>Match score:</strong> {result.match_score}%</p>
            <p><strong>Summary:</strong> {result.summary}</p>
            <p><strong>Key strengths:</strong> {result.strengths}</p>
            <p><strong>Suggested improvements:</strong> {result.improvements}</p>
          </div>
        )}
      </div>
    </div>
  );
}
