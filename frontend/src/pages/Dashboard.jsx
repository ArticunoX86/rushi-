import { useState, useEffect } from 'react';
import api from '../api';
import { Activity, Users, Phone, Zap } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from 'recharts';
import { motion } from 'framer-motion';
import WelcomeBanner from '../components/WelcomeBanner';

const COLORS = ['#8B5CF6', '#3B82F6', '#10B981', '#F59E0B']; // Matching our CSS variables

const containerVariants = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.1 }
  }
};

const itemVariants = {
  hidden: { y: 20, opacity: 0 },
  show: { y: 0, opacity: 1, transition: { type: "spring", stiffness: 300, damping: 24 } }
};

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
    health: 'Checking...',
    chart_data: [],
    lead_breakdown: []
  });
  const [dateFilter, setDateFilter] = useState('today');

  const getDateRange = () => {
    const end = new Date();
    let start = new Date();
    if (dateFilter === '7days') {
      start.setDate(end.getDate() - 7);
    } else if (dateFilter === '30days') {
      start.setDate(end.getDate() - 30);
    } else if (dateFilter === 'all') {
      start = new Date(2020, 0, 1);
    }
    
    return {
      start_date: start.toISOString().split('T')[0],
      end_date: end.toISOString().split('T')[0]
    };
  };

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const { start_date, end_date } = getDateRange();
        const res = await api.get(`/dashboard/stats?start_date=${start_date}&end_date=${end_date}`);
        setStats({ ...res.data.data, health: 'healthy' });
      } catch (error) {
        setStats(prev => ({ ...prev, health: 'offline' }));
      }
    };
    
    fetchStats();
    // Poll every 5 seconds for live dashboard updates
    const interval = setInterval(fetchStats, 5000);
    return () => clearInterval(interval);
  }, [dateFilter]);

  const customTooltipStyle = {
    backgroundColor: 'rgba(19, 23, 34, 0.9)',
    border: '1px solid rgba(255, 255, 255, 0.08)',
    borderRadius: '12px',
    boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.5)',
    color: '#fff',
    backdropFilter: 'blur(10px)',
    padding: '12px',
  };

  return (
    <motion.div 
      initial="hidden" 
      animate="show" 
      variants={containerVariants} 
      className="space-y-8"
    >
      <header className="flex flex-col sm:flex-row justify-between items-start sm:items-center pb-4 border-b border-[rgba(255,255,255,0.08)] gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-gradient">Dashboard</h1>
          <p className="text-muted mt-1">Overview of system health and AI performance.</p>
        </div>
        <div className="flex items-center gap-4">
          <select 
            className="bg-[rgba(19,23,34,0.6)] border border-[rgba(255,255,255,0.08)] text-white text-sm rounded-lg focus:ring-accent-primary focus:border-accent-primary block w-full py-2.5 pl-4 pr-10 shadow-sm outline-none transition-colors"
            value={dateFilter}
            onChange={(e) => setDateFilter(e.target.value)}
          >
            <option value="today" className="bg-[#131722]">Today</option>
            <option value="7days" className="bg-[#131722]">Last 7 Days</option>
            <option value="30days" className="bg-[#131722]">Last 30 Days</option>
            <option value="all" className="bg-[#131722]">All Time</option>
          </select>
          <div className="flex items-center gap-2 px-4 py-2 rounded-full glass-panel whitespace-nowrap text-sm font-medium shadow-sm">
            <span className={`w-2.5 h-2.5 rounded-full ${stats.health === 'healthy' ? 'bg-emerald-500 animate-pulse-glow' : 'bg-red-500'}`}></span>
            <span className="text-white">{stats.health === 'healthy' ? 'System Healthy' : 'Offline'}</span>
          </div>
        </div>
      </header>

      {stats.total_leads === 0 && stats.calls_today === 0 && stats.health === 'healthy' && (
        <motion.div variants={itemVariants}>
          <WelcomeBanner />
        </motion.div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <motion.div variants={itemVariants} whileHover={{ y: -5 }} className="glass-panel rounded-2xl p-6 flex flex-col justify-between transition-all duration-300">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-muted uppercase tracking-wider">Active Calls</h3>
            <div className="p-2.5 rounded-xl bg-[rgba(59,130,246,0.1)] text-[#3B82F6]"><Activity size={22} /></div>
          </div>
          <div className="text-4xl font-bold text-white tracking-tight">{stats.active_calls}</div>
        </motion.div>
        
        <motion.div variants={itemVariants} whileHover={{ y: -5 }} className="glass-panel rounded-2xl p-6 flex flex-col justify-between transition-all duration-300">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-muted uppercase tracking-wider">Calls (Period)</h3>
            <div className="p-2.5 rounded-xl bg-[rgba(16,185,129,0.1)] text-[#10B981]"><Phone size={22} /></div>
          </div>
          <div className="text-4xl font-bold text-white tracking-tight">{stats.calls_today}</div>
        </motion.div>
        
        <motion.div variants={itemVariants} whileHover={{ y: -5 }} className="glass-panel rounded-2xl p-6 flex flex-col justify-between transition-all duration-300">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-muted uppercase tracking-wider">Total Leads</h3>
            <div className="p-2.5 rounded-xl bg-[rgba(139,92,246,0.1)] text-[#8B5CF6]"><Users size={22} /></div>
          </div>
          <div className="text-4xl font-bold text-white tracking-tight">{stats.total_leads}</div>
        </motion.div>
        
        <motion.div variants={itemVariants} whileHover={{ y: -5 }} className="glass-panel rounded-2xl p-6 flex flex-col justify-between transition-all duration-300 border-gradient">
          <div className="flex items-center justify-between mb-4 relative z-10">
            <h3 className="text-sm font-semibold text-muted uppercase tracking-wider">Conversion Rate</h3>
            <div className="p-2.5 rounded-xl bg-[rgba(245,158,11,0.1)] text-[#F59E0B]"><Zap size={22} /></div>
          </div>
          <div className="text-4xl font-bold text-white tracking-tight relative z-10">{stats.conversion_rate_pct}%</div>
        </motion.div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 pt-2">
        <motion.div variants={itemVariants} className="lg:col-span-2 glass-panel rounded-2xl p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-white">Call Volume Trend</h3>
            <span className="text-xs font-medium px-2.5 py-1 bg-[rgba(255,255,255,0.05)] rounded-full text-muted border border-[rgba(255,255,255,0.05)]">Based on Selection</span>
          </div>
          <div className="w-full h-[320px]">
            <ResponsiveContainer>
              <LineChart data={stats.chart_data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorCalls" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#8B5CF6" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#8B5CF6" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="rgba(255,255,255,0.05)" />
                <XAxis dataKey="name" stroke="#64748B" tickLine={false} axisLine={false} tick={{ fontSize: 12, fill: '#94A3B8' }} dy={10} />
                <YAxis stroke="#64748B" tickLine={false} axisLine={false} tick={{ fontSize: 12, fill: '#94A3B8' }} />
                <Tooltip contentStyle={customTooltipStyle} itemStyle={{ color: '#fff' }} cursor={{ stroke: 'rgba(255,255,255,0.1)', strokeWidth: 2 }} />
                <Line 
                  type="monotone" 
                  dataKey="calls" 
                  stroke="#8B5CF6" 
                  strokeWidth={3} 
                  dot={{ fill: '#0B0E14', stroke: '#8B5CF6', strokeWidth: 2, r: 4 }} 
                  activeDot={{ r: 6, fill: '#8B5CF6', stroke: '#fff', strokeWidth: 2 }} 
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        <motion.div variants={itemVariants} className="glass-panel rounded-2xl p-6">
          <h3 className="text-lg font-semibold text-white mb-6">Lead Status Breakdown</h3>
          <div className="w-full h-[320px] flex items-center justify-center">
            {stats.lead_breakdown && stats.lead_breakdown.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={stats.lead_breakdown}
                    cx="50%"
                    cy="50%"
                    innerRadius={70}
                    outerRadius={95}
                    paddingAngle={6}
                    dataKey="value"
                    stroke="none"
                  >
                    {stats.lead_breakdown.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip contentStyle={customTooltipStyle} itemStyle={{ color: '#fff' }} />
                  <Legend 
                    verticalAlign="bottom" 
                    height={40} 
                    iconType="circle" 
                    wrapperStyle={{ fontSize: '13px', color: '#94A3B8', paddingTop: '20px' }} 
                  />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="flex flex-col items-center justify-center text-muted">
                <PieChart size={48} className="mb-3 opacity-20" />
                <p>No lead data available</p>
              </div>
            )}
          </div>
        </motion.div>
      </div>
    </motion.div>
  );
};

export default Dashboard;
