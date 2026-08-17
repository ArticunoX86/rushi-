import React, { useState, useEffect } from 'react';
import api from '../api';
import { Shield, Users, Activity, Plus, Database, Edit, Trash2, Settings, Smartphone } from 'lucide-react';
import Modal from '../components/Modal';


const Agency = () => {
  const [activeTab, setActiveTab] = useState('workspaces');
  
  const [stats, setStats] = useState({ total_tenants: 0, total_calls: 0, total_users: 0, active_ai_minutes: 0 });
  const [tenants, setTenants] = useState([]);
  const [users, setUsers] = useState([]);
  const [devices, setDevices] = useState([]);
  
  const [loading, setLoading] = useState(true);
  
  // Modals for Workspaces
  const [isTenantModalOpen, setIsTenantModalOpen] = useState(false);
  const [isEditingTenant, setIsEditingTenant] = useState(false);
  const [editingTenantId, setEditingTenantId] = useState(null);
  const [tenantFormData, setTenantFormData] = useState({ name: '', is_active: true });
  
  // Modals for Users
  const [isUserModalOpen, setIsUserModalOpen] = useState(false);
  const [editingUserId, setEditingUserId] = useState(null);
  const [userFormData, setUserFormData] = useState({ is_superadmin: false, tenant_id: '' });

  const fetchData = async () => {
    setLoading(true);
    try {
      const [statsRes, tenantsRes, usersRes, devicesRes] = await Promise.all([
        api.get('/admin/stats'),
        api.get('/admin/tenants'),
        api.get('/admin/users'),
        api.get('/admin/devices')
      ]);
      setStats(statsRes.data);
      setTenants(tenantsRes.data);
      setUsers(usersRes.data);
      setDevices(devicesRes.data);
    } catch (error) {
      console.error('Failed to fetch agency data', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  // --- Workspace Handlers ---
  const handleTenantInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setTenantFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleTenantSubmit = async (e) => {
    e.preventDefault();
    try {
      if (isEditingTenant) {
        await api.put(`/admin/tenants/${editingTenantId}`, tenantFormData);
      } else {
        await api.post('/admin/tenants', tenantFormData);
      }
      setIsTenantModalOpen(false);
      setIsEditingTenant(false);
      setEditingTenantId(null);
      setTenantFormData({ name: '', is_active: true });
      fetchData();
    } catch (error) {
      console.error('Failed to save tenant', error);
      alert('Failed to save client workspace.');
    }
  };

  const handleEditTenantClick = (tenant) => {
    setTenantFormData({ name: tenant.name, is_active: tenant.is_active });
    setEditingTenantId(tenant.id);
    setIsEditingTenant(true);
    setIsTenantModalOpen(true);
  };

  const handleAddTenantClick = () => {
    setTenantFormData({ name: '', is_active: true });
    setIsEditingTenant(false);
    setEditingTenantId(null);
    setIsTenantModalOpen(true);
  };

  const handleDeleteTenant = async (id) => {
    if (!window.confirm("Are you sure you want to delete this workspace? This action cannot be undone.")) return;
    try {
      await api.delete(`/admin/tenants/${id}`);
      fetchData();
    } catch (error) {
      console.error('Failed to delete tenant', error);
      alert('Failed to delete workspace.');
    }
  };

  // --- User Handlers ---
  const handleUserInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setUserFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : (value === "" ? null : value)
    }));
  };

  const handleEditUserClick = (user) => {
    setUserFormData({ is_superadmin: user.is_superadmin, tenant_id: user.tenant_id || "" });
    setEditingUserId(user.id);
    setIsUserModalOpen(true);
  };

  const handleUserSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.put(`/admin/users/${editingUserId}`, userFormData);
      setIsUserModalOpen(false);
      setEditingUserId(null);
      setUserFormData({ is_superadmin: false, tenant_id: '' });
      fetchData();
    } catch (error) {
      console.error('Failed to save user', error);
      alert('Failed to save user.');
    }
  };

  const handleDeleteUser = async (id) => {
    if (!window.confirm("Are you sure you want to delete this user?")) return;
    try {
      await api.delete(`/admin/users/${id}`);
      fetchData();
    } catch (error) {
      console.error('Failed to delete user', error);
      alert('Failed to delete user.');
    }
  };

  // --- Device Handlers ---
  const handleDeleteDevice = async (id) => {
    if (!window.confirm("Are you sure you want to delete this device from the system?")) return;
    try {
      await api.delete(`/admin/devices/${id}`);
      fetchData();
    } catch (error) {
      console.error('Failed to delete device', error);
      alert('Failed to delete device.');
    }
  };

  // --- Helper ---
  const getTenantName = (id) => {
    if (!id) return 'Unassigned';
    const t = tenants.find(t => t.id === id);
    return t ? t.name : 'Unknown';
  };

  return (
    <div className="flex flex-col gap-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <header className="flex justify-between items-start mb-2">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight flex items-center gap-3">
            <div className="p-2 bg-[rgba(139,92,246,0.1)] rounded-lg text-accent-primary">
              <Shield size={28} />
            </div>
            Agency Portal <span className="text-lg font-medium text-muted bg-[rgba(255,255,255,0.05)] px-3 py-1 rounded-full ml-2">Super Admin</span>
          </h1>
          <p className="text-muted mt-2 text-lg">Manage client workspaces, global users, and platform metrics.</p>
        </div>
        {activeTab === 'workspaces' && (
          <button className="px-5 py-2.5 rounded-lg font-medium inline-flex items-center gap-2 bg-accent-primary text-white hover:bg-accent-primary/80 transition-all shadow-[0_0_15px_rgba(139,92,246,0.3)] hover:shadow-[0_0_25px_rgba(139,92,246,0.5)] hover:-translate-y-0.5" onClick={handleAddTenantClick}>
            <Plus size={18} /> New Client Workspace
          </button>
        )}
      </header>

      {loading ? (
        <div className="p-12 text-center text-muted">Loading agency data...</div>
      ) : (
        <>
          <div className="grid grid-cols-4 gap-6 mb-8">
            <div className="glass-panel p-6 rounded-xl flex flex-col gap-4 shadow-sm border border-[rgba(255,255,255,0.08)] transition-all hover:-translate-y-1 hover:border-[rgba(255,255,255,0.15)] group relative overflow-hidden">
              <div className="absolute top-0 right-0 w-32 h-32 bg-[rgba(139,92,246,0.05)] rounded-full -mr-16 -mt-16 transition-transform group-hover:scale-150 duration-500 blur-xl"></div>
              <div className="w-12 h-12 rounded-xl bg-[rgba(139,92,246,0.1)] text-accent-primary flex items-center justify-center relative z-10">
                <Database size={24} />
              </div>
              <div className="relative z-10">
                <p className="text-sm font-medium text-muted uppercase tracking-wider mb-1">Total Workspaces</p>
                <h3 className="text-3xl font-bold text-white">{stats.total_tenants}</h3>
              </div>
            </div>
            
            <div className="glass-panel p-6 rounded-xl flex flex-col gap-4 shadow-sm border border-[rgba(255,255,255,0.08)] transition-all hover:-translate-y-1 hover:border-[rgba(255,255,255,0.15)] group relative overflow-hidden">
              <div className="absolute top-0 right-0 w-32 h-32 bg-[rgba(139,92,246,0.05)] rounded-full -mr-16 -mt-16 transition-transform group-hover:scale-150 duration-500 blur-xl"></div>
              <div className="w-12 h-12 rounded-xl bg-[rgba(139,92,246,0.1)] text-accent-primary flex items-center justify-center relative z-10">
                <Users size={24} />
              </div>
              <div className="relative z-10">
                <p className="text-sm font-medium text-muted uppercase tracking-wider mb-1">Total Users</p>
                <h3 className="text-3xl font-bold text-white">{stats.total_users}</h3>
              </div>
            </div>

            <div className="glass-panel p-6 rounded-xl flex flex-col gap-4 shadow-sm border border-[rgba(255,255,255,0.08)] transition-all hover:-translate-y-1 hover:border-[rgba(255,255,255,0.15)] group relative overflow-hidden">
              <div className="absolute top-0 right-0 w-32 h-32 bg-[rgba(139,92,246,0.05)] rounded-full -mr-16 -mt-16 transition-transform group-hover:scale-150 duration-500 blur-xl"></div>
              <div className="w-12 h-12 rounded-xl bg-[rgba(139,92,246,0.1)] text-accent-primary flex items-center justify-center relative z-10">
                <Activity size={24} />
              </div>
              <div className="relative z-10">
                <p className="text-sm font-medium text-muted uppercase tracking-wider mb-1">Total Calls</p>
                <h3 className="text-3xl font-bold text-white">{stats.total_calls}</h3>
              </div>
            </div>

            <div className="glass-panel p-6 rounded-xl flex flex-col gap-4 shadow-sm border border-[rgba(255,255,255,0.08)] transition-all hover:-translate-y-1 hover:border-emerald-500/30 group relative overflow-hidden">
              <div className="absolute top-0 right-0 w-32 h-32 bg-[rgba(16,185,129,0.05)] rounded-full -mr-16 -mt-16 transition-transform group-hover:scale-150 duration-500 blur-xl"></div>
              <div className="w-12 h-12 rounded-xl bg-[rgba(16,185,129,0.1)] text-emerald-400 flex items-center justify-center relative z-10">
                <Shield size={24} />
              </div>
              <div className="relative z-10">
                <p className="text-sm font-medium text-emerald-400/70 uppercase tracking-wider mb-1">AI Minutes Billed</p>
                <h3 className="text-3xl font-bold text-emerald-400">{stats.active_ai_minutes}m</h3>
              </div>
            </div>
          </div>

          {/* Tabs */}
          <div className="flex gap-2 mb-8 bg-[rgba(255,255,255,0.02)] p-1.5 rounded-xl w-max border border-[rgba(255,255,255,0.05)]">
            <button 
              className={`px-5 py-2.5 font-medium text-sm rounded-lg flex items-center gap-2 transition-all ${activeTab === 'workspaces' ? 'bg-[rgba(255,255,255,0.1)] text-white shadow-sm' : 'text-muted hover:text-gray-200 hover:bg-[rgba(255,255,255,0.05)]'}`}
              onClick={() => setActiveTab('workspaces')}
            >
              <Database size={18} /> Workspaces
            </button>
            <button 
              className={`px-5 py-2.5 font-medium text-sm rounded-lg flex items-center gap-2 transition-all ${activeTab === 'users' ? 'bg-[rgba(255,255,255,0.1)] text-white shadow-sm' : 'text-muted hover:text-gray-200 hover:bg-[rgba(255,255,255,0.05)]'}`}
              onClick={() => setActiveTab('users')}
            >
              <Users size={18} /> All Users
            </button>
            <button 
              className={`px-5 py-2.5 font-medium text-sm rounded-lg flex items-center gap-2 transition-all ${activeTab === 'devices' ? 'bg-[rgba(255,255,255,0.1)] text-white shadow-sm' : 'text-muted hover:text-gray-200 hover:bg-[rgba(255,255,255,0.05)]'}`}
              onClick={() => setActiveTab('devices')}
            >
              <Smartphone size={18} /> All Devices
            </button>
          </div>

          {activeTab === 'workspaces' && (
            <div className="glass-panel rounded-xl shadow-sm border border-[rgba(255,255,255,0.08)] overflow-hidden">
              <h3>Client Workspaces (Tenants)</h3>
              <table className="w-full text-left border-collapse" style={{ marginTop: '1rem' }}>
                <thead>
                  <tr>
                    <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Client ID</th>
                    <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Company Name</th>
                    <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Status</th>
                    <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Created At</th>
                    <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {tenants.map(tenant => (
                    <tr key={tenant.id}>
                      <td style={{ fontFamily: 'monospace', fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{tenant.id.split('-')[0]}...</td>
                      <td className="px-6 py-4 whitespace-nowrap font-medium text-white">{tenant.name}</td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`badge ${tenant.is_active ? 'active' : 'inactive'}`}>
                          {tenant.is_active ? 'Active' : 'Suspended'}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">{new Date(tenant.created_at).toLocaleDateString()}</td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                          <button className="p-1.5 text-muted hover:text-accent-primary hover:bg-[rgba(139,92,246,0.1)] rounded-lg transition-colors" onClick={() => handleEditTenantClick(tenant)} title="Edit Settings">
                            <Settings size={16} />
                          </button>
                          <button className="p-1.5 text-muted hover:text-accent-danger hover:bg-red-50 rounded-lg transition-colors" onClick={() => handleDeleteTenant(tenant.id)} title="Delete Workspace">
                            <Trash2 size={16} />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                  {tenants.length === 0 && (
                    <tr><td colSpan="5" style={{ textAlign: 'center', padding: '2rem' }}>No workspaces found.</td></tr>
                  )}
                </tbody>
              </table>
            </div>
          )}

          {activeTab === 'users' && (
            <div className="glass-panel rounded-xl shadow-sm border border-[rgba(255,255,255,0.08)] overflow-hidden">
              <h3>Global Users</h3>
              <table className="w-full text-left border-collapse" style={{ marginTop: '1rem' }}>
                <thead>
                  <tr>
                    <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Email</th>
                    <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Name</th>
                    <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Workspace</th>
                    <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Super Admin</th>
                    <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map(user => (
                    <tr key={user.id}>
                      <td className="px-6 py-4 whitespace-nowrap font-medium text-white">{user.email}</td>
                      <td className="px-6 py-4 whitespace-nowrap">{user.first_name} {user.last_name}</td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="badge neutral">
                          {getTenantName(user.tenant_id)}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {user.is_superadmin ? <span className="badge active">Yes</span> : <span className="badge inactive">No</span>}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                          <button className="p-1.5 text-muted hover:text-accent-primary hover:bg-[rgba(139,92,246,0.1)] rounded-lg transition-colors" onClick={() => handleEditUserClick(user)} title="Edit User">
                            <Settings size={16} />
                          </button>
                          <button className="p-1.5 text-muted hover:text-accent-danger hover:bg-red-50 rounded-lg transition-colors" onClick={() => handleDeleteUser(user.id)} title="Delete User">
                            <Trash2 size={16} />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                  {users.length === 0 && (
                    <tr><td colSpan="5" style={{ textAlign: 'center', padding: '2rem' }}>No users found.</td></tr>
                  )}
                </tbody>
              </table>
            </div>
          )}

          {activeTab === 'devices' && (
            <div className="glass-panel rounded-xl shadow-sm border border-[rgba(255,255,255,0.08)] overflow-hidden">
              <h3>Global Telephony Devices</h3>
              <table className="w-full text-left border-collapse" style={{ marginTop: '1rem' }}>
                <thead>
                  <tr>
                    <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Device Name</th>
                    <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">MAC Address</th>
                    <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Workspace</th>
                    <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Status</th>
                    <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {devices.map(device => (
                    <tr key={device.id}>
                      <td className="px-6 py-4 whitespace-nowrap font-medium text-white">{device.device_name}</td>
                      <td style={{ fontFamily: 'monospace', fontSize: '0.85rem' }}>{device.device_identifier}</td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="badge neutral">
                          {getTenantName(device.tenant_id)}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`badge ${device.status === 'online' ? 'active' : device.status === 'in_call' ? 'warning' : 'inactive'}`}>
                          {device.status}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                          <button className="p-1.5 text-muted hover:text-accent-danger hover:bg-red-50 rounded-lg transition-colors" onClick={() => handleDeleteDevice(device.id)} title="Delete Device">
                            <Trash2 size={16} />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                  {devices.length === 0 && (
                    <tr><td colSpan="5" style={{ textAlign: 'center', padding: '2rem' }}>No devices registered in the system.</td></tr>
                  )}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}

      {/* Workspace Modal */}
      <Modal isOpen={isTenantModalOpen} onClose={() => setIsTenantModalOpen(false)} title={isEditingTenant ? "Edit Client Workspace" : "Provision New Client Workspace"}>
        <form onSubmit={handleTenantSubmit} className="grid grid-cols-2" style={{ gap: '1rem' }}>
          <div className="flex flex-col gap-1.5" style={{ gridColumn: 'span 2' }}>
            <label className="text-sm font-medium text-gray-200">Company / Client Name</label>
            <input type="text" name="name" className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow w-full" value={tenantFormData.name} onChange={handleTenantInputChange} required />
          </div>
          <div className="input-group checkbox-label" style={{ gridColumn: 'span 2', display: 'flex', alignItems: 'center', gap: '0.5rem', marginTop: '0.5rem' }}>
            <input type="checkbox" name="is_active" id="tenant_is_active" checked={tenantFormData.is_active} onChange={handleTenantInputChange} />
            <label htmlFor="tenant_is_active" style={{ cursor: 'pointer' }}>Active Subscription</label>
          </div>
          <div style={{ gridColumn: 'span 2', display: 'flex', justifyContent: 'flex-end', gap: '1rem', marginTop: '1rem' }}>
            <button type="button" className="px-4 py-2 text-sm font-medium text-gray-200 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg hover:bg-[rgba(255,255,255,0.02)] transition-colors" onClick={() => setIsTenantModalOpen(false)}>Cancel</button>
            <button type="submit" className="px-4 py-2 rounded-lg font-medium inline-flex items-center gap-2 bg-accent-primary text-white hover:bg-accent-primary/80 transition-colors shadow-sm">{isEditingTenant ? "Save Changes" : "Create Workspace"}</button>
          </div>
        </form>
      </Modal>

      {/* User Modal */}
      <Modal isOpen={isUserModalOpen} onClose={() => setIsUserModalOpen(false)} title="Edit System User">
        <form onSubmit={handleUserSubmit} className="grid grid-cols-2" style={{ gap: '1rem' }}>
          <div className="flex flex-col gap-1.5" style={{ gridColumn: 'span 2' }}>
            <label className="text-sm font-medium text-gray-200">Assign to Workspace</label>
            <select name="tenant_id" className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow w-full" value={userFormData.tenant_id} onChange={handleUserInputChange}>
              <option value="">Unassigned (No Workspace)</option>
              {tenants.map(t => (
                <option key={t.id} value={t.id}>{t.name}</option>
              ))}
            </select>
          </div>
          <div className="input-group checkbox-label" style={{ gridColumn: 'span 2', display: 'flex', alignItems: 'center', gap: '0.5rem', marginTop: '0.5rem' }}>
            <input type="checkbox" name="is_superadmin" id="user_is_superadmin" checked={userFormData.is_superadmin} onChange={handleUserInputChange} />
            <label htmlFor="user_is_superadmin" style={{ cursor: 'pointer' }}>Grant Super Admin Privileges</label>
          </div>
          <div style={{ gridColumn: 'span 2', display: 'flex', justifyContent: 'flex-end', gap: '1rem', marginTop: '1rem' }}>
            <button type="button" className="px-4 py-2 text-sm font-medium text-gray-200 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg hover:bg-[rgba(255,255,255,0.02)] transition-colors" onClick={() => setIsUserModalOpen(false)}>Cancel</button>
            <button type="submit" className="px-4 py-2 rounded-lg font-medium inline-flex items-center gap-2 bg-accent-primary text-white hover:bg-accent-primary/80 transition-colors shadow-sm">Save User</button>
          </div>
        </form>
      </Modal>

    </div>
  );
};

export default Agency;
