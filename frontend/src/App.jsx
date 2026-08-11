import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import Properties from './pages/Properties';
import Leads from './pages/Leads';
import Calls from './pages/Calls';
import VoiceAgents from './pages/VoiceAgents';
import Devices from './pages/Devices';
import Logs from './pages/Logs';
import Settings from './pages/Settings';
import WebRTC from './pages/WebRTC';
import Auth from './pages/Auth';
import Login from './pages/Login';
import Agency from './pages/Agency';
import { AuthProvider, useAuth } from './context/AuthContext';

const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();
  if (loading) return <div className="login-container"><div className="text-secondary">Checking session...</div></div>;
  if (!user) return <Navigate to="/login" replace />;
  return (
    <div className="app-container">
      <Sidebar />
      <main className="main-content">
        {children}
      </main>
    </div>
  );
};

import PermissionGuard from './components/PermissionGuard';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<ProtectedRoute><PermissionGuard require="view_dashboard" fallback={<Navigate to="/login" replace/>}><Dashboard /></PermissionGuard></ProtectedRoute>} />
          <Route path="/properties" element={<ProtectedRoute><PermissionGuard require="manage_properties" fallback={<Navigate to="/" replace/>}><Properties /></PermissionGuard></ProtectedRoute>} />
          <Route path="/leads" element={<ProtectedRoute><PermissionGuard require="manage_leads" fallback={<Navigate to="/" replace/>}><Leads /></PermissionGuard></ProtectedRoute>} />
          <Route path="/calls" element={<ProtectedRoute><PermissionGuard require="manage_calls" fallback={<Navigate to="/" replace/>}><Calls /></PermissionGuard></ProtectedRoute>} />
          <Route path="/voice-agents" element={<ProtectedRoute><PermissionGuard require="manage_agents" fallback={<Navigate to="/" replace/>}><VoiceAgents /></PermissionGuard></ProtectedRoute>} />
          <Route path="/devices" element={<ProtectedRoute><PermissionGuard require="manage_devices" fallback={<Navigate to="/" replace/>}><Devices /></PermissionGuard></ProtectedRoute>} />
          <Route path="/webrtc" element={<ProtectedRoute><WebRTC /></ProtectedRoute>} />
          <Route path="/logs" element={<ProtectedRoute><PermissionGuard require="view_logs" fallback={<Navigate to="/" replace/>}><Logs /></PermissionGuard></ProtectedRoute>} />
          <Route path="/settings" element={<ProtectedRoute><PermissionGuard require="manage_roles" fallback={<Navigate to="/" replace/>}><Settings /></PermissionGuard></ProtectedRoute>} />
          <Route path="/auth" element={<ProtectedRoute><Auth /></ProtectedRoute>} />
          <Route path="/agency" element={<ProtectedRoute><Agency /></ProtectedRoute>} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
