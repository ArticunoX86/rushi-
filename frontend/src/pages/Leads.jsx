import React, { useState, useEffect } from 'react';
import api from '../api';
import { UserPlus, CloudDownload, Phone, RefreshCw, Edit, Trash2 } from 'lucide-react';
import Modal from '../components/Modal';
import './Shared.css';

const Leads = () => {
  const [leads, setLeads] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isSyncing, setIsSyncing] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState({
    first_name: '', last_name: '', email: '', phone: '', source: 'Salesforce', status: 'NEW'
  });

  const fetchLeads = async () => {
    setLoading(true);
    try {
      const res = await api.get('/leads');
      setLeads(res.data);
    } catch (error) {
      console.error('Failed to fetch leads', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLeads();
  }, []);

  const handleSalesforceSync = async () => {
    setIsSyncing(true);
    try {
      await api.post('/salesforce/sync');
      await fetchLeads(); // refresh the list after syncing
    } catch (error) {
      console.error('Salesforce sync failed', error);
      alert('Failed to sync leads from Salesforce. Check API credentials.');
    } finally {
      setIsSyncing(false);
    }
  };

  const handleQuickCall = (leadId) => {
    // Navigate to WebRTC or Dispatch Call endpoint
    console.log("Dispatching call to lead", leadId);
    alert('AI Call dispatch triggered (coming soon!)');
  };

  const handleEditClick = (lead) => {
    setFormData(lead);
    setEditingId(lead.id);
    setIsEditing(true);
    setIsModalOpen(true);
  };

  const handleAddClick = () => {
    setFormData({
      first_name: '', last_name: '', email: '', phone: '', source: 'Manual', status: 'NEW'
    });
    setIsEditing(false);
    setEditingId(null);
    setIsModalOpen(true);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (isEditing) {
        await api.put(`/leads/${editingId}`, formData);
      } else {
        await api.post('/leads', formData);
      }
      setIsModalOpen(false);
      setIsEditing(false);
      setEditingId(null);
      fetchLeads();
    } catch (error) {
      console.error('Failed to save lead', error);
      alert('Failed to save lead. Please check inputs.');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this lead?")) return;
    try {
      await api.delete(`/leads/${id}`);
      fetchLeads();
    } catch (error) {
      console.error('Failed to delete lead', error);
    }
  };

  return (
    <div className="page-container">
      <header className="page-header">
        <div>
          <h1>Leads</h1>
          <p className="text-secondary">Manage customer leads and contact information.</p>
        </div>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <button 
            className="btn btn-secondary" 
            onClick={handleSalesforceSync}
            disabled={isSyncing}
          >
            {isSyncing ? (
              <><RefreshCw size={16} className="spin" /> Syncing...</>
            ) : (
              <><CloudDownload size={16} /> Sync from Salesforce</>
            )}
          </button>
          <button className="btn btn-primary" onClick={handleAddClick}>
            <UserPlus size={16} /> Add Lead
          </button>
        </div>
      </header>

      <div className="glass table-container">
        {loading ? (
          <div className="loading">Loading leads...</div>
        ) : leads.length === 0 ? (
          <div className="empty-state">
            No leads found. Click "Sync from Salesforce" to import data.
          </div>
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Phone</th>
                <th>Email</th>
                <th>Source</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {leads.map((lead) => (
                <tr key={lead.id}>
                  <td style={{ fontWeight: 500 }}>{lead.first_name} {lead.last_name}</td>
                  <td>{lead.phone || '-'}</td>
                  <td>{lead.email || '-'}</td>
                  <td><span className="badge">{lead.source || 'Salesforce'}</span></td>
                  <td>
                    <span className={`badge ${(lead.status || 'NEW').toLowerCase()}`}>
                      {lead.status || 'NEW'}
                    </span>
                  </td>
                  <td>
                    <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                      <button className="icon-btn" style={{ color: 'var(--success)' }} onClick={() => handleQuickCall(lead.id)} title="Quick Call">
                        <Phone size={16} />
                      </button>
                      <button className="icon-btn edit" onClick={() => handleEditClick(lead)} title="Edit Lead">
                        <Edit size={16} />
                      </button>
                      <button className="icon-btn delete" onClick={() => handleDelete(lead.id)} title="Delete Lead">
                        <Trash2 size={16} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title={isEditing ? "Edit Lead" : "Add New Lead"}>
        <form onSubmit={handleSubmit} className="grid grid-cols-2">
          
          <div className="input-group">
            <label className="input-label">First Name</label>
            <input type="text" name="first_name" className="input-field" value={formData.first_name} onChange={handleInputChange} required />
          </div>

          <div className="input-group">
            <label className="input-label">Last Name</label>
            <input type="text" name="last_name" className="input-field" value={formData.last_name} onChange={handleInputChange} required />
          </div>

          <div className="input-group" style={{ gridColumn: 'span 2' }}>
            <label className="input-label">Email</label>
            <input type="email" name="email" className="input-field" value={formData.email} onChange={handleInputChange} />
          </div>

          <div className="input-group" style={{ gridColumn: 'span 2' }}>
            <label className="input-label">Phone Number</label>
            <input type="text" name="phone" className="input-field" value={formData.phone} onChange={handleInputChange} />
          </div>
          
          <div className="input-group">
            <label className="input-label">Status</label>
            <select name="status" className="input-field" value={formData.status} onChange={handleInputChange}>
              <option value="NEW">New</option>
              <option value="CONTACTED">Contacted</option>
              <option value="QUALIFIED">Qualified</option>
              <option value="CONVERTED">Converted</option>
              <option value="LOST">Lost</option>
            </select>
          </div>

          <div className="input-group">
            <label className="input-label">Source</label>
            <input type="text" name="source" className="input-field" value={formData.source} onChange={handleInputChange} />
          </div>

          <div style={{ gridColumn: 'span 2', display: 'flex', justifyContent: 'flex-end', gap: '1rem', marginTop: '1rem' }}>
            <button type="button" className="btn" onClick={() => setIsModalOpen(false)}>Cancel</button>
            <button type="submit" className="btn btn-primary">Save Lead</button>
          </div>

        </form>
      </Modal>
    </div>
  );
};

export default Leads;
