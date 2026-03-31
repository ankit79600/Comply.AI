import { useState } from 'react';
import { Send, Upload } from 'lucide-react';
import axios from 'axios';

const API_URL = "http://localhost:8000";

export default function UserDashboard() {
  const [messages, setMessages] = useState([]);
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [appealSent, setAppealSent] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [profile, setProfile] = useState({
    name: 'John Doe',
    requestedAmount: '$150,000',
    purpose: 'Home Mortgage',
    zipCode: '10003'
  });

  const sendMessage = async () => {
    if (!prompt.trim()) return;
    
    const newMsg = { role: 'user', content: prompt };
    setMessages([...messages, newMsg]);
    setPrompt('');
    setLoading(true);

    try {
      const res = await axios.post(`${API_URL}/chat`, { message: prompt });
      if (res.status === 200) {
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: res.data.response,
          meta: `Language: ${res.data.detected_language} | SHAP Grounded`
        }]);
      }
    } catch (e) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Connection error: Please ensure FastAPI backend is running.'
      }]);
    }
    setLoading(false);
  };

  return (
    <div className="animate-fade-in">
      <header className="page-header">
        <h1>👤 User Dashboard</h1>
        <p>View your application status and talk to our AI representative.</p>
      </header>

      {/* Metrics Row */}
      <div className="metric-grid">
        <div className="glass-card">
          <div className="metric-value">620</div>
          <div className="metric-label">Credit Score</div>
          <div className="text-secondary mt-2">📉 -15 pts since last check</div>
        </div>
        <div className="glass-card">
          <div className="metric-value text-error">DENIED</div>
          <div className="metric-label">Loan Status</div>
          <div className="text-secondary mt-2">High Risk Assessed</div>
        </div>
        <div className="glass-card">
          <div className="metric-value text-success">Verified</div>
          <div className="metric-label">Income Verification</div>
          <div className="text-secondary mt-2">Records matched successfully</div>
        </div>
      </div>

      <div className="dashboard-layout">
        {/* Left Column: Profile & Appeal */}
        <div className="flex-col">
          <div className="glass-card">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <h3>📋 Application Details</h3>
              <button 
                className="btn btn-secondary" 
                style={{ padding: '4px 12px', fontSize: '0.8rem' }}
                onClick={() => setIsEditing(!isEditing)}
              >
                {isEditing ? 'Save Details' : 'Edit Details'}
              </button>
            </div>
            <div className="mt-4 flex-col" style={{ gap: '0.5rem' }}>
              {isEditing ? (
                <>
                  <input type="text" value={profile.name} onChange={e => setProfile({...profile, name: e.target.value})} placeholder="Name" />
                  <input type="text" value={profile.requestedAmount} onChange={e => setProfile({...profile, requestedAmount: e.target.value})} placeholder="Requested Amount" />
                  <input type="text" value={profile.purpose} onChange={e => setProfile({...profile, purpose: e.target.value})} placeholder="Purpose" />
                  <input type="text" value={profile.zipCode} onChange={e => setProfile({...profile, zipCode: e.target.value})} placeholder="Zip Code" />
                </>
              ) : (
                <>
                  <p><strong>Name:</strong> {profile.name}</p>
                  <p><strong>Requested Amount:</strong> {profile.requestedAmount}</p>
                  <p><strong>Purpose:</strong> {profile.purpose}</p>
                  <p><strong>Zip Code:</strong> {profile.zipCode}</p>
                </>
              )}
            </div>
          </div>

          <div className="glass-card">
            <h3>⚖️ File Appeal</h3>
            <p>Provide additional context for reconsideration:</p>
            <textarea 
              rows={4} 
              placeholder="Why should we reconsider your application?"
              className="mt-4 mb-4"
            ></textarea>
            <button 
              className="btn w-full"
              onClick={() => setAppealSent(true)}
              disabled={appealSent}
            >
              {appealSent ? 'Appeal Submitted ✓' : 'Submit Appeal'}
            </button>
          </div>
        </div>

        {/* Right Column: Chat */}
        <div className="glass-card flex-col">
          <div style={{ marginBottom: '1rem' }}>
            <h3>💬 Ask ComplyAI</h3>
            <p>Find out exactly why decisions were made in everyday language.</p>
          </div>

          <div className="chat-container">
            <div className="chat-history">
              {messages.length === 0 ? (
                <div style={{ margin: 'auto', textAlign: 'center', opacity: 0.5 }}>
                  Send a message to start checking your compliance explanations.
                </div>
              ) : (
                messages.map((msg, i) => (
                  <div key={i} style={{ display: 'flex', flexDirection: 'column' }}>
                    <div className={`chat-bubble ${msg.role}`}>
                      {msg.content}
                    </div>
                    {msg.meta && <small style={{ color: 'var(--text-secondary)', alignSelf: 'flex-start', marginTop: 4, fontSize: '0.75rem' }}>{msg.meta}</small>}
                  </div>
                ))
              )}
              {loading && <div className="chat-bubble assistant">Thinking...</div>}
            </div>

            <div className="chat-input-area mt-4">
              <input 
                type="text" 
                value={prompt}
                onChange={e => setPrompt(e.target.value)}
                onKeyPress={e => e.key === 'Enter' && sendMessage()}
                placeholder="Why was my loan denied? / Mera loan deny kyu hua?" 
              />
              <button className="btn" onClick={sendMessage} disabled={loading || !prompt}>
                <Send size={18} />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
