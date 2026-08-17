import { Shield } from 'lucide-react';

import { useAuth } from '../context/AuthContext';

const Auth = () => {
  const { user } = useAuth();

  return (
    <div className="flex flex-col gap-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <header className="flex justify-between items-start mb-2">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight">Auth & API</h1>
          <p className="text-muted mt-1">Manage API keys, webhooks, and security settings.</p>
        </div>
      </header>

      <div className="glass-panel rounded-xl shadow-sm border border-[rgba(255,255,255,0.08)] overflow-hidden">
        <div style={{ padding: '2rem' }}>
          <Shield size={48} className="text-primary" style={{ marginBottom: '1rem' }} />
          <h2>Security Settings</h2>
          <p className="text-muted mt-1" style={{ marginTop: '0.5rem', marginBottom: '2rem' }}>
            Current Role: <span className="badge badge-active">{user?.role?.name || 'Unknown'}</span>
          </p>
          
          <div className="settings-section">
            <h3>API Keys</h3>
            <p className="text-muted mt-1" style={{ marginBottom: '1rem', fontSize: '0.875rem' }}>
              API keys allow you to authenticate external services with your AI Caller platform.
            </p>
            <button className="px-4 py-2 rounded-lg font-medium inline-flex items-center gap-2 bg-accent-primary text-white hover:bg-accent-primary/80 transition-colors shadow-sm">Generate New Key</button>
          </div>
          
          <div className="settings-section" style={{ marginTop: '2rem' }}>
            <h3>Webhooks</h3>
            <p className="text-muted mt-1" style={{ marginBottom: '1rem', fontSize: '0.875rem' }}>
              Configure webhooks to receive real-time call and lead updates.
            </p>
            <button className="px-4 py-2 rounded-lg font-medium inline-flex items-center gap-2 glass-panel border border-[rgba(255,255,255,0.08)] text-gray-200 hover:bg-[rgba(255,255,255,0.02)] transition-colors shadow-sm">Configure Webhooks</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Auth;
