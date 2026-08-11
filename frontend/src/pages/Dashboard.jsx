import { useState, useEffect } from 'react';
import api from '../api';
import { Activity, Users, Phone, Zap } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from 'recharts';
import './Dashboard.css';

const mockCallData = [
  { name: 'Mon', calls: 40 },
  { name: 'Tue', calls: 65 },
  { name: 'Wed', calls: 85 },
  { name: 'Thu', calls: 120 },
  { name: 'Fri', calls: 90 },
  { name: 'Sat', calls: 30 },
  { name: 'Sun', calls: 20 },
];

const mockLeadData = [
  { name: 'New', value: 400 },
  { name: 'Contacted', value: 300 },
  { name: 'Qualified', value: 200 },
  { name: 'Converted', value: 100 },
];

const COLORS = ['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b'];

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

      <div className="charts-grid" style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '1.5rem', marginTop: '1.5rem' }}>
        <div className="glass chart-card" style={{ padding: '1.5rem', borderRadius: '12px' }}>
          <h3 style={{ marginBottom: '1.5rem', color: 'var(--text-primary)' }}>Call Volume (Last 7 Days)</h3>
          <div style={{ width: '100%', height: 300 }}>
            <ResponsiveContainer>
              <LineChart data={mockCallData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" />
                <XAxis dataKey="name" stroke="#ffffff50" />
                <YAxis stroke="#ffffff50" />
                <Tooltip contentStyle={{ backgroundColor: 'rgba(15, 23, 42, 0.9)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }} />
                <Line type="monotone" dataKey="calls" stroke="#8b5cf6" strokeWidth={3} dot={{ fill: '#8b5cf6', r: 4 }} activeDot={{ r: 6 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="glass chart-card" style={{ padding: '1.5rem', borderRadius: '12px' }}>
          <h3 style={{ marginBottom: '1.5rem', color: 'var(--text-primary)' }}>Lead Status Breakdown</h3>
          <div style={{ width: '100%', height: 300 }}>
            <ResponsiveContainer>
              <PieChart>
                <Pie
                  data={mockLeadData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {mockLeadData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: 'rgba(15, 23, 42, 0.9)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }} />
                <Legend verticalAlign="bottom" height={36} iconType="circle" />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
