import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import Properties from './pages/Properties';
import Leads from './pages/Leads';
import Calls from './pages/Calls';
import VoiceAgents from './pages/VoiceAgents';
import Devices from './pages/Devices';
import Campaigns from './pages/Campaigns';
import Logs from './pages/Logs';
import Settings from './pages/Settings';
import WebRTC from './pages/WebRTC';
import Auth from './pages/Auth';
import Login from './pages/Login';
import Agency from './pages/Agency';
import Profile from './pages/Profile';
import AITraining from './pages/AITraining';
import { AuthProvider, useAuth } from './context/AuthContext';

const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();
  if (loading) return <div className="flex h-screen w-full items-center justify-center bg-gray-50"><div className="text-gray-500 animate-pulse">Checking session...</div></div>;
  if (!user) return <Navigate to="/login" replace />;
  return (
    <div className="flex h-screen w-full overflow-hidden">
      <Sidebar />
      <main className="flex-1 overflow-y-auto px-6 py-8">
        <div className="mx-auto max-w-7xl">
          {children}
        </div>
      </main>
    </div>
  );
};

import PermissionGuard from './components/PermissionGuard';

const NotAuthorized = () => (
  <div className="flex h-full w-full items-center justify-center">
    <div className="text-center glass-panel p-8 rounded-2xl border border-[rgba(255,255,255,0.08)]">
      <h2 className="text-2xl font-bold text-white mb-2">Access Denied</h2>
      <p className="text-muted">You do not have permission to view this page.</p>
      <p className="text-sm text-gray-400 mt-4">Please contact your administrator if you need access.</p>
    </div>
  </div>
);

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<ProtectedRoute><PermissionGuard require="view_dashboard" fallback={<NotAuthorized />}><Dashboard /></PermissionGuard></ProtectedRoute>} />
          <Route path="/properties" element={<ProtectedRoute><PermissionGuard require="manage_properties" fallback={<NotAuthorized />}><Properties /></PermissionGuard></ProtectedRoute>} />
          <Route path="/leads" element={<ProtectedRoute><PermissionGuard require="manage_leads" fallback={<NotAuthorized />}><Leads /></PermissionGuard></ProtectedRoute>} />
          <Route path="/calls" element={<ProtectedRoute><PermissionGuard require="manage_calls" fallback={<NotAuthorized />}><Calls /></PermissionGuard></ProtectedRoute>} />
          <Route path="/campaigns" element={<ProtectedRoute><PermissionGuard require="manage_calls" fallback={<NotAuthorized />}><Campaigns /></PermissionGuard></ProtectedRoute>} />
          <Route path="/voice-agents" element={<ProtectedRoute><PermissionGuard require="manage_agents" fallback={<NotAuthorized />}><VoiceAgents /></PermissionGuard></ProtectedRoute>} />
          <Route path="/devices" element={<ProtectedRoute><PermissionGuard require="manage_devices" fallback={<NotAuthorized />}><Devices /></PermissionGuard></ProtectedRoute>} />
          <Route path="/webrtc" element={<ProtectedRoute><WebRTC /></ProtectedRoute>} />
          <Route path="/logs" element={<ProtectedRoute><PermissionGuard require="view_logs" fallback={<NotAuthorized />}><Logs /></PermissionGuard></ProtectedRoute>} />
          <Route path="/settings" element={<ProtectedRoute><PermissionGuard require="manage_roles" fallback={<NotAuthorized />}><Settings /></PermissionGuard></ProtectedRoute>} />
          <Route path="/ai-training" element={<ProtectedRoute><AITraining /></ProtectedRoute>} />
          <Route path="/auth" element={<ProtectedRoute><Auth /></ProtectedRoute>} />
          <Route path="/agency" element={<ProtectedRoute><Agency /></ProtectedRoute>} />
          <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
