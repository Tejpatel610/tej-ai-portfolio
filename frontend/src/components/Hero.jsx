export default function Hero() {
  return (
    <section className="section">
      <div className="card">
        <p style={{ fontSize: "0.85rem", color: "#9ca3af", marginBottom: "0.5rem" }}>
          Winter 2026 · Algonquin College · Web & AI
        </p>
        <h1 style={{ fontSize: "2.2rem", margin: "0 0 0.75rem" }}>
          Full-stack web developer exploring AI-powered interfaces.
        </h1>
        <p style={{ maxWidth: "650px", fontSize: "0.98rem", color: "#d1d5db" }}>
          I build end-to-end web applications using React, Python and modern APIs,
          with a growing focus on LLM-powered tools and agentic workflows.
          This site hosts live demos tailored to the AI Accelerator Hub role.
        </p>
        <div style={{ marginTop: "1.5rem", display: "flex", gap: "0.75rem", flexWrap: "wrap" }}>
          <a href="#projects" className="button">
            View featured projects
          </a>
          <a
            href="https://github.com/Tejpatel610"
            target="_blank"
            rel="noreferrer"
            style={{ fontSize: "0.9rem", textDecoration: "underline", color: "#a5b4fc" }}
          >
            GitHub · Code history
          </a>
        </div>
      </div>
    </section>
  );
}
