import React, { useState, useEffect } from 'react';
import api from '../api';
import { PhoneOutgoing, Eye, PlayCircle, FileText, Download, PhoneCall } from 'lucide-react';
import Modal from '../components/Modal';
import EmptyState from '../components/EmptyState';
import { downloadCSV } from '../utils/exportUtils';


const Calls = () => {
  const [calls, setCalls] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCall, setSelectedCall] = useState(null);
  
  // Filtering and Sorting State
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('ALL');
  const [sortBy, setSortBy] = useState('date_desc');
  
  // New Call Modal State
  const [isNewCallModalOpen, setIsNewCallModalOpen] = useState(false);
  const [leads, setLeads] = useState([]);
  const [fetchingLeads, setFetchingLeads] = useState(false);
  const [dispatching, setDispatching] = useState(null);

  const fetchCalls = async () => {
    try {
      const res = await api.get('/calls/');
      setCalls(res.data);
    } catch (error) {
      console.error('Failed to fetch calls', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCalls();
  }, []);

  const openNewCallModal = async () => {
    setIsNewCallModalOpen(true);
    if (leads.length === 0) {
      setFetchingLeads(true);
      try {
        const res = await api.get('/leads');
        setLeads(res.data);
      } catch (error) {
        console.error('Failed to fetch leads', error);
      } finally {
        setFetchingLeads(false);
      }
    }
  };

  const handleDispatch = async (leadId) => {
    setDispatching(leadId);
    try {
      await api.post('/calls/start', { lead_id: leadId });
      // Refresh calls after short delay
      setTimeout(fetchCalls, 1000);
      setIsNewCallModalOpen(false);
    } catch (error) {
      console.error('Failed to dispatch call', error);
      alert('Failed to dispatch call');
    } finally {
      setDispatching(null);
    }
  };

  // Apply filters and sorting
  const filteredCalls = calls
    .filter(call => {
      if (statusFilter !== 'ALL' && call.status !== statusFilter) return false;
      if (searchTerm) {
        const term = searchTerm.toLowerCase();
        return (
          call.id.toLowerCase().includes(term) ||
          (call.outcome && call.outcome.toLowerCase().includes(term)) ||
          (call.summary && call.summary.toLowerCase().includes(term))
        );
      }
      return true;
    })
    .sort((a, b) => {
      if (sortBy === 'date_desc') return new Date(b.created_at) - new Date(a.created_at);
      if (sortBy === 'date_asc') return new Date(a.created_at) - new Date(b.created_at);
      if (sortBy === 'duration_desc') return (b.duration_seconds || 0) - (a.duration_seconds || 0);
      return 0;
    });

  const handleViewCall = (call) => {
    setSelectedCall(call);
  };

  const closeCallModal = () => {
    setSelectedCall(null);
  };

  return (
    <div className="flex flex-col gap-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <header className="flex justify-between items-start mb-2">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight">Calls & Dispatch</h1>
          <p className="text-muted mt-1">View call history and dispatch new AI calls.</p>
        </div>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', flexWrap: 'wrap' }}>
          <input 
            type="text" 
            placeholder="Search calls..." 
            className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow w-full" 
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
            style={{ margin: 0, minWidth: '200px' }}
          />
          <select 
            className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow w-full" 
            value={statusFilter} 
            onChange={e => setStatusFilter(e.target.value)}
            style={{ margin: 0, minWidth: '130px' }}
          >
            <option value="ALL">All Statuses</option>
            <option value="scheduled">Scheduled</option>
            <option value="in_progress">In Progress</option>
            <option value="completed">Completed</option>
            <option value="failed">Failed</option>
          </select>
          <select 
            className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow w-full" 
            value={sortBy} 
            onChange={e => setSortBy(e.target.value)}
            style={{ margin: 0, minWidth: '140px' }}
          >
            <option value="date_desc">Newest First</option>
            <option value="date_asc">Oldest First</option>
            <option value="duration_desc">Longest Duration</option>
          </select>
          <button 
            className="px-4 py-2 rounded-lg font-medium inline-flex items-center gap-2 glass-panel border border-[rgba(255,255,255,0.08)] text-gray-200 hover:bg-[rgba(255,255,255,0.02)] transition-colors shadow-sm"
            onClick={() => downloadCSV(filteredCalls, 'calls_export')}
            disabled={filteredCalls.length === 0}
          >
            <Download size={16} /> Export
          </button>
          <button className="px-4 py-2 rounded-lg font-medium inline-flex items-center gap-2 bg-accent-primary text-white hover:bg-accent-primary/80 transition-colors shadow-sm" onClick={openNewCallModal}>
            <PhoneOutgoing size={16} /> New Call
          </button>
        </div>
      </header>

      <div className="glass-panel rounded-xl shadow-sm border border-[rgba(255,255,255,0.08)] overflow-hidden">
        {loading ? (
          <div className="p-12 text-center text-muted">Loading calls...</div>
        ) : calls.length === 0 ? (
          <EmptyState 
            icon={PhoneCall}
            title="No call history"
            description="Your AI agents haven't made any calls yet. Trigger a manual call or set up a campaign to get started."
            actionButton={
              <button className="px-4 py-2 rounded-lg font-medium inline-flex items-center gap-2 bg-accent-primary text-white hover:bg-accent-primary/80 transition-colors shadow-sm">
                <PhoneOutgoing size={16} /> Dispatch First Call
              </button>
            }
          />
        ) : (
          <table className="w-full text-left border-collapse">
            <thead>
              <tr>
                <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Call ID</th>
                <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Status</th>
                <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Outcome</th>
                <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Duration</th>
                <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Date</th>
                <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredCalls.map((call) => (
                <tr key={call.id}>
                  <td style={{ fontFamily: 'monospace', fontSize: '0.8rem' }}>{call.id.substring(0,8)}...</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`badge ${(call.status || 'SCHEDULED').toLowerCase()}`}>
                      {call.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {call.outcome ? (
                      <span className={`badge ${call.outcome.toLowerCase()}`}>
                        {call.outcome.replace('_', ' ').toUpperCase()}
                      </span>
                    ) : '-'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">{call.duration_seconds || 0}s</td>
                  <td className="px-6 py-4 whitespace-nowrap">{new Date(call.created_at).toLocaleString()}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <button className="p-1.5 text-muted hover:text-accent-primary hover:bg-[rgba(139,92,246,0.1)] rounded-lg transition-colors" onClick={() => handleViewCall(call)} title="View Details">
                      <Eye size={16} color="var(--accent-primary)" />
                    </button>
                  </td>
                </tr>
              ))}
              {filteredCalls.length === 0 && (
                <tr>
                  <td colSpan="6" style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
                    No calls match your filters.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        )}
      </div>

      <Modal isOpen={!!selectedCall} onClose={closeCallModal} title="Call Details">
        {selectedCall && (
          <div className="grid grid-cols-1" style={{ gap: '1rem' }}>
            <div className="flex-between">
              <div>
                <strong>Status:</strong> <span className={`badge ${(selectedCall.status || '').toLowerCase()}`}>{selectedCall.status}</span>
              </div>
              <div>
                <strong>Duration:</strong> {selectedCall.duration_seconds}s
              </div>
            </div>
            
            {selectedCall.recording_url && (
              <div className="flex flex-col gap-1.5">
                <label className="text-sm font-medium text-gray-200"><PlayCircle size={14} style={{ display: 'inline', verticalAlign: 'middle', marginRight: '4px' }}/> Recording</label>
                <audio controls src={selectedCall.recording_url} style={{ width: '100%', outline: 'none' }} />
              </div>
            )}

            <div className="flex flex-col gap-1.5">
              <label className="text-sm font-medium text-gray-200"><FileText size={14} style={{ display: 'inline', verticalAlign: 'middle', marginRight: '4px' }}/> Summary</label>
              <div className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow w-full" style={{ minHeight: '60px', backgroundColor: 'rgba(0,0,0,0.02)' }}>
                {selectedCall.summary || 'No summary available.'}
              </div>
            </div>

            <div className="flex flex-col gap-1.5">
              <label className="text-sm font-medium text-gray-200">Transcript</label>
              <div className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow w-full" style={{ minHeight: '150px', maxHeight: '300px', overflowY: 'auto', backgroundColor: 'rgba(0,0,0,0.02)', whiteSpace: 'pre-wrap' }}>
                {selectedCall.transcript || 'No transcript available.'}
              </div>
            </div>
            
            <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '1rem' }}>
              <button className="px-4 py-2 rounded-lg font-medium inline-flex items-center gap-2 bg-accent-primary text-white hover:bg-accent-primary/80 transition-colors shadow-sm" onClick={closeCallModal}>Close</button>
            </div>
          </div>
        )}
      </Modal>

      {/* New Call Dispatch Modal */}
      <Modal isOpen={isNewCallModalOpen} onClose={() => setIsNewCallModalOpen(false)} title="Dispatch AI Call">
        <div style={{ marginBottom: '1rem' }}>
          <p className="text-muted mt-1">Select a lead below to immediately dispatch an AI voice agent call to them.</p>
        </div>
        
        {fetchingLeads ? (
          <div className="p-12 text-center text-muted">Loading leads...</div>
        ) : leads.length === 0 ? (
          <div className="p-12 text-center text-muted">No leads available to call. Please add a lead first.</div>
        ) : (
          <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
            <table className="w-full text-left border-collapse">
              <thead>
                <tr>
                  <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Lead Name</th>
                  <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Phone Number</th>
                  <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Action</th>
                </tr>
              </thead>
              <tbody>
                {leads.map(lead => (
                  <tr key={lead.id}>
                    <td className="px-6 py-4 whitespace-nowrap">{lead.first_name} {lead.last_name}</td>
                    <td className="px-6 py-4 whitespace-nowrap">{lead.phone}</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <button 
                        className="px-4 py-2 rounded-lg font-medium inline-flex items-center gap-2 bg-accent-primary text-white hover:bg-accent-primary/80 transition-colors shadow-sm" 
                        style={{ padding: '0.25rem 0.75rem', fontSize: '0.8rem' }}
                        onClick={() => handleDispatch(lead.id)}
                        disabled={dispatching === lead.id}
                      >
                        {dispatching === lead.id ? 'Calling...' : 'Start Call'}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default Calls;
