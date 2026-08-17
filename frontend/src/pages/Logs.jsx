import React, { useState, useEffect, useRef } from 'react';
import api from '../api';
import { Terminal, Download, RefreshCw } from 'lucide-react';


const Logs = () => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const terminalEndRef = useRef(null);

  const fetchLogs = async (isManual = false) => {
    if (isManual) setIsRefreshing(true);
    try {
      const res = await api.get('/logs');
      setLogs(res.data);
    } catch (error) {
      console.error('Failed to fetch logs', error);
    } finally {
      setLoading(false);
      setIsRefreshing(false);
    }
  };

  useEffect(() => {
    fetchLogs();
    const interval = setInterval(() => fetchLogs(), 10000); // Poll every 10s
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    // Auto-scroll to bottom on new logs
    terminalEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  const getLogColor = (level) => {
    switch ((level || '').toUpperCase()) {
      case 'ERROR': return '#ef4444'; // red
      case 'WARNING': return '#f59e0b'; // yellow
      case 'SUCCESS': return '#10b981'; // green
      case 'INFO': return '#3b82f6'; // blue
      default: return '#9ca3af'; // gray
    }
  };

  const handleExport = () => {
    const textContent = logs.map(l => `[${new Date(l.timestamp || l.created_at).toISOString()}] [${l.level}] ${l.message}`).join('\n');
    const blob = new Blob([textContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `system_logs_${new Date().toISOString().split('T')[0]}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="flex flex-col gap-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <header className="flex justify-between items-start mb-2">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight">System Logs</h1>
          <p className="text-muted mt-1">View real-time system events, errors, and debug information.</p>
        </div>
        <div style={{ display: 'flex', gap: '0.75rem' }}>
          <button className="p-1.5 text-muted hover:text-accent-primary hover:bg-[rgba(139,92,246,0.1)] rounded-lg transition-colors" onClick={() => fetchLogs(true)} disabled={isRefreshing} title="Refresh Logs">
            <RefreshCw size={20} className={isRefreshing ? 'spin' : ''} />
          </button>
          <button className="px-4 py-2 rounded-lg font-medium inline-flex items-center gap-2 glass-panel border border-[rgba(255,255,255,0.08)] text-gray-200 hover:bg-[rgba(255,255,255,0.02)] transition-colors shadow-sm" onClick={handleExport} disabled={logs.length === 0}>
            <Download size={16} /> Export Logs
          </button>
        </div>
      </header>

      <div className="glass-panel rounded-xl shadow-sm border border-[rgba(255,255,255,0.08)] overflow-hidden" style={{ flex: 1, backgroundColor: '#0f172a', padding: '1.5rem', borderRadius: '12px', overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
        
        {loading && logs.length === 0 ? (
          <div className="p-12 text-center text-muted" style={{ margin: 'auto' }}>Connecting to log stream...</div>
        ) : logs.length === 0 ? (
          <div className="p-12 text-center text-muted" style={{ margin: 'auto' }}>
            <Terminal size={48} className="text-muted mt-1" style={{ margin: '0 auto 1rem', opacity: 0.5 }} />
            System is quiet. No logs available.
          </div>
        ) : (
          <div style={{ flex: 1, overflowY: 'auto', fontFamily: '"JetBrains Mono", "Fira Code", monospace', fontSize: '0.875rem', lineHeight: '1.6' }}>
            {logs.map((log, index) => (
              <div key={log.id || index} style={{ display: 'flex', gap: '1rem', borderBottom: '1px solid rgba(255,255,255,0.02)', padding: '0.25rem 0' }}>
                <span style={{ color: 'var(--text-secondary)', minWidth: '160px', opacity: 0.7 }}>
                  {new Date(log.timestamp || log.created_at).toLocaleString()}
                </span>
                <span style={{ color: getLogColor(log.level), minWidth: '80px', fontWeight: 600 }}>
                  [{log.level}]
                </span>
                <span style={{ color: '#e2e8f0', wordBreak: 'break-all' }}>
                  {log.message}
                </span>
              </div>
            ))}
            <div ref={terminalEndRef} />
          </div>
        )}
      </div>
    </div>
  );
};

export default Logs;
