import React, { useState, useEffect } from 'react';
import api from '../api';
import { PhoneOutgoing, Eye, PlayCircle, FileText } from 'lucide-react';
import Modal from '../components/Modal';
import './Shared.css';

const Calls = () => {
  const [calls, setCalls] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCall, setSelectedCall] = useState(null);

  useEffect(() => {
    const fetchCalls = async () => {
      try {
        const res = await api.get('/calls');
        setCalls(res.data);
      } catch (error) {
        console.error('Failed to fetch calls', error);
      } finally {
        setLoading(false);
      }
    };
    fetchCalls();
  }, []);

  const handleViewCall = (call) => {
    setSelectedCall(call);
  };

  const closeCallModal = () => {
    setSelectedCall(null);
  };

  return (
    <div className="page-container">
      <header className="page-header">
        <div>
          <h1>Calls & Dispatch</h1>
          <p className="text-secondary">View call history and dispatch new AI calls.</p>
        </div>
        <button className="btn btn-primary">
          <PhoneOutgoing size={16} /> New Call
        </button>
      </header>

      <div className="glass table-container">
        {loading ? (
          <div className="loading">Loading calls...</div>
        ) : calls.length === 0 ? (
          <div className="empty-state">No call history found.</div>
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th>Call ID</th>
                <th>Status</th>
                <th>Outcome</th>
                <th>Duration</th>
                <th>Date</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {calls.map((call) => (
                <tr key={call.id}>
                  <td style={{ fontFamily: 'monospace', fontSize: '0.8rem' }}>{call.id.substring(0,8)}...</td>
                  <td>
                    <span className={`badge ${(call.status || 'SCHEDULED').toLowerCase()}`}>
                      {call.status}
                    </span>
                  </td>
                  <td>{call.outcome || '-'}</td>
                  <td>{call.duration_seconds || 0}s</td>
                  <td>{new Date(call.created_at).toLocaleString()}</td>
                  <td>
                    <button className="icon-btn" onClick={() => handleViewCall(call)} title="View Details">
                      <Eye size={16} color="var(--accent-primary)" />
                    </button>
                  </td>
                </tr>
              ))}
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
              <div className="input-group">
                <label className="input-label"><PlayCircle size={14} style={{ display: 'inline', verticalAlign: 'middle', marginRight: '4px' }}/> Recording</label>
                <audio controls src={selectedCall.recording_url} style={{ width: '100%', outline: 'none' }} />
              </div>
            )}

            <div className="input-group">
              <label className="input-label"><FileText size={14} style={{ display: 'inline', verticalAlign: 'middle', marginRight: '4px' }}/> Summary</label>
              <div className="input-field" style={{ minHeight: '60px', backgroundColor: 'rgba(0,0,0,0.2)' }}>
                {selectedCall.summary || 'No summary available.'}
              </div>
            </div>

            <div className="input-group">
              <label className="input-label">Transcript</label>
              <div className="input-field" style={{ minHeight: '150px', maxHeight: '300px', overflowY: 'auto', backgroundColor: 'rgba(0,0,0,0.2)', whiteSpace: 'pre-wrap' }}>
                {selectedCall.transcript || 'No transcript available.'}
              </div>
            </div>
            
            <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '1rem' }}>
              <button className="btn btn-primary" onClick={closeCallModal}>Close</button>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default Calls;
