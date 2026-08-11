import { Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, Building, Users, PhoneCall, Mic, Smartphone, Terminal, Shield, PhoneForwarded, Settings as SettingsIcon, LogOut } from 'lucide-react';
import './Sidebar.css';
import { useAuth } from '../context/AuthContext';

const Sidebar = () => {
  const location = useLocation();
  const { user, logout } = useAuth();

  const navItems = [
    { path: '/', label: 'Dashboard', icon: <LayoutDashboard size={20} />, require: 'view_dashboard' },
    { path: '/properties', label: 'Properties', icon: <Building size={20} />, require: 'manage_properties' },
    { path: '/leads', label: 'Leads', icon: <Users size={20} />, require: 'manage_leads' },
    { path: '/calls', label: 'Calls', icon: <PhoneCall size={20} />, require: 'manage_calls' },
    { path: '/voice-agents', label: 'Voice Agents', icon: <Mic size={20} />, require: 'manage_agents' },
    { path: '/devices', label: 'Devices', icon: <Smartphone size={20} />, require: 'manage_devices' },
    { path: '/webrtc', label: 'WebRTC', icon: <PhoneForwarded size={20} /> },
    { path: '/logs', label: 'System Logs', icon: <Terminal size={20} />, require: 'view_logs' },
    { path: '/auth', label: 'Auth & API', icon: <Shield size={20} /> },
  ];

  const hasPermission = (requirePerm) => {
    if (!requirePerm) return true;
    if (user?.role?.name === "System Administrator") return true;
    return user?.role?.permissions?.includes(requirePerm);
  };

  return (
    <aside className="sidebar glass">
      <div className="sidebar-header">
        <div className="logo-placeholder"></div>
        <h2>AI Caller</h2>
      </div>
      
      <nav className="sidebar-nav">
        {navItems.filter(item => hasPermission(item.require)).map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`nav-item ${location.pathname === item.path ? 'active' : ''}`}
          >
            <span className="nav-icon">{item.icon}</span>
            <span className="nav-label">{item.label}</span>
          </Link>
        ))}
        {hasPermission('manage_roles') && (
          <Link
            to="/settings"
            className={`nav-item ${location.pathname === '/settings' ? 'active' : ''}`}
          >
            <span className="nav-icon"><SettingsIcon size={20} /></span>
            <span className="nav-label">Settings</span>
          </Link>
        )}
        {user?.is_superadmin && (
          <Link
            to="/agency"
            className={`nav-item ${location.pathname === '/agency' ? 'active' : ''}`}
          >
            <span className="nav-icon"><Shield size={20} /></span>
            <span className="nav-label">Agency Portal</span>
          </Link>
        )}
      </nav>
      
      <div className="sidebar-footer" style={{ marginTop: 'auto', paddingTop: '1rem', borderTop: '1px solid var(--border-color)' }}>
        <button 
          onClick={logout}
          className="nav-item" 
          style={{ width: '100%', background: 'transparent', border: 'none', cursor: 'pointer', textAlign: 'left' }}
        >
          <span className="nav-icon"><LogOut size={20} /></span>
          <span className="nav-label">Logout</span>
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
