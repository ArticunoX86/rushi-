import React, { useState, useEffect } from 'react';
import api from '../api';
import { Shield, Users, Activity, Plus, Database } from 'lucide-react';
import Modal from '../components/Modal';
import './Shared.css';

const Agency = () => {
  const [stats, setStats] = useState({ total_tenants: 0, total_calls: 0, total_users: 0, active_ai_minutes: 0 });
  const [tenants, setTenants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState({ name: '', is_active: true });

  const fetchData = async () => {
    setLoading(true);
    try {
      const [statsRes, tenantsRes] = await Promise.all([
        api.get('/admin/stats'),
        api.get('/admin/tenants')
      ]);
      setStats(statsRes.data);
      setTenants(tenantsRes.data);
    } catch (error) {
      console.error('Failed to fetch agency data', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/admin/tenants', formData);
      setIsModalOpen(false);
      setFormData({ name: '', is_active: true });
      fetchData();
    } catch (error) {
      console.error('Failed to create tenant', error);
      alert('Failed to create client workspace.');
    }
  };

  return (
    <div className="page-container">
      <header className="page-header">
        <div>
          <h1 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Shield size={28} color="var(--accent-primary)" />
            Agency Portal (Super Admin)
          </h1>
          <p className="text-secondary">Manage client workspaces and global platform metrics.</p>
        </div>
        <button className="btn btn-primary" onClick={() => setIsModalOpen(true)}>
          <Plus size={16} /> New Client Workspace
        </button>
      </header>

      {loading ? (
        <div className="loading">Loading agency data...</div>
      ) : (
        <>
          <div className="grid grid-cols-4" style={{ marginBottom: '2rem' }}>
            <div className="stat-card">
              <div className="stat-icon"><Database size={20} /></div>
              <div className="stat-content">
                <p className="stat-label">Total Workspaces</p>
                <h3 className="stat-value">{stats.total_tenants}</h3>
              </div>
            </div>
            <div className="stat-card">
              <div className="stat-icon"><Users size={20} /></div>
              <div className="stat-content">
                <p className="stat-label">Total Users</p>
                <h3 className="stat-value">{stats.total_users}</h3>
              </div>
            </div>
            <div className="stat-card">
              <div className="stat-icon"><Activity size={20} /></div>
              <div className="stat-content">
                <p className="stat-label">Total Calls</p>
                <h3 className="stat-value">{stats.total_calls}</h3>
              </div>
            </div>
            <div className="stat-card">
              <div className="stat-icon" style={{ color: 'var(--success)', background: 'rgba(16, 185, 129, 0.1)' }}>
                <Shield size={20} />
              </div>
              <div className="stat-content">
                <p className="stat-label">AI Minutes Billed</p>
                <h3 className="stat-value">{stats.active_ai_minutes}m</h3>
              </div>
            </div>
          </div>

          <div className="glass table-container">
            <h3>Client Workspaces (Tenants)</h3>
            <table className="data-table" style={{ marginTop: '1rem' }}>
              <thead>
                <tr>
                  <th>Client ID</th>
                  <th>Company Name</th>
                  <th>Status</th>
                  <th>Created At</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {tenants.map(tenant => (
                  <tr key={tenant.id}>
                    <td style={{ fontFamily: 'monospace', fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{tenant.id.split('-')[0]}...</td>
                    <td style={{ fontWeight: 500 }}>{tenant.name}</td>
                    <td>
                      <span className={`badge ${tenant.is_active ? 'active' : 'inactive'}`}>
                        {tenant.is_active ? 'Active' : 'Suspended'}
                      </span>
                    </td>
                    <td>{new Date(tenant.created_at).toLocaleDateString()}</td>
                    <td>
                      <button className="btn" style={{ fontSize: '0.75rem', padding: '0.25rem 0.5rem' }}>
                        Manage Settings
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Provision New Client Workspace">
        <form onSubmit={handleSubmit} className="grid grid-cols-2" style={{ gap: '1rem' }}>
          
          <div className="input-group" style={{ gridColumn: 'span 2' }}>
            <label className="input-label">Company / Client Name</label>
            <input type="text" name="name" className="input-field" value={formData.name} onChange={handleInputChange} required />
          </div>

          <div className="input-group checkbox-label" style={{ gridColumn: 'span 2', display: 'flex', alignItems: 'center', gap: '0.5rem', marginTop: '0.5rem' }}>
            <input type="checkbox" name="is_active" id="is_active" checked={formData.is_active} onChange={handleInputChange} />
            <label htmlFor="is_active" style={{ cursor: 'pointer' }}>Active Subscription</label>
          </div>

          <div style={{ gridColumn: 'span 2', display: 'flex', justifyContent: 'flex-end', gap: '1rem', marginTop: '1rem' }}>
            <button type="button" className="btn" onClick={() => setIsModalOpen(false)}>Cancel</button>
            <button type="submit" className="btn btn-primary">Create Workspace</button>
          </div>
        </form>
      </Modal>
    </div>
  );
};

export default Agency;
