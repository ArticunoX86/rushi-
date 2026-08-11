import { Shield } from 'lucide-react';
import './Shared.css';
import { useAuth } from '../context/AuthContext';

const Auth = () => {
  const { user } = useAuth();

  return (
    <div className="page-container">
      <header className="page-header">
        <div>
          <h1>Auth & API</h1>
          <p className="text-secondary">Manage API keys, webhooks, and security settings.</p>
        </div>
      </header>

      <div className="glass table-container">
        <div style={{ padding: '2rem' }}>
          <Shield size={48} className="text-primary" style={{ marginBottom: '1rem' }} />
          <h2>Security Settings</h2>
          <p className="text-secondary" style={{ marginTop: '0.5rem', marginBottom: '2rem' }}>
            Current Role: <span className="badge badge-active">{user?.role?.name || 'Unknown'}</span>
          </p>
          
          <div className="settings-section">
            <h3>API Keys</h3>
            <p className="text-secondary" style={{ marginBottom: '1rem', fontSize: '0.875rem' }}>
              API keys allow you to authenticate external services with your AI Caller platform.
            </p>
            <button className="btn btn-primary">Generate New Key</button>
          </div>
          
          <div className="settings-section" style={{ marginTop: '2rem' }}>
            <h3>Webhooks</h3>
            <p className="text-secondary" style={{ marginBottom: '1rem', fontSize: '0.875rem' }}>
              Configure webhooks to receive real-time call and lead updates.
            </p>
            <button className="btn btn-secondary">Configure Webhooks</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Auth;
