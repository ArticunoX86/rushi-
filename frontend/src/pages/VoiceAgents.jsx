import React, { useState, useEffect } from 'react';
import api from '../api';
import { Mic, Plus, Edit2, Play, Volume2 } from 'lucide-react';
import Modal from '../components/Modal';
import './Shared.css';

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
    prompt: '',
    is_active: true
  });

  useEffect(() => {
    const fetchAgents = async () => {
      try {
        const res = await api.get('/voice-agent');
        // If backend returns empty, provide a mock agent for UI demonstration
        if (res.data.length === 0) {
          setAgents([{
            id: 'agent-1234',
            name: 'Real Estate Sales Agent',
            provider: 'ElevenLabs',
            voice_id: 'rachel',
            language: 'en-US',
            prompt: 'You are a helpful real estate assistant. Ask the client if they are looking to buy or rent.',
            is_active: true
          }]);
        } else {
          setAgents(res.data);
        }
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
        name: '', provider: 'ElevenLabs', voice_id: 'rachel', language: 'en-US', prompt: '', is_active: true
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
    // Simulate save
    if (editingAgent) {
      setAgents(prev => prev.map(a => a.id === editingAgent.id ? { ...formData, id: a.id } : a));
    } else {
      setAgents(prev => [...prev, { ...formData, id: `agent-${Math.random().toString().slice(2,8)}` }]);
    }
    setIsModalOpen(false);
  };

  return (
    <div className="page-container">
      <header className="page-header">
        <div>
          <h1>Voice Agents</h1>
          <p className="text-secondary">Configure AI personas and scripts.</p>
        </div>
        <button className="btn btn-primary" onClick={() => openModal()}>
          <Plus size={16} /> New Agent
        </button>
      </header>

      {loading ? (
        <div className="loading">Loading agents...</div>
      ) : agents.length === 0 ? (
        <div className="empty-state">
          <Mic size={48} className="text-secondary" style={{ margin: '0 auto 1rem', opacity: 0.5 }} />
          No voice agents configured yet.
        </div>
      ) : (
        <div className="grid grid-cols-3">
          {agents.map((agent) => (
            <div key={agent.id} className="glass" style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div className="flex-between">
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                  <div className="icon-btn" style={{ background: 'rgba(59, 130, 246, 0.1)', color: 'var(--accent-primary)' }}>
                    <Volume2 size={20} />
                  </div>
                  <div>
                    <h3 style={{ margin: 0, fontSize: '1.1rem' }}>{agent.name}</h3>
                    <span className="text-secondary" style={{ fontSize: '0.8rem' }}>{agent.provider}</span>
                  </div>
                </div>
                <span className={`badge ${agent.is_active ? 'active' : ''}`}>
                  {agent.is_active ? 'Active' : 'Inactive'}
                </span>
              </div>
              
              <div style={{ flex: 1, backgroundColor: 'rgba(0,0,0,0.2)', padding: '0.75rem', borderRadius: '8px', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                "{agent.prompt.length > 80 ? agent.prompt.slice(0,80) + '...' : agent.prompt}"
              </div>

              <div className="flex-between" style={{ borderTop: '1px solid var(--border-color)', paddingTop: '1rem', marginTop: 'auto' }}>
                <button className="btn" style={{ fontSize: '0.8rem', padding: '0.25rem 0.5rem' }}>
                  <Play size={14} /> Test Voice
                </button>
                <button className="icon-btn" onClick={() => openModal(agent)}>
                  <Edit2 size={16} />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title={editingAgent ? "Edit Agent" : "New Agent"}>
        <form onSubmit={handleSubmit} className="grid grid-cols-2" style={{ gap: '1rem' }}>
          
          <div className="input-group" style={{ gridColumn: 'span 2' }}>
            <label className="input-label">Agent Name</label>
            <input type="text" name="name" className="input-field" value={formData.name} onChange={handleInputChange} required />
          </div>

          <div className="input-group">
            <label className="input-label">Provider</label>
            <select name="provider" className="input-field" value={formData.provider} onChange={handleInputChange}>
              <option value="ElevenLabs">ElevenLabs</option>
              <option value="OpenAI">OpenAI (TTS)</option>
              <option value="PlayHT">Play.ht</option>
            </select>
          </div>

          <div className="input-group">
            <label className="input-label">Voice Model</label>
            <select name="voice_id" className="input-field" value={formData.voice_id} onChange={handleInputChange}>
              <option value="rachel">Rachel (Female, Calm)</option>
              <option value="drew">Drew (Male, Professional)</option>
              <option value="emily">Emily (Female, Energetic)</option>
            </select>
          </div>

          <div className="input-group" style={{ gridColumn: 'span 2' }}>
            <label className="input-label">System Prompt (Instructions)</label>
            <textarea 
              name="prompt" 
              className="input-field" 
              rows={4}
              style={{ resize: 'vertical' }}
              value={formData.prompt} 
              onChange={handleInputChange} 
              placeholder="You are an AI assistant calling a real estate lead..."
              required 
            />
          </div>

          <div className="input-group checkbox-label" style={{ gridColumn: 'span 2', display: 'flex', alignItems: 'center', gap: '0.5rem', marginTop: '0.5rem' }}>
            <input type="checkbox" name="is_active" id="is_active" checked={formData.is_active} onChange={handleInputChange} />
            <label htmlFor="is_active" style={{ cursor: 'pointer' }}>Set as Active Agent</label>
          </div>

          <div style={{ gridColumn: 'span 2', display: 'flex', justifyContent: 'flex-end', gap: '1rem', marginTop: '1rem' }}>
            <button type="button" className="btn" onClick={() => setIsModalOpen(false)}>Cancel</button>
            <button type="submit" className="btn btn-primary">Save Agent</button>
          </div>

        </form>
      </Modal>
    </div>
  );
};

export default VoiceAgents;
