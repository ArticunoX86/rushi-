import React, { useState, useEffect } from 'react';
import api from '../api';
import { UserPlus, CloudDownload, Phone, RefreshCw } from 'lucide-react';
import './Shared.css';

const Leads = () => {
  const [leads, setLeads] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isSyncing, setIsSyncing] = useState(false);

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

  return (
    <div className="page-container">
      <header className="page-header">
        <div>
          <h1>Leads</h1>
          <p className="text-secondary">Manage customer leads and contact information.</p>
        </div>
        <button 
          className="btn btn-primary" 
          onClick={handleSalesforceSync}
          disabled={isSyncing}
        >
          {isSyncing ? (
            <><RefreshCw size={16} className="spin" /> Syncing...</>
          ) : (
            <><CloudDownload size={16} /> Sync from Salesforce</>
          )}
        </button>
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
                    <button className="icon-btn" style={{ color: 'var(--success)' }} onClick={() => handleQuickCall(lead.id)} title="Quick Call">
                      <Phone size={16} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default Leads;
