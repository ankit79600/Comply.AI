import { useState } from 'react';
import { ShieldCheck, User, Building, Info } from 'lucide-react';
import './App.css';
import BankPortal from './components/BankPortal';
import UserDashboard from './components/UserDashboard';
import About from './components/About';

function App() {
  const [activeTab, setActiveTab] = useState('userDashboard');

  const renderContent = () => {
    switch (activeTab) {
      case 'bankPortal':
        return <BankPortal />;
      case 'userDashboard':
        return <UserDashboard />;
      case 'about':
        return <About />;
      default:
        return <UserDashboard />;
    }
  };

  return (
    <div className="app-container">
      {/* Sidebar Navigation */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <ShieldCheck size={28} color="var(--accent-primary)" />
          <h2>ComplyAI</h2>
        </div>
        
        <nav className="nav-links">
          <button 
            className={`nav-item ${activeTab === 'userDashboard' ? 'active' : ''}`}
            onClick={() => setActiveTab('userDashboard')}
          >
            <User size={20} />
            User Dashboard
          </button>
          <button 
            className={`nav-item ${activeTab === 'bankPortal' ? 'active' : ''}`}
            onClick={() => setActiveTab('bankPortal')}
          >
            <Building size={20} />
            Bank Portal
          </button>
          <button 
            className={`nav-item ${activeTab === 'about' ? 'active' : ''}`}
            onClick={() => setActiveTab('about')}
          >
            <Info size={20} />
            About
          </button>
        </nav>
      </aside>

      {/* Main Content Area */}
      <main className="main-content">
        {renderContent()}
      </main>
    </div>
  );
}

export default App;
