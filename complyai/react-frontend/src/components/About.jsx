import { Info, Code2, Shield, Search } from 'lucide-react';

export default function About() {
  return (
    <div className="animate-fade-in" style={{ maxWidth: '800px', margin: '0 auto' }}>
      <header className="page-header" style={{ textAlign: 'center' }}>
        <Info size={48} color="var(--accent-primary)" style={{ marginBottom: '1rem' }} />
        <h1>ℹ️ About ComplyAI</h1>
        <p>Building the future of fair and explainable banking.</p>
      </header>

      <div className="glass-card mb-4" style={{ padding: '3rem' }}>
        <h2>The Problem</h2>
        <p style={{ fontSize: '1.1rem', lineHeight: '1.8' }}>
          As banks embrace AI for credit decisions, they risk violating compliance laws like the <strong>Fair Lending Act</strong>.
          Black-box models often carry hidden biases (e.g., proxying race through zip codes) that lead to unfair denials. Let's fix this.
        </p>

        <h2 style={{ marginTop: '2rem' }}>The Solution: ComplyAI Sandbox</h2>
        <p style={{ marginBottom: '2rem' }}>
          ComplyAI is an end-to-end MVP for AI Governance in financial services.
        </p>

        <div className="grid" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
          <div style={{ padding: '1.5rem', background: 'rgba(255,255,255,0.02)', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
            <h4 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}><Code2 size={20} color="var(--accent-primary)"/> Backend Architecture</h4>
            <p className="mt-4" style={{ margin: 0 }}>FastAPI, SQLite, SQLAlchemy. Robust API for model management.</p>
          </div>
          <div style={{ padding: '1.5rem', background: 'rgba(255,255,255,0.02)', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
            <h4 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}><Search size={20} color="var(--success)"/> Frontend Interface</h4>
            <p className="mt-4" style={{ margin: 0 }}>React + Vite. A highly dynamic, glassmorphic UX mapping complex data smoothly.</p>
          </div>
          <div style={{ padding: '1.5rem', background: 'rgba(255,255,255,0.02)', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
            <h4 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}><Shield size={20} color="var(--error)"/> AI Engine</h4>
            <p className="mt-4" style={{ margin: 0 }}>Scikit-Learn RandomForest + SHAP. Extract transparent insights from complex trees.</p>
          </div>
          <div style={{ padding: '1.5rem', background: 'rgba(255,255,255,0.02)', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
            <h4 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}><Info size={20} color="var(--accent-hover)"/> Core Features</h4>
            <p className="mt-4" style={{ margin: 0 }}>Automated compliance tests, PDF reports, Bilingual (English/Hindi) Chatbot.</p>
          </div>
        </div>

        <div style={{ textAlign: 'center', marginTop: '3rem', color: 'var(--text-secondary)' }}>
          <p><em>Built for a 3-Day Hackathon.</em></p>
        </div>
      </div>
    </div>
  );
}
