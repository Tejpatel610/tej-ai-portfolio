const API_BASE = "https://tej-ai-portfolio.onrender.com";

import { useState } from "react";
import axios from "axios";

export default function AIChat() {
  const [messages, setMessages] = useState([
    { role: "system", content: "Ask me about Tej's projects, tech stack, or study questions." },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const sendMessage = async () => {
  if (!input.trim()) return;
  const newMessages = [...messages, { role: "user", content: input }];
  setMessages(newMessages);
  setInput("");
  setLoading(true);
  setError("");

  try {
    const response = await axios.post(`${API_BASE}/api/chat`, {
      messages: newMessages,
    });
    const reply = response.data.reply || "I couldn't generate a response.";
    setMessages([...newMessages, { role: "assistant", content: reply }]);
  } catch (err) {
    console.error(err);
    setError("Backend is not responding. Check if the server is up.");
  } finally {
    setLoading(false);
  }
};


  return (
    <div className="card">
      <h2 style={{ marginTop: 0 }}>AI agent for students & project Q&A</h2>
      <p style={{ fontSize: "0.95rem", color: "#d1d5db" }}>
        Prototype conversational agent designed to answer questions about my projects,
        technologies I use, and common student topics.
      </p>

      <div
        style={{
          marginTop: "1rem",
          maxHeight: "280px",
          overflowY: "auto",
          padding: "0.75rem",
          borderRadius: "0.75rem",
          background: "rgba(15,23,42,0.9)",
        }}
      >
        {messages
          .filter((m) => m.role !== "system")
          .map((m, idx) => (
            <div
              key={idx}
              style={{
                marginBottom: "0.6rem",
                textAlign: m.role === "user" ? "right" : "left",
              }}
            >
              <div
                style={{
                  display: "inline-block",
                  padding: "0.35rem 0.7rem",
                  borderRadius: "0.75rem",
                  background:
                    m.role === "user"
                      ? "rgba(34,197,94,0.15)"
                      : "rgba(148,163,184,0.15)",
                  fontSize: "0.9rem",
                }}
              >
                {m.content}
              </div>
            </div>
          ))}
      </div>

      <div style={{ marginTop: "0.75rem", display: "flex", gap: "0.5rem" }}>
        <input
          className="input"
          placeholder="Ask about my stack, projects, or student life..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button className="button" onClick={sendMessage} disabled={loading}>
          {loading ? "Thinking..." : "Send"}
        </button>
      </div>
      {error && (
        <p style={{ color: "#fca5a5", fontSize: "0.9rem", marginTop: "0.4rem" }}>
          {error}
        </p>
      )}
    </div>
  );
}
