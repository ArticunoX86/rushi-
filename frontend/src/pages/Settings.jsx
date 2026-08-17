import { useState, useEffect } from 'react';
import api from '../api';
import { Users, Shield, Plus, Edit, Trash2 } from 'lucide-react';
import Modal from '../components/Modal';


const Settings = () => {
  const [activeTab, setActiveTab] = useState('members');
  const [users, setUsers] = useState([]);
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(true);

  // Form States
  const [showRoleForm, setShowRoleForm] = useState(false);
  const [showUserForm, setShowUserForm] = useState(false);
  
  // New User Form State
  const [newUser, setNewUser] = useState({
    first_name: '', last_name: '', email: '', phone: '', password: '', role_id: ''
  });

  // Edit States
  const [editingUser, setEditingUser] = useState(null);
  const [editingRole, setEditingRole] = useState(null);

  // New Role Form State
  const [newRole, setNewRole] = useState({
    name: '', description: '', permissions: []
  });

  const availablePermissions = [
    'application_access', 'website_access', 'manage_users', 'manage_roles', 'view_dashboard', 'manage_properties', 
    'manage_leads', 'manage_calls', 'manage_agents', 'view_logs'
  ];

  useEffect(() => {
    fetchData();
  }, [activeTab]);

  const fetchData = async () => {
    setLoading(true);
    try {
      if (activeTab === 'members') {
        const [usersRes, rolesRes] = await Promise.all([
          api.get('/users'),
          api.get('/roles')
        ]);
        setUsers(usersRes.data);
        setRoles(rolesRes.data);
      } else {
        const res = await api.get('/roles');
        setRoles(res.data);
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteUser = async (id) => {
    if (!window.confirm("Are you sure you want to delete this user?")) return;
    try {
      await api.delete(`/users/${id}`);
      fetchData();
    } catch (err) {
      alert("Failed to delete user.");
    }
  };

  const handleDeleteRole = async (id) => {
    if (!window.confirm("Are you sure you want to delete this role?")) return;
    try {
      await api.delete(`/roles/${id}`);
      fetchData();
    } catch (err) {
      alert("Failed to delete role. It might be assigned to users.");
    }
  };

  const handleCreateUser = async (e) => {
    e.preventDefault();
    try {
      await api.post('/users', newUser);
      setShowUserForm(false);
      setNewUser({ first_name: '', last_name: '', email: '', phone: '', password: '', role_id: '' });
      fetchData();
    } catch (err) {
      alert(err.response?.data?.detail || "Failed to create user.");
    }
  };

  const handleCreateRole = async (e) => {
    e.preventDefault();
    try {
      await api.post('/roles', newRole);
      setShowRoleForm(false);
      setNewRole({ name: '', description: '', permissions: [] });
      fetchData();
    } catch (err) {
      alert(err.response?.data?.detail || "Failed to create role.");
    }
  };

  const handleUpdateUser = async (e) => {
    e.preventDefault();
    try {
      const payload = { ...editingUser };
      if (!payload.password) delete payload.password;
      await api.put(`/users/${editingUser.id}`, payload);
      setEditingUser(null);
      fetchData();
    } catch (err) {
      alert(err.response?.data?.detail || "Failed to update user.");
    }
  };

  const handleUpdateRole = async (e) => {
    e.preventDefault();
    try {
      await api.put(`/roles/${editingRole.id}`, editingRole);
      setEditingRole(null);
      fetchData();
    } catch (err) {
      alert(err.response?.data?.detail || "Failed to update role.");
    }
  };

  const handlePermissionToggle = (perm, isEditing = false) => {
    if (isEditing) {
      setEditingRole(prev => ({
        ...prev,
        permissions: prev.permissions.includes(perm)
          ? prev.permissions.filter(p => p !== perm)
          : [...prev.permissions, perm]
      }));
    } else {
      setNewRole(prev => ({
        ...prev,
        permissions: prev.permissions.includes(perm) 
          ? prev.permissions.filter(p => p !== perm)
          : [...prev.permissions, perm]
      }));
    }
  };

  return (
    <div className="flex flex-col gap-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="flex justify-between items-start mb-2">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight">Settings</h1>
          <p className="text-muted mt-1">Manage platform access and permissions.</p>
        </div>
      </div>

      <div className="flex gap-2 mb-8 bg-[rgba(255,255,255,0.02)] p-1.5 rounded-xl w-max border border-[rgba(255,255,255,0.05)]">
        <button 
          className={`px-5 py-2.5 font-medium text-sm rounded-lg flex items-center gap-2 transition-all ${activeTab === 'members' ? 'bg-[rgba(255,255,255,0.1)] text-white shadow-sm' : 'text-muted hover:text-gray-200 hover:bg-[rgba(255,255,255,0.05)]'}`}
          onClick={() => setActiveTab('members')}
        >
          <Users size={18} /> Members
        </button>
        <button 
          className={`px-5 py-2.5 font-medium text-sm rounded-lg flex items-center gap-2 transition-all ${activeTab === 'roles' ? 'bg-[rgba(255,255,255,0.1)] text-white shadow-sm' : 'text-muted hover:text-gray-200 hover:bg-[rgba(255,255,255,0.05)]'}`}
          onClick={() => setActiveTab('roles')}
        >
          <Shield size={18} /> Roles & Permissions
        </button>
      </div>

      <div className="tab-content">
        {loading ? (
          <div className="loading-state">Loading...</div>
        ) : activeTab === 'members' ? (
          <div className="glass-panel rounded-xl shadow-sm border border-[rgba(255,255,255,0.08)] overflow-hidden" style={{ padding: '1.5rem' }}>
            <div className="card-header flex-between">
              <h2>Team Members</h2>
              <button className="px-4 py-2 rounded-lg font-medium inline-flex items-center gap-2 bg-accent-primary text-white hover:bg-accent-primary/80 transition-colors shadow-sm" onClick={() => setShowUserForm(!showUserForm)}>
                <Plus size={16} /> {showUserForm ? 'Cancel' : 'Add Member'}
              </button>
            </div>

            {showUserForm && (
              <div className="bg-[rgba(255,255,255,0.02)] p-6 rounded-xl border border-[rgba(255,255,255,0.08)] mb-6">
                <form onSubmit={handleCreateUser} className="inline-form">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="form-group input-group">
                      <label className="text-sm font-medium text-gray-200">First Name</label>
                      <input className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow w-full" required type="text" value={newUser.first_name} onChange={e => setNewUser({...newUser, first_name: e.target.value})} />
                    </div>
                    <div className="form-group input-group">
                      <label className="text-sm font-medium text-gray-200">Last Name</label>
                      <input className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow w-full" required type="text" value={newUser.last_name} onChange={e => setNewUser({...newUser, last_name: e.target.value})} />
                    </div>
                    <div className="form-group input-group">
                      <label className="text-sm font-medium text-gray-200">Email</label>
                      <input className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow w-full" required type="email" value={newUser.email} onChange={e => setNewUser({...newUser, email: e.target.value})} />
                    </div>
                    <div className="form-group input-group">
                      <label className="text-sm font-medium text-gray-200">Phone</label>
                      <input className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow w-full" required type="text" value={newUser.phone} onChange={e => setNewUser({...newUser, phone: e.target.value})} />
                    </div>
                    <div className="form-group input-group">
                      <label className="text-sm font-medium text-gray-200">Password</label>
                      <input className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow w-full" required type="password" value={newUser.password} onChange={e => setNewUser({...newUser, password: e.target.value})} />
                    </div>
                    <div className="form-group input-group">
                      <label className="text-sm font-medium text-gray-200">Role</label>
                      <select className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow w-full" required value={newUser.role_id} onChange={e => setNewUser({...newUser, role_id: e.target.value})}>
                        <option value="" disabled>Select a Role...</option>
                        {roles.map(r => (
                          <option key={r.id} value={r.id} className="select-option">{r.name}</option>
                        ))}
                      </select>
                    </div>
                  </div>
                  <div className="flex justify-end gap-3 mt-4 pt-4 border-t border-[rgba(255,255,255,0.08)]">
                    <button type="submit" className="px-4 py-2 rounded-lg font-medium inline-flex items-center gap-2 bg-accent-primary text-white hover:bg-accent-primary/80 transition-colors shadow-sm">Save Member</button>
                  </div>
                </form>
              </div>
            )}

            <div className="table-responsive">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr>
                    <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Name</th>
                    <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Email</th>
                    <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Role</th>
                    <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Status</th>
                    <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {users.length === 0 ? (
                    <tr>
                      <td colSpan="5" className="p-12 text-center text-muted">No members found.</td>
                    </tr>
                  ) : (
                    users.map(user => (
                      <tr key={user.id}>
                        <td className="px-6 py-4 whitespace-nowrap">{user.first_name} {user.last_name}</td>
                        <td className="px-6 py-4 whitespace-nowrap">{user.email}</td>
                        <td className="px-6 py-4 whitespace-nowrap"><span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-[rgba(255,255,255,0.05)] text-white">{user.role?.name || 'No Role'}</span></td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`status-badge ${user.is_active ? 'active' : 'inactive'}`}>
                            {user.is_active ? 'Active' : 'Inactive'}
                          </span>
                        </td>
                        <td className="actions-cell">
                          <button className="p-1.5 text-muted hover:text-accent-primary hover:bg-[rgba(139,92,246,0.1)] rounded-lg transition-colors" onClick={() => setEditingUser(user)}><Edit size={16} /></button>
                          <button className="p-1.5 text-muted hover:text-accent-danger hover:bg-red-50 rounded-lg transition-colors" onClick={() => handleDeleteUser(user.id)}><Trash2 size={16} /></button>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        ) : (
          <div className="glass-panel rounded-xl shadow-sm border border-[rgba(255,255,255,0.08)] overflow-hidden" style={{ padding: '1.5rem' }}>
            <div className="card-header flex-between">
              <h2>Custom Roles</h2>
              <button className="px-4 py-2 rounded-lg font-medium inline-flex items-center gap-2 bg-accent-primary text-white hover:bg-accent-primary/80 transition-colors shadow-sm" onClick={() => setShowRoleForm(!showRoleForm)}>
                <Plus size={16} /> {showRoleForm ? 'Cancel' : 'Create Role'}
              </button>
            </div>

            {showRoleForm && (
              <div className="bg-[rgba(255,255,255,0.02)] p-6 rounded-xl border border-[rgba(255,255,255,0.08)] mb-6">
                <form onSubmit={handleCreateRole} className="inline-form">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="form-group input-group">
                      <label className="text-sm font-medium text-gray-200">Role Name</label>
                      <input className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow w-full" required type="text" value={newRole.name} onChange={e => setNewRole({...newRole, name: e.target.value})} placeholder="e.g., Viewer" />
                    </div>
                    <div className="form-group input-group">
                      <label className="text-sm font-medium text-gray-200">Description</label>
                      <input className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow w-full" type="text" value={newRole.description} onChange={e => setNewRole({...newRole, description: e.target.value})} placeholder="Describe what this role can do..." />
                    </div>
                  </div>
                  <div className="form-group input-group" style={{ marginTop: '1rem' }}>
                    <label className="text-sm font-medium text-gray-200">Permissions</label>
                    <div className="permissions-grid">
                      {availablePermissions.map(perm => (
                        <label key={perm} className="checkbox-label">
                          <input 
                            type="checkbox" 
                            checked={newRole.permissions.includes(perm)}
                            onChange={() => handlePermissionToggle(perm, false)}
                          />
                          <span>{perm}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                  <div className="flex justify-end gap-3 mt-4 pt-4 border-t border-[rgba(255,255,255,0.08)]">
                    <button type="submit" className="px-4 py-2 rounded-lg font-medium inline-flex items-center gap-2 bg-accent-primary text-white hover:bg-accent-primary/80 transition-colors shadow-sm">Save Role</button>
                  </div>
                </form>
              </div>
            )}

            <div className="table-responsive">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr>
                    <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Role Name</th>
                    <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Description</th>
                    <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Permissions</th>
                    <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {roles.length === 0 ? (
                    <tr>
                      <td colSpan="4" className="p-12 text-center text-muted">No roles found.</td>
                    </tr>
                  ) : (
                    roles.map(role => (
                      <tr key={role.id}>
                        <td className="px-6 py-4 whitespace-nowrap"><strong>{role.name}</strong></td>
                        <td className="px-6 py-4 whitespace-nowrap">{role.description}</td>
                        <td className="px-6 py-4 min-w-[350px]">
                          <div className="flex flex-wrap gap-2">
                            {role.permissions.map((p, i) => (
                              <span key={i} className="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-[rgba(255,255,255,0.05)] text-gray-200 border border-[rgba(255,255,255,0.1)]">{p}</span>
                            ))}
                          </div>
                        </td>
                        <td className="actions-cell">
                          <button className="p-1.5 text-muted hover:text-accent-primary hover:bg-[rgba(139,92,246,0.1)] rounded-lg transition-colors" onClick={() => setEditingRole(role)}><Edit size={16} /></button>
                          <button className="p-1.5 text-muted hover:text-accent-danger hover:bg-red-50 rounded-lg transition-colors" onClick={() => handleDeleteRole(role.id)}><Trash2 size={16} /></button>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>

      {/* Edit User Modal */}
      <Modal isOpen={!!editingUser} onClose={() => setEditingUser(null)} title="Edit Member">
        {editingUser && (
          <form onSubmit={handleUpdateUser} className="inline-form" style={{ padding: '1rem' }}>
            <div className="grid grid-cols-2 gap-4">
              <div className="form-group input-group">
                <label className="text-sm font-medium text-gray-200">First Name</label>
                <input className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow w-full" required type="text" value={editingUser.first_name} onChange={e => setEditingUser({...editingUser, first_name: e.target.value})} />
              </div>
              <div className="form-group input-group">
                <label className="text-sm font-medium text-gray-200">Last Name</label>
                <input className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow w-full" required type="text" value={editingUser.last_name} onChange={e => setEditingUser({...editingUser, last_name: e.target.value})} />
              </div>
              <div className="form-group input-group">
                <label className="text-sm font-medium text-gray-200">Email</label>
                <input className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow w-full" required type="email" value={editingUser.email} onChange={e => setEditingUser({...editingUser, email: e.target.value})} />
              </div>
              <div className="form-group input-group">
                <label className="text-sm font-medium text-gray-200">Phone</label>
                <input className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow w-full" required type="text" value={editingUser.phone} onChange={e => setEditingUser({...editingUser, phone: e.target.value})} />
              </div>
              <div className="form-group input-group">
                <label className="text-sm font-medium text-gray-200">Status</label>
                <select className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow w-full" value={editingUser.is_active} onChange={e => setEditingUser({...editingUser, is_active: e.target.value === 'true'})}>
                  <option value="true">Active</option>
                  <option value="false">Inactive</option>
                </select>
              </div>
              <div className="form-group input-group">
                <label className="text-sm font-medium text-gray-200">Role</label>
                <select className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow w-full" value={editingUser.role_id} onChange={e => setEditingUser({...editingUser, role_id: e.target.value})}>
                  {roles.map(r => (
                    <option key={r.id} value={r.id} className="select-option">{r.name}</option>
                  ))}
                </select>
              </div>
            </div>
            <div className="flex justify-end gap-3 mt-4 pt-4 border-t border-[rgba(255,255,255,0.08)]" style={{ marginTop: '1.5rem' }}>
              <button type="button" className="px-4 py-2 text-sm font-medium text-gray-200 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg hover:bg-[rgba(255,255,255,0.02)] transition-colors" onClick={() => setEditingUser(null)}>Cancel</button>
              <button type="submit" className="px-4 py-2 rounded-lg font-medium inline-flex items-center gap-2 bg-accent-primary text-white hover:bg-accent-primary/80 transition-colors shadow-sm">Save Changes</button>
            </div>
          </form>
        )}
      </Modal>

      {/* Edit Role Modal */}
      <Modal isOpen={!!editingRole} onClose={() => setEditingRole(null)} title="Edit Role">
        {editingRole && (
          <form onSubmit={handleUpdateRole} className="inline-form" style={{ padding: '1rem' }}>
            <div className="grid grid-cols-2 gap-4">
              <div className="form-group input-group">
                <label className="text-sm font-medium text-gray-200">Role Name</label>
                <input className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow w-full" required type="text" value={editingRole.name} onChange={e => setEditingRole({...editingRole, name: e.target.value})} />
              </div>
              <div className="form-group input-group">
                <label className="text-sm font-medium text-gray-200">Description</label>
                <input className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow w-full" type="text" value={editingRole.description} onChange={e => setEditingRole({...editingRole, description: e.target.value})} />
              </div>
            </div>
            <div className="form-group input-group" style={{ marginTop: '1rem' }}>
              <label className="text-sm font-medium text-gray-200">Permissions</label>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 mt-3">
                {availablePermissions.map(perm => (
                  <label key={perm} className="flex items-center gap-3 p-3 rounded-xl border border-[rgba(255,255,255,0.05)] bg-[rgba(255,255,255,0.02)] hover:bg-[rgba(255,255,255,0.05)] hover:border-[rgba(255,255,255,0.1)] cursor-pointer transition-all">
                    <input 
                      type="checkbox" 
                      className="w-4 h-4 rounded border-gray-600 bg-gray-700 text-accent-primary focus:ring-accent-primary focus:ring-offset-gray-900"
                      checked={editingRole.permissions?.includes(perm)}
                      onChange={() => handlePermissionToggle(perm, true)}
                    />
                    <span className="text-sm font-medium text-gray-300">{perm}</span>
                  </label>
                ))}
              </div>
            </div>
            <div className="flex justify-end gap-3 mt-4 pt-4 border-t border-[rgba(255,255,255,0.08)]" style={{ marginTop: '1.5rem' }}>
              <button type="button" className="px-4 py-2 text-sm font-medium text-gray-200 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg hover:bg-[rgba(255,255,255,0.02)] transition-colors" onClick={() => setEditingRole(null)}>Cancel</button>
              <button type="submit" className="px-4 py-2 rounded-lg font-medium inline-flex items-center gap-2 bg-accent-primary text-white hover:bg-accent-primary/80 transition-colors shadow-sm">Update Role</button>
            </div>
          </form>
        )}
      </Modal>
    </div>
  );
};

export default Settings;
