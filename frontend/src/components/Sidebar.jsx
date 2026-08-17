import { Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, Building, Users, PhoneCall, Megaphone, Mic, Smartphone, Terminal, Shield, PhoneForwarded, Settings as SettingsIcon, LogOut, User, Brain } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { motion } from 'framer-motion';

const Sidebar = () => {
  const location = useLocation();
  const { user, logout } = useAuth();

  const navItems = [
    { path: '/', label: 'Dashboard', icon: <LayoutDashboard size={20} />, require: 'view_dashboard' },
    { path: '/properties', label: 'Properties', icon: <Building size={20} />, require: 'manage_properties' },
    { path: '/leads', label: 'Leads', icon: <Users size={20} />, require: 'manage_leads' },
    { path: '/calls', label: 'Calls', icon: <PhoneCall size={20} />, require: 'manage_calls' },
    { path: '/campaigns', label: 'Campaigns', icon: <Megaphone size={20} />, require: 'manage_calls' },
    { path: '/voice-agents', label: 'Voice Agents', icon: <Mic size={20} />, require: 'manage_agents' },
    { path: '/ai-training', label: 'AI Training', icon: <Brain size={20} />, require: 'manage_agents' },
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
    <aside className="w-64 bg-[#0B0E14]/80 backdrop-blur-xl border-r border-[rgba(255,255,255,0.05)] flex flex-col transition-all duration-300 relative z-20">
      <div className="h-20 flex items-center px-6 border-b border-[rgba(255,255,255,0.05)]">
        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-accent-primary to-accent-secondary flex items-center justify-center mr-3 shadow-[0_0_15px_rgba(139,92,246,0.4)]">
          <span className="text-white font-bold text-lg leading-none">N</span>
        </div>
        <h2 className="text-xl font-bold tracking-tight text-white">NexaVoice</h2>
      </div>
      
      <div className="flex-1 overflow-y-auto py-6 px-3 space-y-1 scrollbar-hide">
        {navItems.filter(item => hasPermission(item.require)).map((item) => {
          const isActive = location.pathname === item.path;
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 relative overflow-hidden group ${
                isActive 
                  ? 'text-white bg-[rgba(255,255,255,0.05)]' 
                  : 'text-muted hover:bg-[rgba(255,255,255,0.02)] hover:text-white'
              }`}
            >
              {isActive && (
                <motion.div layoutId="activeNavIndicator" className="absolute left-0 top-0 bottom-0 w-1 bg-accent-primary" />
              )}
              <span className={`mr-3 z-10 transition-colors ${isActive ? 'text-accent-primary' : 'text-muted group-hover:text-accent-primary/70'}`}>
                {item.icon}
              </span>
              <span className="z-10">{item.label}</span>
            </Link>
          );
        })}
        
        {hasPermission('manage_roles') && (
          <Link
            to="/settings"
            className={`flex items-center px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 relative group ${
              location.pathname === '/settings' 
                ? 'text-white bg-[rgba(255,255,255,0.05)]' 
                : 'text-muted hover:bg-[rgba(255,255,255,0.02)] hover:text-white'
            }`}
          >
            {location.pathname === '/settings' && (
              <motion.div layoutId="activeNavIndicator" className="absolute left-0 top-0 bottom-0 w-1 bg-accent-primary" />
            )}
            <span className={`mr-3 z-10 transition-colors ${location.pathname === '/settings' ? 'text-accent-primary' : 'text-muted group-hover:text-accent-primary/70'}`}>
              <SettingsIcon size={20} />
            </span>
            <span className="z-10">Settings</span>
          </Link>
        )}
        
        {user?.is_superadmin && (
          <Link
            to="/agency"
            className={`flex items-center px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 relative group mt-4 border border-[rgba(255,255,255,0.05)] ${
              location.pathname === '/agency' 
                ? 'text-white bg-[rgba(139,92,246,0.1)] border-[rgba(139,92,246,0.3)]' 
                : 'text-accent-primary hover:bg-[rgba(139,92,246,0.05)] hover:border-[rgba(139,92,246,0.2)]'
            }`}
          >
            <span className="mr-3 z-10">
              <Shield size={20} />
            </span>
            <span className="z-10">Agency Portal</span>
          </Link>
        )}
      </div>
      
      <div className="p-4 border-t border-[rgba(255,255,255,0.05)] bg-[rgba(0,0,0,0.2)]">
        <Link
          to="/profile"
          className={`flex items-center px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 mb-2 relative group ${
            location.pathname === '/profile' 
              ? 'text-white bg-[rgba(255,255,255,0.05)]' 
              : 'text-muted hover:bg-[rgba(255,255,255,0.02)] hover:text-white'
          }`}
        >
          {location.pathname === '/profile' && (
            <motion.div layoutId="activeNavIndicator" className="absolute left-0 top-0 bottom-0 w-1 bg-accent-primary" />
          )}
          <User size={18} className={`mr-3 z-10 transition-colors ${location.pathname === '/profile' ? 'text-accent-primary' : 'text-muted group-hover:text-white'}`} />
          <span className="z-10 truncate">{user?.first_name ? `${user.first_name} ${user.last_name || ''}` : 'My Profile'}</span>
        </Link>
        <button 
          onClick={logout}
          className="w-full flex items-center px-4 py-3 rounded-xl text-sm font-medium text-muted hover:bg-[rgba(239,68,68,0.1)] hover:text-accent-danger transition-colors group" 
        >
          <LogOut size={18} className="mr-3 text-muted group-hover:text-accent-danger transition-colors" />
          Logout
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
