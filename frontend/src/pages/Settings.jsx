import { useState, useEffect } from 'react';
import api from '../api';
import { Users, Shield, Plus, Edit, Trash2 } from 'lucide-react';
import './Shared.css';

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

  // New Role Form State
  const [newRole, setNewRole] = useState({
    name: '', description: '', permissions: []
  });

  const availablePermissions = [
    'manage_users', 'manage_roles', 'view_dashboard', 'manage_properties', 
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

  const handlePermissionToggle = (perm) => {
    setNewRole(prev => ({
      ...prev,
      permissions: prev.permissions.includes(perm) 
        ? prev.permissions.filter(p => p !== perm)
        : [...prev.permissions, perm]
    }));
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <div>
          <h1>Settings</h1>
          <p className="text-secondary">Manage platform access and permissions.</p>
        </div>
      </div>

      <div className="tabs-container">
        <button 
          className={`tab-btn ${activeTab === 'members' ? 'active' : ''}`}
          onClick={() => setActiveTab('members')}
        >
          <Users size={18} /> Members
        </button>
        <button 
          className={`tab-btn ${activeTab === 'roles' ? 'active' : ''}`}
          onClick={() => setActiveTab('roles')}
        >
          <Shield size={18} /> Roles & Permissions
        </button>
      </div>

      <div className="tab-content">
        {loading ? (
          <div className="loading-state">Loading...</div>
        ) : activeTab === 'members' ? (
          <div className="glass" style={{ padding: '1.5rem' }}>
            <div className="card-header flex-between">
              <h2>Team Members</h2>
              <button className="btn btn-primary" onClick={() => setShowUserForm(!showUserForm)}>
                <Plus size={16} /> {showUserForm ? 'Cancel' : 'Add Member'}
              </button>
            </div>

            {showUserForm && (
              <div className="form-container">
                <form onSubmit={handleCreateUser} className="inline-form">
                  <div className="form-grid">
                    <div className="form-group input-group">
                      <label className="input-label">First Name</label>
                      <input className="input-field" required type="text" value={newUser.first_name} onChange={e => setNewUser({...newUser, first_name: e.target.value})} />
                    </div>
                    <div className="form-group input-group">
                      <label className="input-label">Last Name</label>
                      <input className="input-field" required type="text" value={newUser.last_name} onChange={e => setNewUser({...newUser, last_name: e.target.value})} />
                    </div>
                    <div className="form-group input-group">
                      <label className="input-label">Email</label>
                      <input className="input-field" required type="email" value={newUser.email} onChange={e => setNewUser({...newUser, email: e.target.value})} />
                    </div>
                    <div className="form-group input-group">
                      <label className="input-label">Phone</label>
                      <input className="input-field" required type="text" value={newUser.phone} onChange={e => setNewUser({...newUser, phone: e.target.value})} />
                    </div>
                    <div className="form-group input-group">
                      <label className="input-label">Password</label>
                      <input className="input-field" required type="password" value={newUser.password} onChange={e => setNewUser({...newUser, password: e.target.value})} />
                    </div>
                    <div className="form-group input-group">
                      <label className="input-label">Role</label>
                      <select className="input-field" required value={newUser.role_id} onChange={e => setNewUser({...newUser, role_id: e.target.value})}>
                        <option value="" disabled>Select a Role...</option>
                        {roles.map(r => (
                          <option key={r.id} value={r.id} className="select-option">{r.name}</option>
                        ))}
                      </select>
                    </div>
                  </div>
                  <div className="form-actions">
                    <button type="submit" className="btn btn-primary">Save Member</button>
                  </div>
                </form>
              </div>
            )}

            <div className="table-responsive">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Role</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {users.length === 0 ? (
                    <tr>
                      <td colSpan="5" className="empty-state">No members found.</td>
                    </tr>
                  ) : (
                    users.map(user => (
                      <tr key={user.id}>
                        <td>{user.first_name} {user.last_name}</td>
                        <td>{user.email}</td>
                        <td><span className="badge">{user.role?.name || 'No Role'}</span></td>
                        <td>
                          <span className={`status-badge ${user.is_active ? 'active' : 'inactive'}`}>
                            {user.is_active ? 'Active' : 'Inactive'}
                          </span>
                        </td>
                        <td className="actions-cell">
                          <button className="icon-btn edit"><Edit size={16} /></button>
                          <button className="icon-btn delete" onClick={() => handleDeleteUser(user.id)}><Trash2 size={16} /></button>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        ) : (
          <div className="glass" style={{ padding: '1.5rem' }}>
            <div className="card-header flex-between">
              <h2>Custom Roles</h2>
              <button className="btn btn-primary" onClick={() => setShowRoleForm(!showRoleForm)}>
                <Plus size={16} /> {showRoleForm ? 'Cancel' : 'Create Role'}
              </button>
            </div>

            {showRoleForm && (
              <div className="form-container">
                <form onSubmit={handleCreateRole} className="inline-form">
                  <div className="form-grid">
                    <div className="form-group input-group">
                      <label className="input-label">Role Name</label>
                      <input className="input-field" required type="text" value={newRole.name} onChange={e => setNewRole({...newRole, name: e.target.value})} placeholder="e.g., Viewer" />
                    </div>
                    <div className="form-group input-group">
                      <label className="input-label">Description</label>
                      <input className="input-field" type="text" value={newRole.description} onChange={e => setNewRole({...newRole, description: e.target.value})} placeholder="Describe what this role can do..." />
                    </div>
                  </div>
                  <div className="form-group input-group" style={{ marginTop: '1rem' }}>
                    <label className="input-label">Permissions</label>
                    <div className="permissions-grid">
                      {availablePermissions.map(perm => (
                        <label key={perm} className="checkbox-label">
                          <input 
                            type="checkbox" 
                            checked={newRole.permissions.includes(perm)}
                            onChange={() => handlePermissionToggle(perm)}
                          />
                          <span>{perm}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                  <div className="form-actions">
                    <button type="submit" className="btn btn-primary">Save Role</button>
                  </div>
                </form>
              </div>
            )}

            <div className="table-responsive">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Role Name</th>
                    <th>Description</th>
                    <th>Permissions</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {roles.length === 0 ? (
                    <tr>
                      <td colSpan="4" className="empty-state">No roles found.</td>
                    </tr>
                  ) : (
                    roles.map(role => (
                      <tr key={role.id}>
                        <td><strong>{role.name}</strong></td>
                        <td>{role.description}</td>
                        <td>
                          <div className="tags-container">
                            {role.permissions.map((p, i) => (
                              <span key={i} className="tag">{p}</span>
                            ))}
                          </div>
                        </td>
                        <td className="actions-cell">
                          <button className="icon-btn edit"><Edit size={16} /></button>
                          <button className="icon-btn delete" onClick={() => handleDeleteRole(role.id)}><Trash2 size={16} /></button>
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
    </div>
  );
};

export default Settings;
