import React, { useState, useEffect } from 'react';
import api from '../api';
import { User, Lock, Save } from 'lucide-react';
import { useAuth } from '../context/AuthContext';


const Profile = () => {
  const { user } = useAuth();
  const [profileData, setProfileData] = useState({
    first_name: '',
    last_name: '',
    phone: '',
    email: ''
  });
  
  const [passwordData, setPasswordData] = useState({
    current_password: '',
    new_password: '',
    confirm_password: ''
  });

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });

  useEffect(() => {
    if (user) {
      setProfileData({
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        phone: user.phone || '',
        email: user.email || '' // Readonly
      });
    }
  }, [user]);

  const handleProfileChange = (e) => {
    setProfileData({ ...profileData, [e.target.name]: e.target.value });
  };

  const handlePasswordChange = (e) => {
    setPasswordData({ ...passwordData, [e.target.name]: e.target.value });
  };

  const submitProfile = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage({ type: '', text: '' });
    try {
      await api.put('/auth/me', {
        first_name: profileData.first_name,
        last_name: profileData.last_name,
        phone: profileData.phone
      });
      setMessage({ type: 'success', text: 'Profile updated successfully. Refresh to see changes globally.' });
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to update profile.' });
    } finally {
      setLoading(false);
    }
  };

  const submitPassword = async (e) => {
    e.preventDefault();
    if (passwordData.new_password !== passwordData.confirm_password) {
      setMessage({ type: 'error', text: 'New passwords do not match.' });
      return;
    }
    
    setLoading(true);
    setMessage({ type: '', text: '' });
    try {
      await api.put('/auth/me/password', {
        current_password: passwordData.current_password,
        new_password: passwordData.new_password
      });
      setMessage({ type: 'success', text: 'Password updated successfully.' });
      setPasswordData({ current_password: '', new_password: '', confirm_password: '' });
    } catch (error) {
      setMessage({ type: 'error', text: error.response?.data?.detail || 'Failed to update password.' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col gap-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <header className="flex justify-between items-start mb-2">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight">My Profile</h1>
          <p className="text-muted mt-1">Manage your personal information and security.</p>
        </div>
      </header>

      {message.text && (
        <div style={{
          padding: '1rem', 
          marginBottom: '1.5rem', 
          borderRadius: '8px',
          background: message.type === 'success' ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)',
          color: message.type === 'success' ? '#10b981' : '#ef4444',
          border: `1px solid ${message.type === 'success' ? 'rgba(16, 185, 129, 0.2)' : 'rgba(239, 68, 68, 0.2)'}`
        }}>
          {message.text}
        </div>
      )}

      <div className="grid grid-cols-2" style={{ gap: '2rem', alignItems: 'start' }}>
        
        {/* Profile Settings Card */}
        <div className="glass-panel rounded-xl shadow-sm border border-[rgba(255,255,255,0.08)] overflow-hidden" style={{ padding: '2rem', borderRadius: '12px' }}>
          <h2 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1.5rem', color: 'var(--text-primary)' }}>
            <User size={20} className="text-primary" /> Personal Information
          </h2>
          
          <form onSubmit={submitProfile} className="grid grid-cols-2" style={{ gap: '1.5rem' }}>
            <div className="flex flex-col gap-1.5">
              <label className="text-sm font-medium text-gray-200">First Name</label>
              <input type="text" name="first_name" className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow w-full" value={profileData.first_name} onChange={handleProfileChange} required />
            </div>
            
            <div className="flex flex-col gap-1.5">
              <label className="text-sm font-medium text-gray-200">Last Name</label>
              <input type="text" name="last_name" className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow w-full" value={profileData.last_name} onChange={handleProfileChange} required />
            </div>
            
            <div className="flex flex-col gap-1.5" style={{ gridColumn: 'span 2' }}>
              <label className="text-sm font-medium text-gray-200">Email Address</label>
              <input type="email" className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow w-full" value={profileData.email} disabled style={{ opacity: 0.7, cursor: 'not-allowed' }} />
              <small className="text-muted mt-1" style={{ marginTop: '0.25rem', display: 'block' }}>Email cannot be changed.</small>
            </div>
            
            <div className="flex flex-col gap-1.5" style={{ gridColumn: 'span 2' }}>
              <label className="text-sm font-medium text-gray-200">Phone Number</label>
              <input type="text" name="phone" className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow w-full" value={profileData.phone} onChange={handleProfileChange} />
            </div>
            
            <div style={{ gridColumn: 'span 2', display: 'flex', justifyContent: 'flex-end', marginTop: '0.5rem' }}>
              <button type="submit" className="px-4 py-2 rounded-lg font-medium inline-flex items-center gap-2 bg-accent-primary text-white hover:bg-accent-primary/80 transition-colors shadow-sm" disabled={loading}>
                <Save size={16} /> Save Changes
              </button>
            </div>
          </form>
        </div>

        {/* Security Card */}
        <div className="glass-panel rounded-xl shadow-sm border border-[rgba(255,255,255,0.08)] overflow-hidden" style={{ padding: '2rem', borderRadius: '12px' }}>
          <h2 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1.5rem', color: 'var(--text-primary)' }}>
            <Lock size={20} className="text-primary" /> Change Password
          </h2>
          
          <form onSubmit={submitPassword} style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
            <div className="flex flex-col gap-1.5">
              <label className="text-sm font-medium text-gray-200">Current Password</label>
              <input type="password" name="current_password" className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow w-full" value={passwordData.current_password} onChange={handlePasswordChange} required />
            </div>
            
            <div className="flex flex-col gap-1.5">
              <label className="text-sm font-medium text-gray-200">New Password</label>
              <input type="password" name="new_password" className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow w-full" value={passwordData.new_password} onChange={handlePasswordChange} required minLength="6" />
            </div>
            
            <div className="flex flex-col gap-1.5">
              <label className="text-sm font-medium text-gray-200">Confirm New Password</label>
              <input type="password" name="confirm_password" className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow w-full" value={passwordData.confirm_password} onChange={handlePasswordChange} required minLength="6" />
            </div>
            
            <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '0.5rem' }}>
              <button type="submit" className="px-4 py-2 rounded-lg font-medium inline-flex items-center gap-2 glass-panel border border-[rgba(255,255,255,0.08)] text-gray-200 hover:bg-[rgba(255,255,255,0.02)] transition-colors shadow-sm" disabled={loading || !passwordData.current_password}>
                <Lock size={16} /> Update Password
              </button>
            </div>
          </form>
        </div>

      </div>
    </div>
  );
};

export default Profile;
