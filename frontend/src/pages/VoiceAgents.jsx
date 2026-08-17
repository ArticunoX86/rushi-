import React, { useState, useEffect } from 'react';
import api from '../api';
import { Mic, Plus, Edit2, Play, Volume2 } from 'lucide-react';
import Modal from '../components/Modal';

const VoiceAgents = () => {
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingAgent, setEditingAgent] = useState(null);

  const [formData, setFormData] = useState({
    name: '',
    provider: 'ElevenLabs',
    voice_id: '',
    language: 'en-US',
    first_message: '',
    prompt: '',
    is_active: true
  });

  useEffect(() => {
    const fetchAgents = async () => {
      try {
        const res = await api.get('/voice-agent');
        setAgents(res.data);
      } catch (error) {
        console.error('Failed to fetch voice agents', error);
      } finally {
        setLoading(false);
      }
    };
    fetchAgents();
  }, []);

  const openModal = (agent = null) => {
    if (agent) {
      setEditingAgent(agent);
      setFormData(agent);
    } else {
      setEditingAgent(null);
      setFormData({
        name: '', provider: 'ElevenLabs', voice_id: 'rachel', language: 'en-US', first_message: '', prompt: '', is_active: true
      });
    }
    setIsModalOpen(true);
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingAgent) {
        const res = await api.put(`/voice-agent/${editingAgent.id}`, formData);
        setAgents(prev => prev.map(a => a.id === editingAgent.id ? res.data : a));
      } else {
        const res = await api.post('/voice-agent', formData);
        setAgents(prev => [...prev, res.data]);
      }
      setIsModalOpen(false);
    } catch (error) {
      console.error('Failed to save agent', error);
      alert('Failed to save voice agent.');
    }
  };

  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <header className="flex justify-between items-center pb-4 border-b border-[rgba(255,255,255,0.08)]">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight">Voice Agents</h1>
          <p className="text-muted mt-1">Configure AI personas and scripts.</p>
        </div>
        <button 
          className="inline-flex items-center gap-2 bg-accent-primary text-white px-4 py-2 rounded-lg font-medium shadow-sm hover:bg-accent-primary/80 hover:shadow transition-all"
          onClick={() => openModal()}
        >
          <Plus size={18} /> New Agent
        </button>
      </header>

      {loading ? (
        <div className="flex justify-center items-center py-20 text-muted animate-pulse">Loading agents...</div>
      ) : agents.length === 0 ? (
        <div className="glass-panel border border-[rgba(255,255,255,0.08)] border-dashed rounded-xl p-12 text-center flex flex-col items-center">
          <div className="w-16 h-16 bg-[rgba(255,255,255,0.02)] rounded-full flex items-center justify-center mb-4">
            <Mic size={32} className="text-muted" />
          </div>
          <h3 className="text-lg font-medium text-white mb-1">No voice agents</h3>
          <p className="text-muted max-w-sm">Create a new AI voice agent to handle your calls.</p>
          <button 
            className="mt-6 inline-flex items-center gap-2 glass-panel border border-[rgba(255,255,255,0.15)] text-gray-200 px-4 py-2 rounded-lg font-medium hover:bg-[rgba(255,255,255,0.02)] transition-colors"
            onClick={() => openModal()}
          >
            <Plus size={16} /> Create your first agent
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {agents.map((agent) => (
            <div key={agent.id} className="glass-panel rounded-xl shadow-sm border border-[rgba(255,255,255,0.08)] p-6 flex flex-col hover:shadow-md transition-shadow">
              <div className="flex justify-between items-start mb-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-[rgba(139,92,246,0.1)] text-accent-primary flex items-center justify-center">
                    <Volume2 size={20} />
                  </div>
                  <div>
                    <h3 className="text-lg font-bold text-white leading-tight">{agent.name}</h3>
                    <span className="text-xs font-medium text-muted bg-[rgba(255,255,255,0.05)] px-2 py-0.5 rounded-full mt-1 inline-block">{agent.provider}</span>
                  </div>
                </div>
                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                  agent.is_active 
                    ? 'bg-emerald-100 text-emerald-800' 
                    : 'bg-[rgba(255,255,255,0.05)] text-white'
                }`}>
                  {agent.is_active ? 'Active' : 'Inactive'}
                </span>
              </div>
              
              <div className="flex-1 bg-[rgba(255,255,255,0.02)] p-4 rounded-lg text-sm text-muted italic mb-4 border border-[rgba(255,255,255,0.08)] relative">
                <div className="absolute top-2 left-2 text-gray-300">"</div>
                <p className="indent-4">{agent.prompt.length > 100 ? agent.prompt.slice(0,100) + '...' : agent.prompt}</p>
                <div className="absolute bottom-2 right-2 text-gray-300">"</div>
              </div>

              <div className="flex justify-between items-center pt-4 border-t border-[rgba(255,255,255,0.08)] mt-auto">
                <button className="inline-flex items-center gap-1.5 glass-panel border border-[rgba(255,255,255,0.15)] text-gray-200 hover:bg-[rgba(255,255,255,0.02)] px-3 py-1.5 rounded-md text-xs font-medium transition-colors shadow-sm">
                  <Play size={14} className="text-accent-primary" /> Test Voice
                </button>
                <button 
                  className="p-1.5 text-muted hover:text-accent-primary hover:bg-[rgba(139,92,246,0.1)] rounded-md transition-colors"
                  onClick={() => openModal(agent)}
                >
                  <Edit2 size={16} />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title={editingAgent ? "Edit Agent" : "New Agent"}>
        <form onSubmit={handleSubmit} className="space-y-5">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            <div className="col-span-1 md:col-span-2">
              <label className="block text-sm font-medium text-gray-200 mb-1">Agent Name</label>
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
              <label className="block text-sm font-medium text-gray-200 mb-1">Provider</label>
              <select 
                name="provider" 
                className="w-full glass-panel border border-[rgba(255,255,255,0.15)] text-white text-sm rounded-lg focus:ring-accent-primary focus:border-accent-primary p-2.5 shadow-sm" 
                value={formData.provider} 
                onChange={handleInputChange}
              >
                <option value="ElevenLabs">ElevenLabs</option>
                <option value="Cartesia">Cartesia</option>
                <option value="OpenAI">OpenAI (TTS)</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-200 mb-1">Voice Model</label>
              <select 
                name="voice_id" 
                className="w-full glass-panel border border-[rgba(255,255,255,0.15)] text-white text-sm rounded-lg focus:ring-accent-primary focus:border-accent-primary p-2.5 shadow-sm" 
                value={formData.voice_id} 
                onChange={handleInputChange}
              >
                <option value="rachel">Rachel (Female, Calm)</option>
                <option value="drew">Drew (Male, Professional)</option>
                <option value="emily">Emily (Female, Energetic)</option>
                <option value="cartesia_en_1">Cartesia British (Male)</option>
              </select>
            </div>

            <div className="col-span-1 md:col-span-2">
              <label className="block text-sm font-medium text-gray-200 mb-1">First Message (Greeting)</label>
              <textarea 
                name="first_message" 
                className="w-full glass-panel border border-[rgba(255,255,255,0.15)] text-white text-sm rounded-lg focus:ring-accent-primary focus:border-accent-primary p-2.5 shadow-sm" 
                rows={2}
                value={formData.first_message || ''} 
                onChange={handleInputChange} 
                placeholder="Hi {lead_name}, this is Sarah from Real Estate..."
              />
              <p className="text-xs text-muted mt-1">Variables: <code className="bg-[rgba(255,255,255,0.05)] px-1 py-0.5 rounded">{"{lead_name}"}</code> <code className="bg-[rgba(255,255,255,0.05)] px-1 py-0.5 rounded">{"{city}"}</code></p>
            </div>

            <div className="col-span-1 md:col-span-2">
              <label className="block text-sm font-medium text-gray-200 mb-1">System Prompt (Sales Playbook)</label>
              <textarea 
                name="prompt" 
                className="w-full glass-panel border border-[rgba(255,255,255,0.15)] text-white text-sm rounded-lg focus:ring-accent-primary focus:border-accent-primary p-2.5 shadow-sm" 
                rows={6}
                value={formData.prompt} 
                onChange={handleInputChange} 
                placeholder="You are an AI assistant calling a real estate lead..."
                required 
              />
            </div>

            <div className="col-span-1 md:col-span-2 flex flex-col sm:flex-row gap-4 mt-2 bg-[rgba(255,255,255,0.02)] p-4 rounded-lg border border-[rgba(255,255,255,0.08)]">
              <label className="flex items-center gap-2 cursor-pointer">
                <input 
                  type="checkbox" 
                  name="is_active" 
                  className="w-4 h-4 text-accent-primary bg-[rgba(255,255,255,0.05)] border-[rgba(255,255,255,0.15)] rounded focus:ring-accent-primary focus:ring-2"
                  checked={formData.is_active} 
                  onChange={handleInputChange} 
                />
                <span className="text-sm font-medium text-gray-200">Set as Active Agent</span>
              </label>
              <label className="flex items-center gap-2 cursor-pointer">
                <input 
                  type="checkbox" 
                  name="interruptible" 
                  className="w-4 h-4 text-accent-primary bg-[rgba(255,255,255,0.05)] border-[rgba(255,255,255,0.15)] rounded focus:ring-accent-primary focus:ring-2"
                  checked={formData.interruptible || true} 
                  onChange={handleInputChange} 
                />
                <span className="text-sm font-medium text-gray-200">Allow User Interruption</span>
              </label>
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
              Save Agent
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};

export default VoiceAgents;
