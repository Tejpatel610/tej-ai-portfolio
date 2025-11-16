function ProjectCard({ title, tech, description, link }) {
  return (
    <div className="card" style={{ height: "100%" }}>
      <h3 style={{ marginTop: 0 }}>{title}</h3>
      <p style={{ fontSize: "0.85rem", color: "#9ca3af" }}>{tech}</p>
      <p style={{ fontSize: "0.95rem" }}>{description}</p>
      {link && (
        <a
          href={link}
          target="_blank"
          rel="noreferrer"
          style={{ fontSize: "0.9rem", textDecoration: "underline", color: "#a5b4fc" }}
        >
          View code
        </a>
      )}
    </div>
  );
}

export default function Projects() {
  return (
    <section id="projects" className="section">
      <h2 style={{ fontSize: "1.6rem", marginBottom: "1rem" }}>Featured work</h2>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
          gap: "1rem",
        }}
      >
        <ProjectCard
          title="AI-powered resume & job match analyzer"
          tech="React · Flask · REST · JSON · LLM API"
          description="Upload a resume and a job posting to get a structured match score, missing-skills analysis, and tailored suggestions."
        />
        <ProjectCard
          title="Student AI helper agent"
          tech="React · Python · Chat endpoint"
          description="Conversational agent prototype that answers common student questions and surfaces relevant links and resources."
        />
        <ProjectCard
          title="Web development projects (coursework & labs)"
          tech="HTML · CSS · JS · Python · Git"
          description="Selection of assignments and labs showcasing component-based UIs, database access, and unit testing."
          link="https://github.com/Tejpatel610"
        />
      </div>
    </section>
  );
}
