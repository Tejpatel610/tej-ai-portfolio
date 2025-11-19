export default function Navbar() {
  return (
    <header
      style={{
        position: "sticky",
        top: 0,
        zIndex: 50,
        backdropFilter: "blur(18px)",
        background: "rgba(15,23,42,0.85)",
        borderBottom: "1px solid rgba(148,163,184,0.4)",
      }}
    >
      <nav
        style={{
          maxWidth: "1100px",
          margin: "0 auto",
          padding: "0.75rem 1.5rem",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
        }}
      >
        <div style={{ fontWeight: 700, letterSpacing: "0.06em" }}>
          <span style={{ color: "#22c55e" }}>TEJ</span> PATEL
        </div>
        <div style={{ display: "flex", gap: "1rem", fontSize: "0.9rem" }}>
          <a href="#projects">Projects</a>
          <a href="#resume-tool">Resume AI</a>
          <a href="#ai-chat">AI Agent</a>
        </div>
      </nav>
    </header>
  );
}
