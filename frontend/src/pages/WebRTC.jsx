import React, { useState } from 'react';
import { Phone, PhoneOff, Mic, MicOff, Volume2, VolumeX, Delete } from 'lucide-react';


const WebRTC = () => {
  const [phoneNumber, setPhoneNumber] = useState('');
  const [callStatus, setCallStatus] = useState('IDLE'); // IDLE, CALLING, CONNECTED
  const [isMuted, setIsMuted] = useState(false);
  const [speakerOn, setSpeakerOn] = useState(true);
  const [callDuration, setCallDuration] = useState(0);

  // Formatting utility
  const formatTime = (seconds) => {
    const m = Math.floor(seconds / 60).toString().padStart(2, '0');
    const s = (seconds % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
  };

  const handleKeyPress = (key) => {
    if (callStatus === 'IDLE') {
      setPhoneNumber(prev => prev + key);
    }
  };

  const handleDelete = () => {
    if (callStatus === 'IDLE') {
      setPhoneNumber(prev => prev.slice(0, -1));
    }
  };

  const handleCall = () => {
    if (!phoneNumber) return;
    setCallStatus('CALLING');
    
    // Simulate call connection after 2 seconds
    setTimeout(() => {
      setCallStatus('CONNECTED');
      // In a real app, we'd start a timer for callDuration here
    }, 2000);
  };

  const handleHangup = () => {
    setCallStatus('IDLE');
    setCallDuration(0);
    setPhoneNumber('');
  };

  return (
    <div className="flex flex-col gap-6 animate-in fade-in slide-in-from-bottom-4 duration-500" style={{ alignItems: 'center', justifyContent: 'center', height: 'calc(100vh - 4rem)' }}>
      
      <div className="glass-panel rounded-xl shadow-sm border border-[rgba(255,255,255,0.08)] overflow-hidden" style={{ width: '100%', maxWidth: '400px', padding: '2rem', borderRadius: '24px', textAlign: 'center', display: 'flex', flexDirection: 'column', gap: '1.5rem', boxShadow: '0 20px 40px rgba(0,0,0,0.3)' }}>
        
        {/* Header / Status Indicator */}
        <div>
          <h2 style={{ margin: 0, fontWeight: 600, fontSize: '1.5rem' }}>Browser Phone</h2>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem', marginTop: '0.5rem', color: callStatus === 'CONNECTED' ? 'var(--success)' : callStatus === 'CALLING' ? 'var(--warning)' : 'var(--text-secondary)' }}>
            <span className={`status-dot ${callStatus === 'CONNECTED' ? 'healthy' : callStatus === 'CALLING' ? 'offline' : ''}`} style={{ backgroundColor: callStatus === 'IDLE' ? 'var(--text-secondary)' : '' }}></span>
            <span style={{ fontSize: '0.875rem', fontWeight: 500 }}>
              {callStatus === 'IDLE' ? 'Ready' : callStatus === 'CALLING' ? 'Dialing...' : `Connected - ${formatTime(callDuration)}`}
            </span>
          </div>
        </div>

        {/* Number Display */}
        <div style={{ backgroundColor: 'rgba(0,0,0,0.3)', padding: '1rem', borderRadius: '12px', minHeight: '60px', display: 'flex', alignItems: 'center', justifyContent: 'center', position: 'relative' }}>
          <span style={{ fontSize: '1.5rem', letterSpacing: '2px', fontFamily: 'monospace' }}>
            {phoneNumber || 'Enter Number'}
          </span>
          {phoneNumber && callStatus === 'IDLE' && (
            <button className="p-1.5 text-muted hover:text-accent-primary hover:bg-[rgba(139,92,246,0.1)] rounded-lg transition-colors" onClick={handleDelete} style={{ position: 'absolute', right: '10px' }}>
              <Delete size={20} />
            </button>
          )}
        </div>

        {/* Dialpad */}
        <div className="grid grid-cols-3" style={{ gap: '1rem' }}>
          {['1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '0', '#'].map(key => (
            <button 
              key={key}
              onClick={() => handleKeyPress(key)}
              disabled={callStatus !== 'IDLE'}
              style={{
                aspectRatio: '1',
                borderRadius: '50%',
                border: '1px solid rgba(255,255,255,0.1)',
                background: 'rgba(255,255,255,0.05)',
                color: 'white',
                fontSize: '1.25rem',
                cursor: callStatus === 'IDLE' ? 'pointer' : 'not-allowed',
                transition: 'all 0.2s',
              }}
              onMouseOver={(e) => { if (callStatus === 'IDLE') e.target.style.background = 'rgba(255,255,255,0.1)'; }}
              onMouseOut={(e) => { if (callStatus === 'IDLE') e.target.style.background = 'rgba(255,255,255,0.05)'; }}
            >
              {key}
            </button>
          ))}
        </div>

        {/* Call Controls */}
        <div className="flex-between" style={{ marginTop: '1rem', padding: '0 1rem' }}>
          <button 
            className="p-1.5 text-muted hover:text-accent-primary hover:bg-[rgba(139,92,246,0.1)] rounded-lg transition-colors" 
            onClick={() => setIsMuted(!isMuted)} 
            style={{ 
              background: isMuted ? 'rgba(239, 68, 68, 0.2)' : 'rgba(255,255,255,0.1)', 
              color: isMuted ? 'var(--danger)' : 'white',
              padding: '1rem', 
              borderRadius: '50%' 
            }}
          >
            {isMuted ? <MicOff size={24} /> : <Mic size={24} />}
          </button>

          {callStatus === 'IDLE' ? (
            <button 
              onClick={handleCall}
              style={{ 
                background: 'var(--success)', 
                color: 'white', 
                border: 'none', 
                padding: '1.25rem', 
                borderRadius: '50%', 
                cursor: 'pointer',
                boxShadow: '0 4px 15px rgba(16, 185, 129, 0.4)'
              }}
            >
              <Phone size={28} />
            </button>
          ) : (
            <button 
              onClick={handleHangup}
              style={{ 
                background: 'var(--danger)', 
                color: 'white', 
                border: 'none', 
                padding: '1.25rem', 
                borderRadius: '50%', 
                cursor: 'pointer',
                boxShadow: '0 4px 15px rgba(239, 68, 68, 0.4)',
                animation: 'pulse 2s infinite'
              }}
            >
              <PhoneOff size={28} />
            </button>
          )}

          <button 
            className="p-1.5 text-muted hover:text-accent-primary hover:bg-[rgba(139,92,246,0.1)] rounded-lg transition-colors" 
            onClick={() => setSpeakerOn(!speakerOn)} 
            style={{ 
              background: !speakerOn ? 'rgba(255,255,255,0.05)' : 'rgba(255,255,255,0.1)', 
              color: 'white',
              padding: '1rem', 
              borderRadius: '50%' 
            }}
          >
            {speakerOn ? <Volume2 size={24} /> : <VolumeX size={24} />}
          </button>
        </div>

      </div>
    </div>
  );
};

export default WebRTC;
