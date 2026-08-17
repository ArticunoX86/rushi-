import React, { useState, useEffect } from 'react';
import api from '../api';
import { UserPlus, CloudDownload, Phone, RefreshCw, Edit, Trash2, Download, Users } from 'lucide-react';
import Modal from '../components/Modal';
import EmptyState from '../components/EmptyState';
import { downloadCSV } from '../utils/exportUtils';


const Leads = () => {
  const [leads, setLeads] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isSyncing, setIsSyncing] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState({
    first_name: '', last_name: '', email: '', phone: '', source: 'MANUAL', status: 'NEW'
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
      first_name: '', last_name: '', email: '', phone: '', source: 'MANUAL', status: 'NEW'
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
    <div className="flex flex-col gap-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <header className="flex justify-between items-start mb-2">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight">Leads</h1>
          <p className="text-muted mt-1">Manage customer leads and contact information.</p>
        </div>
        <div className="flex gap-3">
          <button 
            className="px-4 py-2 rounded-lg font-medium inline-flex items-center gap-2 glass-panel border border-[rgba(255,255,255,0.08)] text-gray-200 hover:bg-[rgba(255,255,255,0.02)] transition-colors shadow-sm"
            onClick={handleSalesforceSync}
            disabled={isSyncing}
          >
            {isSyncing ? (
              <><RefreshCw size={16} className="animate-spin text-accent-primary" /> Syncing...</>
            ) : (
              <><CloudDownload size={16} className="text-muted" /> Sync from Salesforce</>
            )}
          </button>
          <button 
            className="px-4 py-2 rounded-lg font-medium inline-flex items-center gap-2 glass-panel border border-[rgba(255,255,255,0.08)] text-gray-200 hover:bg-[rgba(255,255,255,0.02)] transition-colors shadow-sm"
            onClick={() => downloadCSV(leads, 'leads_export')}
            disabled={leads.length === 0}
          >
            <Download size={16} className="text-muted" /> Export
          </button>
          <button 
            className="px-4 py-2 rounded-lg font-medium inline-flex items-center gap-2 bg-accent-primary text-white hover:bg-accent-primary/80 transition-colors shadow-sm"
            onClick={handleAddClick}
          >
            <UserPlus size={16} /> Add Lead
          </button>
        </div>
      </header>

      <div className="glass-panel rounded-xl shadow-sm border border-[rgba(255,255,255,0.08)] overflow-hidden">
        {loading ? (
          <div className="p-12 text-center text-muted">Loading leads...</div>
        ) : leads.length === 0 ? (
          <EmptyState 
            icon={Users}
            title="No leads yet"
            description="Import your leads from Salesforce or add them manually to get started with AI calling."
            actionButton={
              <button className="px-4 py-2 rounded-lg font-medium inline-flex items-center gap-2 bg-accent-primary text-white hover:bg-accent-primary/80 transition-colors shadow-sm" onClick={handleAddClick}>
                <UserPlus size={16} /> Add First Lead
              </button>
            }
          />
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-[rgba(255,255,255,0.08)] bg-[rgba(255,255,255,0.02)]/50">
                  <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Name</th>
                  <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Phone</th>
                  <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Email</th>
                  <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Source</th>
                  <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Status</th>
                  <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
              {leads.map((lead) => (
                <tr key={lead.id} className="hover:bg-[rgba(255,255,255,0.02)]/50 transition-colors group">
                  <td className="px-6 py-4 whitespace-nowrap font-medium text-white">{lead.first_name} {lead.last_name}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-muted">{lead.phone || '-'}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-muted">{lead.email || '-'}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-[rgba(255,255,255,0.05)] text-white">
                      {lead.source || 'Salesforce'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      lead.status === 'NEW' ? 'bg-blue-100 text-blue-800' :
                      lead.status === 'CONTACTED' ? 'bg-yellow-100 text-yellow-800' :
                      lead.status === 'CONVERTED' ? 'bg-green-100 text-green-800' :
                      lead.status === 'NOT_INTERESTED' ? 'bg-red-100 text-red-800' :
                      'bg-[rgba(255,255,255,0.05)] text-white'
                    }`}>
                      {lead.status || 'NEW'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right">
                    <div className="flex items-center justify-end gap-2">
                      <button 
                        className="p-1.5 text-muted hover:text-green-600 hover:bg-green-50 rounded-lg transition-colors"
                        onClick={() => handleQuickCall(lead.id)} title="Quick Call"
                      >
                        <Phone size={18} />
                      </button>
                      <button 
                        className="p-1.5 text-muted hover:text-accent-primary hover:bg-[rgba(139,92,246,0.1)] rounded-lg transition-colors"
                        onClick={() => handleEditClick(lead)} title="Edit Lead"
                      >
                        <Edit size={18} />
                      </button>
                      <button 
                        className="p-1.5 text-muted hover:text-accent-danger hover:bg-red-50 rounded-lg transition-colors"
                        onClick={() => handleDelete(lead.id)} title="Delete Lead"
                      >
                        <Trash2 size={18} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          </div>
        )}
      </div>

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title={isEditing ? "Edit Lead" : "Add New Lead"}>
        <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4">
          
          <div className="flex flex-col gap-1.5">
            <label className="text-sm font-medium text-gray-200">First Name</label>
            <input type="text" name="first_name" className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow" value={formData.first_name} onChange={handleInputChange} required />
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-sm font-medium text-gray-200">Last Name</label>
            <input type="text" name="last_name" className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow" value={formData.last_name} onChange={handleInputChange} required />
          </div>

          <div className="col-span-2 flex flex-col gap-1.5">
            <label className="text-sm font-medium text-gray-200">Email</label>
            <input type="email" name="email" className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow" value={formData.email} onChange={handleInputChange} />
          </div>

          <div className="col-span-2 flex flex-col gap-1.5">
            <label className="text-sm font-medium text-gray-200">Phone Number</label>
            <input type="text" name="phone" className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow" value={formData.phone} onChange={handleInputChange} />
          </div>
          
          <div className="flex flex-col gap-1.5">
            <label className="text-sm font-medium text-gray-200">Status</label>
            <select name="status" className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow" value={formData.status} onChange={handleInputChange}>
              <option value="NEW">New</option>
              <option value="CONTACTED">Contacted</option>
              <option value="INTERESTED">Interested</option>
              <option value="NOT_INTERESTED">Not Interested</option>
              <option value="FOLLOW_UP">Follow Up</option>
              <option value="CONVERTED">Converted</option>
            </select>
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-sm font-medium text-gray-200">Source</label>
            <select name="source" className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow" value={formData.source} onChange={handleInputChange}>
              <option value="MANUAL">Manual</option>
              <option value="WEBSITE">Website</option>
              <option value="CSV_IMPORT">CSV Import</option>
              <option value="API">API</option>
            </select>
          </div>

          <div className="col-span-2 flex justify-end gap-3 mt-4 pt-4 border-t border-[rgba(255,255,255,0.08)]">
            <button type="button" className="px-4 py-2 text-sm font-medium text-gray-200 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg hover:bg-[rgba(255,255,255,0.02)] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent-primary transition-colors" onClick={() => setIsModalOpen(false)}>Cancel</button>
            <button type="submit" className="px-4 py-2 text-sm font-medium text-white bg-accent-primary border border-transparent rounded-lg hover:bg-accent-primary/80 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent-primary transition-colors">Save Lead</button>
          </div>

        </form>
      </Modal>
    </div>
  );
};

export default Leads;
