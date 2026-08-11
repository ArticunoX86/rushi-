import React, { useState, useEffect } from 'react';
import api from '../api';
import { Smartphone, Plus, Trash2, CheckCircle, XCircle } from 'lucide-react';
import Modal from '../components/Modal';
import './Shared.css';

const Devices = () => {
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  
  const [formData, setFormData] = useState({
    device_name: '',
    device_identifier: '',
    phone_number: ''
  });

  const fetchDevices = async () => {
    setLoading(true);
    try {
      const res = await api.get('/devices');
      setDevices(res.data);
    } catch (error) {
      console.error('Failed to fetch devices', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDevices();
  }, []);

  const handleInputChange = (e) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/devices/register', formData);
      setIsModalOpen(false);
      setFormData({ device_name: '', device_identifier: '', phone_number: '' });
      fetchDevices();
    } catch (error) {
      console.error('Failed to add device', error);
      alert('Failed to add device. Device identifier might already exist.');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Remove this device?")) return;
    try {
      await api.delete(`/devices/${id}`);
      fetchDevices();
    } catch (error) {
      console.error('Failed to delete device', error);
    }
  };

  return (
    <div className="page-container">
      <header className="page-header">
        <div>
          <h1>Devices</h1>
          <p className="text-secondary">Manage mobile and SIP devices connected to the platform.</p>
        </div>
        <button className="btn btn-primary" onClick={() => setIsModalOpen(true)}>
          <Plus size={16} /> Add Device
        </button>
      </header>

      <div className="glass table-container">
        {loading ? (
          <div className="loading">Loading devices...</div>
        ) : devices.length === 0 ? (
          <div className="empty-state">
            <Smartphone size={48} className="text-secondary" style={{ margin: '0 auto 1rem', opacity: 0.5 }} />
            No devices configured.
          </div>
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th>Device Name</th>
                <th>Identifier (MAC/IMEI)</th>
                <th>Phone Number</th>
                <th>Last Seen</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {devices.map((device) => (
                <tr key={device.id}>
                  <td style={{ fontWeight: 500 }}>{device.device_name}</td>
                  <td style={{ fontFamily: 'monospace' }}>{device.device_identifier}</td>
                  <td>{device.phone_number || '-'}</td>
                  <td>{device.last_seen ? new Date(device.last_seen).toLocaleString() : 'Never'}</td>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      {device.status === 'ONLINE' ? <CheckCircle size={14} color="var(--success)" /> : <XCircle size={14} color="var(--text-secondary)" />}
                      <span className={`badge ${(device.status || 'OFFLINE').toLowerCase()}`}>
                        {device.status}
                      </span>
                    </div>
                  </td>
                  <td>
                    <button className="icon-btn" onClick={() => handleDelete(device.id)}>
                      <Trash2 size={16} color="var(--danger)" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Add Device">
        <form onSubmit={handleSubmit} className="grid grid-cols-1" style={{ gap: '1rem' }}>
          
          <div className="input-group">
            <label className="input-label">Device Name</label>
            <input type="text" name="device_name" className="input-field" value={formData.device_name} onChange={handleInputChange} placeholder="e.g. Sales Floor Android 1" required />
          </div>

          <div className="input-group">
            <label className="input-label">Device Identifier (IMEI or UUID)</label>
            <input type="text" name="device_identifier" className="input-field" value={formData.device_identifier} onChange={handleInputChange} required />
          </div>

          <div className="input-group">
            <label className="input-label">Assigned Phone Number (Optional)</label>
            <input type="text" name="phone_number" className="input-field" value={formData.phone_number} onChange={handleInputChange} placeholder="+1234567890" />
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '1rem', marginTop: '1rem' }}>
            <button type="button" className="btn" onClick={() => setIsModalOpen(false)}>Cancel</button>
            <button type="submit" className="btn btn-primary">Save Device</button>
          </div>

        </form>
      </Modal>
    </div>
  );
};

export default Devices;
