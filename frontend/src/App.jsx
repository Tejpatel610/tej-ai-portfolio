import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import Projects from "./components/Projects";
import ResumeAnalyzer from "./components/ResumeAnalyzer";
import AIChat from "./components/AIChat";
import Footer from "./components/Footer";

export default function App() {
  return (
    <>
      <Navbar />
      <main>
        <Hero />
        <Projects />
        <section id="resume-tool" className="section">
          <ResumeAnalyzer />
        </section>
        <section id="ai-chat" className="section">
          <AIChat />
        </section>
      </main>
      <Footer />
    </>
  );
}
