import { useState, useEffect } from 'react';
import api from '../api';
import { Activity, Users, Phone, Zap } from 'lucide-react';
import './Dashboard.css';

const Dashboard = () => {
  const [stats, setStats] = useState({
    calls_today: 0,
    active_calls: 0,
    completed_calls: 0,
    avg_duration: "00:00",
    total_leads: 0,
    online_devices: 0,
    conversion_rate_pct: 0,
    ai_agents_active: 1,
    health: 'Checking...'
  });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await api.get('/dashboard/stats');
        setStats({ ...res.data.data, health: 'healthy' });
      } catch (error) {
        setStats(prev => ({ ...prev, health: 'offline' }));
      }
    };
    
    fetchStats();
    // Poll every 5 seconds for live dashboard updates
    const interval = setInterval(fetchStats, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="dashboard-container">
      <header className="page-header">
        <div>
          <h1>Dashboard</h1>
          <p className="text-secondary">Overview of system health and metrics.</p>
        </div>
        <div className="status-badge">
          <span className={`status-dot ${stats.health === 'healthy' ? 'healthy' : 'offline'}`}></span>
          {stats.health}
        </div>
      </header>

      <div className="grid grid-cols-4 stats-grid">
        <div className="glass stat-card">
          <div className="stat-icon bg-blue"><Activity size={24} /></div>
          <div className="stat-content">
            <h3>Active Calls</h3>
            <div className="stat-value">{stats.active_calls}</div>
          </div>
        </div>
        <div className="glass stat-card">
          <div className="stat-icon bg-green"><Phone size={24} /></div>
          <div className="stat-content">
            <h3>Calls Today</h3>
            <div className="stat-value">{stats.calls_today}</div>
          </div>
        </div>
        <div className="glass stat-card">
          <div className="stat-icon bg-purple"><Users size={24} /></div>
          <div className="stat-content">
            <h3>Total Leads</h3>
            <div className="stat-value">{stats.total_leads}</div>
          </div>
        </div>
        <div className="glass stat-card">
          <div className="stat-icon bg-yellow"><Zap size={24} /></div>
          <div className="stat-content">
            <h3>Conversion Rate</h3>
            <div className="stat-value">{stats.conversion_rate_pct}%</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
