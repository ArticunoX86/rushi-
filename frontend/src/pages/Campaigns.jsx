import React, { useState, useEffect } from 'react';
import api from '../api';
import { Play, Plus, Upload, Users, CheckCircle } from 'lucide-react';
import Modal from '../components/Modal';

const Campaigns = () => {
  const [campaigns, setCampaigns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [voiceAgents, setVoiceAgents] = useState([]);

  const [formData, setFormData] = useState({
    name: '',
    voice_agent_id: ''
  });
  
  const [file, setFile] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [campaignRes, agentRes] = await Promise.all([
        api.get('/campaigns'),
        api.get('/voice-agent')
      ]);
      setCampaigns(campaignRes.data);
      setVoiceAgents(agentRes.data);
    } catch (error) {
      console.error('Failed to fetch data', error);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // 1. Create Campaign
      const campRes = await api.post('/campaigns', formData);
      const newCampaign = campRes.data;
      
      // 2. Upload Leads if file selected
      if (file) {
        const formDataUpload = new FormData();
        formDataUpload.append('file', file);
        await api.post(`/campaigns/${newCampaign.id}/upload-leads`, formDataUpload, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
      }
      
      setIsModalOpen(false);
      setFormData({ name: '', voice_agent_id: '' });
      setFile(null);
      fetchData(); // Refresh list
    } catch (error) {
      console.error('Failed to create campaign', error);
      alert('Failed to create campaign.');
    }
  };

  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <header className="flex justify-between items-center pb-4 border-b border-[rgba(255,255,255,0.08)]">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight">Campaigns</h1>
          <p className="text-muted mt-1">Manage bulk AI calling campaigns.</p>
        </div>
        <button 
          className="inline-flex items-center gap-2 bg-accent-primary text-white px-4 py-2 rounded-lg font-medium shadow-sm hover:bg-accent-primary/80 hover:shadow transition-all"
          onClick={() => setIsModalOpen(true)}
        >
          <Plus size={18} /> New Campaign
        </button>
      </header>

      {loading ? (
        <div className="flex justify-center items-center py-20 text-muted animate-pulse">Loading campaigns...</div>
      ) : campaigns.length === 0 ? (
        <div className="glass-panel border border-[rgba(255,255,255,0.08)] border-dashed rounded-xl p-12 text-center flex flex-col items-center">
          <div className="w-16 h-16 bg-[rgba(255,255,255,0.02)] rounded-full flex items-center justify-center mb-4">
            <Upload size={32} className="text-muted" />
          </div>
          <h3 className="text-lg font-medium text-white mb-1">No campaigns found</h3>
          <p className="text-muted max-w-sm">Create a new campaign to upload leads and start calling in bulk.</p>
          <button 
            className="mt-6 inline-flex items-center gap-2 glass-panel border border-[rgba(255,255,255,0.15)] text-gray-200 px-4 py-2 rounded-lg font-medium hover:bg-[rgba(255,255,255,0.02)] transition-colors"
            onClick={() => setIsModalOpen(true)}
          >
            <Plus size={16} /> Create your first campaign
          </button>
        </div>
      ) : (
        <div className="glass-panel rounded-xl shadow-sm border border-[rgba(255,255,255,0.08)] overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-[rgba(255,255,255,0.02)]">
                <tr>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-muted uppercase tracking-wider">Campaign Name</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-muted uppercase tracking-wider">Status</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-muted uppercase tracking-wider">Voice Agent</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-muted uppercase tracking-wider">Leads</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-muted uppercase tracking-wider">Completed</th>
                  <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-muted uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody className="glass-panel divide-y divide-gray-200">
                {campaigns.map((camp) => (
                  <tr key={camp.id} className="hover:bg-[rgba(255,255,255,0.02)] transition-colors">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-white">{camp.name}</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        camp.status === 'active' 
                          ? 'bg-emerald-100 text-emerald-800' 
                          : 'bg-[rgba(255,255,255,0.05)] text-white'
                      }`}>
                        {camp.status.toUpperCase()}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-muted">
                      {voiceAgents.find(a => a.id === camp.voice_agent_id)?.name || 'None'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center text-sm text-muted">
                        <Users size={16} className="mr-2 text-muted" /> 
                        {camp.total_leads}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center text-sm text-muted">
                        <CheckCircle size={16} className="mr-2 text-muted" /> 
                        {camp.calls_completed}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <button className="inline-flex items-center gap-1.5 glass-panel border border-[rgba(255,255,255,0.15)] text-gray-200 hover:bg-[rgba(255,255,255,0.02)] px-3 py-1.5 rounded-md text-xs font-medium transition-colors shadow-sm">
                        <Play size={14} className="text-muted" /> Start
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="New Campaign">
        <form onSubmit={handleSubmit} className="space-y-5">
          
          <div>
            <label className="block text-sm font-medium text-gray-200 mb-1">Campaign Name</label>
            <input 
              type="text" 
              name="name" 
              className="w-full glass-panel border border-[rgba(255,255,255,0.15)] text-white text-sm rounded-lg focus:ring-accent-primary focus:border-accent-primary p-2.5 shadow-sm" 
              value={formData.name} 
              onChange={handleInputChange} 
              required 
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-200 mb-1">Select Voice Agent</label>
            <select 
              name="voice_agent_id" 
              className="w-full glass-panel border border-[rgba(255,255,255,0.15)] text-white text-sm rounded-lg focus:ring-accent-primary focus:border-accent-primary p-2.5 shadow-sm" 
              value={formData.voice_agent_id} 
              onChange={handleInputChange} 
              required
            >
              <option value="">-- Select an Agent --</option>
              {voiceAgents.map(agent => (
                <option key={agent.id} value={agent.id}>{agent.name}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-200 mb-1">Upload Leads (CSV)</label>
            <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-[rgba(255,255,255,0.15)] border-dashed rounded-lg hover:bg-[rgba(255,255,255,0.02)] cursor-pointer transition-colors relative">
              <div className="space-y-1 text-center">
                <Upload className="mx-auto h-12 w-12 text-muted" />
                <div className="flex text-sm text-muted">
                  <label htmlFor="file-upload" className="relative cursor-pointer bg-transparent rounded-md font-medium text-accent-primary hover:text-accent-primary focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-accent-primary">
                    <span>Upload a file</span>
                    <input id="file-upload" type="file" accept=".csv" className="sr-only" onChange={handleFileChange} />
                  </label>
                  <p className="pl-1">or drag and drop</p>
                </div>
                <p className="text-xs text-muted">CSV must contain: first_name, last_name, phone, email</p>
                {file && <p className="text-sm font-medium text-accent-tertiary mt-2">Selected: {file.name}</p>}
              </div>
              <input type="file" accept=".csv" onChange={handleFileChange} className="absolute inset-0 w-full h-full opacity-0 cursor-pointer" />
            </div>
          </div>

          <div className="flex justify-end gap-3 pt-4 border-t border-[rgba(255,255,255,0.08)] mt-6">
            <button 
              type="button" 
              className="px-4 py-2 text-sm font-medium text-gray-200 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg hover:bg-[rgba(255,255,255,0.02)] shadow-sm" 
              onClick={() => setIsModalOpen(false)}
            >
              Cancel
            </button>
            <button 
              type="submit" 
              className="px-4 py-2 text-sm font-medium text-white bg-accent-primary rounded-lg hover:bg-accent-primary/80 shadow-sm"
            >
              Create Campaign
            </button>
          </div>

        </form>
      </Modal>
    </div>
  );
};

export default Campaigns;
