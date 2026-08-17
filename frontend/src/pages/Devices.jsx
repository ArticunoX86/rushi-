import React, { useState, useEffect } from 'react';
import api from '../api';
import { Smartphone, Plus, Trash2, CheckCircle, XCircle } from 'lucide-react';
import Modal from '../components/Modal';


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
    <div className="flex flex-col gap-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <header className="flex justify-between items-start mb-2">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight">Devices</h1>
          <p className="text-muted mt-1">Manage mobile and SIP devices connected to the platform.</p>
        </div>
        <button className="px-4 py-2 rounded-lg font-medium inline-flex items-center gap-2 bg-accent-primary text-white hover:bg-accent-primary/80 transition-colors shadow-sm" onClick={() => setIsModalOpen(true)}>
          <Plus size={16} /> Add Device
        </button>
      </header>

      <div className="glass-panel rounded-xl shadow-sm border border-[rgba(255,255,255,0.08)] overflow-hidden">
        {loading ? (
          <div className="p-12 text-center text-muted">Loading devices...</div>
        ) : devices.length === 0 ? (
          <div className="p-12 text-center text-muted">
            <Smartphone size={48} className="text-muted mt-1" style={{ margin: '0 auto 1rem', opacity: 0.5 }} />
            No devices configured.
          </div>
        ) : (
          <table className="w-full text-left border-collapse">
            <thead>
              <tr>
                <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Device Name</th>
                <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Identifier (MAC/IMEI)</th>
                <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Phone Number</th>
                <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Last Seen</th>
                <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Status</th>
                <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody>
              {devices.map((device) => (
                <tr key={device.id}>
                  <td className="px-6 py-4 whitespace-nowrap font-medium text-white">{device.device_name}</td>
                  <td style={{ fontFamily: 'monospace' }}>{device.device_identifier}</td>
                  <td className="px-6 py-4 whitespace-nowrap">{device.phone_number || '-'}</td>
                  <td className="px-6 py-4 whitespace-nowrap">{device.last_seen ? new Date(device.last_seen).toLocaleString() : 'Never'}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      {device.status === 'ONLINE' ? <CheckCircle size={14} color="var(--success)" /> : <XCircle size={14} color="var(--text-secondary)" />}
                      <span className={`badge ${(device.status || 'OFFLINE').toLowerCase()}`}>
                        {device.status}
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <button className="p-1.5 text-muted hover:text-accent-primary hover:bg-[rgba(139,92,246,0.1)] rounded-lg transition-colors" onClick={() => handleDelete(device.id)}>
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
          
          <div className="flex flex-col gap-1.5">
            <label className="text-sm font-medium text-gray-200">Device Name</label>
            <input type="text" name="device_name" className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow w-full" value={formData.device_name} onChange={handleInputChange} placeholder="e.g. Sales Floor Android 1" required />
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-sm font-medium text-gray-200">Device Identifier (IMEI or UUID)</label>
            <input type="text" name="device_identifier" className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow w-full" value={formData.device_identifier} onChange={handleInputChange} required />
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-sm font-medium text-gray-200">Assigned Phone Number (Optional)</label>
            <input type="text" name="phone_number" className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow w-full" value={formData.phone_number} onChange={handleInputChange} placeholder="+1234567890" />
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '1rem', marginTop: '1rem' }}>
            <button type="button" className="px-4 py-2 text-sm font-medium text-gray-200 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg hover:bg-[rgba(255,255,255,0.02)] transition-colors" onClick={() => setIsModalOpen(false)}>Cancel</button>
            <button type="submit" className="px-4 py-2 rounded-lg font-medium inline-flex items-center gap-2 bg-accent-primary text-white hover:bg-accent-primary/80 transition-colors shadow-sm">Save Device</button>
          </div>

        </form>
      </Modal>
    </div>
  );
};

export default Devices;
