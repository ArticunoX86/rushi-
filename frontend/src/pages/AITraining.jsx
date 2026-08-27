import { useState, useEffect, useCallback } from 'react';
import { Brain, Plus, Trash2, Edit3, ChevronDown, ChevronUp, Zap, TrendingUp, BookOpen, Shield, HelpCircle, Lightbulb, BarChart3, Upload, Sparkles, CheckCircle2, XCircle, AlertTriangle, Search, RefreshCw, Cloud, Database } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import api from '../api';

// ─── Constants ────────────────────────────────────────────────────────────────

const CATEGORIES = [
  { value: 'ALL', label: 'All Entries', icon: <Brain size={16} />, color: 'text-purple-400', bg: 'bg-purple-500/10' },
  { value: 'OBJECTION_HANDLING', label: 'Objection Handling', icon: <Shield size={16} />, color: 'text-red-400', bg: 'bg-red-500/10' },
  { value: 'FAQ', label: 'FAQ', icon: <HelpCircle size={16} />, color: 'text-blue-400', bg: 'bg-blue-500/10' },
  { value: 'SALES_PLAYBOOK', label: 'Sales Playbook', icon: <BookOpen size={16} />, color: 'text-green-400', bg: 'bg-green-500/10' },
  { value: 'PRODUCT_KNOWLEDGE', label: 'Product Knowledge', icon: <Lightbulb size={16} />, color: 'text-yellow-400', bg: 'bg-yellow-500/10' },
  { value: 'PERSONA_RULE', label: 'Persona Rules', icon: <Sparkles size={16} />, color: 'text-pink-400', bg: 'bg-pink-500/10' },
];

const CATEGORY_MAP = Object.fromEntries(CATEGORIES.slice(1).map(c => [c.value, c]));

const EMPTY_FORM = {
  title: '',
  category: 'OBJECTION_HANDLING',
  trigger_phrase: '',
  situation_context: '',
  ideal_response: '',
  tags: '',
  priority: 5,
  is_active: true,
};

// ─── Sub-components ───────────────────────────────────────────────────────────

const StatCard = ({ icon, label, value, accent }) => (
  <div className={`glass-panel rounded-2xl p-5 border border-[rgba(255,255,255,0.06)] flex items-center gap-4`}>
    <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${accent}`}>
      {icon}
    </div>
    <div>
      <p className="text-muted text-xs font-medium uppercase tracking-wider">{label}</p>
      <p className="text-white text-2xl font-bold">{value ?? '—'}</p>
    </div>
  </div>
);

const CategoryBadge = ({ category }) => {
  const meta = CATEGORY_MAP[category] || CATEGORIES[0];
  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${meta.bg} ${meta.color}`}>
      {meta.icon}
      {meta.label}
    </span>
  );
};

const PriorityDots = ({ priority }) => (
  <div className="flex gap-0.5" title={`Priority: ${priority}/10`}>
    {Array.from({ length: 10 }, (_, i) => (
      <div
        key={i}
        className={`w-2 h-2 rounded-full transition-colors ${
          i < priority ? 'bg-accent-primary' : 'bg-white/10'
        }`}
      />
    ))}
  </div>
);

// ─── Entry Form Modal ─────────────────────────────────────────────────────────

const EntryModal = ({ entry, onClose, onSave }) => {
  const [form, setForm] = useState(entry
    ? { ...entry, tags: Array.isArray(entry.tags) ? entry.tags.join(', ') : '' }
    : EMPTY_FORM
  );
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.title.trim() || !form.ideal_response.trim()) {
      setError('Title and Ideal Response are required.');
      return;
    }
    setSaving(true);
    setError('');
    try {
      const payload = {
        ...form,
        tags: form.tags ? form.tags.split(',').map(t => t.trim()).filter(Boolean) : [],
        priority: Number(form.priority),
      };
      if (entry) {
        await api.put(`/ai-training/${entry.id}`, payload);
      } else {
        await api.post('/ai-training', payload);
      }
      onSave();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save entry.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm px-4"
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      <motion.div
        initial={{ scale: 0.92, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.92, opacity: 0 }}
        className="w-full max-w-2xl glass-panel rounded-2xl border border-[rgba(255,255,255,0.08)] overflow-hidden"
      >
        {/* Header */}
        <div className="px-6 py-5 border-b border-[rgba(255,255,255,0.06)] flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-purple-500/20 flex items-center justify-center">
              <Brain size={18} className="text-purple-400" />
            </div>
            <h2 className="text-white font-semibold text-lg">
              {entry ? 'Edit Training Entry' : 'New Training Entry'}
            </h2>
          </div>
          <button onClick={onClose} className="text-muted hover:text-white transition-colors">
            <XCircle size={20} />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-4 max-h-[70vh] overflow-y-auto">
          {error && (
            <div className="flex items-center gap-2 p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm">
              <AlertTriangle size={16} />
              {error}
            </div>
          )}

          <div className="grid grid-cols-2 gap-4">
            <div className="col-span-2">
              <label className="block text-xs font-medium text-muted mb-1.5 uppercase tracking-wider">Title *</label>
              <input
                id="training-title"
                value={form.title}
                onChange={e => setForm(f => ({ ...f, title: e.target.value }))}
                placeholder="e.g., Not Interested Objection"
                className="w-full bg-[rgba(255,255,255,0.04)] border border-[rgba(255,255,255,0.08)] rounded-xl px-4 py-2.5 text-white text-sm placeholder:text-muted/50 focus:outline-none focus:border-accent-primary/50 transition-colors"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-muted mb-1.5 uppercase tracking-wider">Category</label>
              <select
                id="training-category"
                value={form.category}
                onChange={e => setForm(f => ({ ...f, category: e.target.value }))}
                className="w-full bg-[rgba(255,255,255,0.04)] border border-[rgba(255,255,255,0.08)] rounded-xl px-4 py-2.5 text-white text-sm focus:outline-none focus:border-accent-primary/50 transition-colors"
              >
                {CATEGORIES.slice(1).map(c => (
                  <option key={c.value} value={c.value}>{c.label}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-medium text-muted mb-1.5 uppercase tracking-wider">
                Priority (1–10)
              </label>
              <div className="flex items-center gap-3">
                <input
                  id="training-priority"
                  type="range"
                  min="1"
                  max="10"
                  value={form.priority}
                  onChange={e => setForm(f => ({ ...f, priority: e.target.value }))}
                  className="flex-1 accent-purple-500"
                />
                <span className="text-white font-bold w-4 text-center">{form.priority}</span>
              </div>
            </div>
          </div>

          <div>
            <label className="block text-xs font-medium text-muted mb-1.5 uppercase tracking-wider">
              Trigger Phrase
            </label>
            <input
              id="training-trigger"
              value={form.trigger_phrase}
              onChange={e => setForm(f => ({ ...f, trigger_phrase: e.target.value }))}
              placeholder="e.g., not interested, no thanks, too expensive"
              className="w-full bg-[rgba(255,255,255,0.04)] border border-[rgba(255,255,255,0.08)] rounded-xl px-4 py-2.5 text-white text-sm placeholder:text-muted/50 focus:outline-none focus:border-accent-primary/50 transition-colors"
            />
            <p className="text-muted/60 text-xs mt-1">Keywords the AI will look for in the customer's message to activate this entry.</p>
          </div>

          <div>
            <label className="block text-xs font-medium text-muted mb-1.5 uppercase tracking-wider">
              Situation Context
            </label>
            <input
              id="training-context"
              value={form.situation_context}
              onChange={e => setForm(f => ({ ...f, situation_context: e.target.value }))}
              placeholder="e.g., Customer expresses disinterest in the call"
              className="w-full bg-[rgba(255,255,255,0.04)] border border-[rgba(255,255,255,0.08)] rounded-xl px-4 py-2.5 text-white text-sm placeholder:text-muted/50 focus:outline-none focus:border-accent-primary/50 transition-colors"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-muted mb-1.5 uppercase tracking-wider">
              Ideal AI Response *
            </label>
            <textarea
              id="training-response"
              rows={4}
              value={form.ideal_response}
              onChange={e => setForm(f => ({ ...f, ideal_response: e.target.value }))}
              placeholder="What the AI should say or do in this situation..."
              className="w-full bg-[rgba(255,255,255,0.04)] border border-[rgba(255,255,255,0.08)] rounded-xl px-4 py-2.5 text-white text-sm placeholder:text-muted/50 focus:outline-none focus:border-accent-primary/50 transition-colors resize-none"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-muted mb-1.5 uppercase tracking-wider">
              Tags (comma-separated)
            </label>
            <input
              id="training-tags"
              value={form.tags}
              onChange={e => setForm(f => ({ ...f, tags: e.target.value }))}
              placeholder="e.g., not_interested, price_objection, budget"
              className="w-full bg-[rgba(255,255,255,0.04)] border border-[rgba(255,255,255,0.08)] rounded-xl px-4 py-2.5 text-white text-sm placeholder:text-muted/50 focus:outline-none focus:border-accent-primary/50 transition-colors"
            />
            <p className="text-muted/60 text-xs mt-1">Used for smart matching when customer messages contain these intent signals.</p>
          </div>

          <div className="flex items-center gap-3">
            <button
              type="button"
              id="training-active-toggle"
              onClick={() => setForm(f => ({ ...f, is_active: !f.is_active }))}
              className={`relative w-11 h-6 rounded-full transition-colors ${form.is_active ? 'bg-accent-primary' : 'bg-white/10'}`}
            >
              <span className={`absolute top-0.5 w-5 h-5 bg-white rounded-full shadow transition-transform ${form.is_active ? 'translate-x-5' : 'translate-x-0.5'}`} />
            </button>
            <span className="text-sm text-white">Active — inject this entry during live calls</span>
          </div>
        </form>

        {/* Footer */}
        <div className="px-6 py-4 border-t border-[rgba(255,255,255,0.06)] flex justify-end gap-3">
          <button onClick={onClose} className="px-4 py-2 rounded-xl text-sm text-muted hover:text-white transition-colors">
            Cancel
          </button>
          <button
            id="training-save-btn"
            onClick={handleSubmit}
            disabled={saving}
            className="px-5 py-2 rounded-xl text-sm font-medium bg-accent-primary text-white hover:bg-accent-primary/80 transition-colors disabled:opacity-50 flex items-center gap-2"
          >
            {saving ? <RefreshCw size={14} className="animate-spin" /> : <CheckCircle2 size={14} />}
            {saving ? 'Saving...' : (entry ? 'Update Entry' : 'Create Entry')}
          </button>
        </div>
      </motion.div>
    </motion.div>
  );
};

// ─── Training Entry Row ───────────────────────────────────────────────────────

const EntryRow = ({ entry, onEdit, onDelete }) => {
  const [expanded, setExpanded] = useState(false);

  return (
    <motion.div
      layout
      className={`glass-panel rounded-xl border transition-colors ${
        entry.is_active
          ? 'border-[rgba(255,255,255,0.06)] hover:border-[rgba(255,255,255,0.1)]'
          : 'border-[rgba(255,255,255,0.03)] opacity-50'
      }`}
    >
      {/* Row header */}
      <div className="flex items-center gap-4 px-5 py-4">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-3 flex-wrap">
            <CategoryBadge category={entry.category} />
            <h3 className="text-white font-medium text-sm truncate">{entry.title}</h3>
            {!entry.is_active && (
              <span className="text-xs text-muted bg-white/5 px-2 py-0.5 rounded-full">Inactive</span>
            )}
          </div>
          {entry.trigger_phrase && (
            <p className="text-muted/60 text-xs mt-1 truncate">
              Trigger: <span className="text-accent-primary/80 italic">"{entry.trigger_phrase}"</span>
            </p>
          )}
        </div>

        <div className="flex items-center gap-4 shrink-0">
          <div className="hidden md:block">
            <PriorityDots priority={entry.priority} />
          </div>
          <div className="text-center hidden sm:block">
            <p className="text-white font-bold text-sm">{entry.usage_count}</p>
            <p className="text-muted/60 text-xs">uses</p>
          </div>
          <div className="flex items-center gap-1">
            <button
              onClick={() => onEdit(entry)}
              className="w-8 h-8 rounded-lg flex items-center justify-center text-muted hover:text-accent-primary hover:bg-accent-primary/10 transition-colors"
              title="Edit"
            >
              <Edit3 size={14} />
            </button>
            <button
              onClick={() => onDelete(entry.id)}
              className="w-8 h-8 rounded-lg flex items-center justify-center text-muted hover:text-red-400 hover:bg-red-500/10 transition-colors"
              title="Deactivate"
            >
              <Trash2 size={14} />
            </button>
            <button
              onClick={() => setExpanded(x => !x)}
              className="w-8 h-8 rounded-lg flex items-center justify-center text-muted hover:text-white hover:bg-white/5 transition-colors"
            >
              {expanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
            </button>
          </div>
        </div>
      </div>

      {/* Expanded view */}
      <AnimatePresence>
        {expanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="overflow-hidden border-t border-[rgba(255,255,255,0.06)]"
          >
            <div className="px-5 py-4 grid grid-cols-1 md:grid-cols-2 gap-4">
              {entry.situation_context && (
                <div>
                  <p className="text-xs font-medium text-muted uppercase tracking-wider mb-1">When to Apply</p>
                  <p className="text-sm text-white/80">{entry.situation_context}</p>
                </div>
              )}
              <div className={entry.situation_context ? '' : 'col-span-2'}>
                <p className="text-xs font-medium text-muted uppercase tracking-wider mb-1">AI Response Script</p>
                <p className="text-sm text-white/80 leading-relaxed bg-white/[0.03] rounded-lg p-3 border border-white/5">
                  {entry.ideal_response}
                </p>
              </div>
              {entry.tags && entry.tags.length > 0 && (
                <div className="col-span-2">
                  <p className="text-xs font-medium text-muted uppercase tracking-wider mb-1">Tags</p>
                  <div className="flex flex-wrap gap-2">
                    {entry.tags.map(tag => (
                      <span key={tag} className="text-xs bg-white/5 text-muted px-2 py-0.5 rounded-full border border-white/10">
                        #{tag}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};

// ─── Main Page ────────────────────────────────────────────────────────────────

const AITraining = () => {
  const [entries, setEntries] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeCategory, setActiveCategory] = useState('ALL');
  const [search, setSearch] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editEntry, setEditEntry] = useState(null);
  const [seeding, setSeeding] = useState(false);
  const [seedResult, setSeedResult] = useState(null);
  const [notification, setNotification] = useState(null);

  const showNotif = (msg, type = 'success') => {
    setNotification({ msg, type });
    setTimeout(() => setNotification(null), 3500);
  };

  const [showPending, setShowPending] = useState(false);
  const [activeTab, setActiveTab] = useState('TRAINING'); // 'TRAINING' | 'SALESFORCE'
  const [sfDocs, setSfDocs] = useState([]);
  const [syncing, setSyncing] = useState(false);

  const fetchSfDocs = useCallback(async () => {
    try {
      const res = await api.get('/salesforce-knowledge');
      setSfDocs(res.data);
    } catch (err) {
      console.error(err);
    }
  }, []);

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const params = {};
      if (activeCategory !== 'ALL') params.category = activeCategory;
      const [entriesRes, statsRes] = await Promise.all([
        api.get('/ai-training', { params }),
        api.get('/ai-training/stats'),
      ]);
      setEntries(entriesRes.data);
      setStats(statsRes.data);
      if (activeTab === 'SALESFORCE') fetchSfDocs();
    } catch (err) {
      showNotif('Failed to load data.', 'error');
    } finally {
      setLoading(false);
    }
  }, [activeCategory, activeTab, fetchSfDocs]);

  useEffect(() => { fetchData(); }, [fetchData]);

  const handleSeed = async () => {
    setSeeding(true);
    setSeedResult(null);
    try {
      const res = await api.post('/ai-training/seed-defaults');
      setSeedResult(res.data);
      showNotif(`Seeded ${res.data.seeded_count} entries successfully!`);
      fetchData();
    } catch (err) {
      showNotif('Seeding failed.', 'error');
    } finally {
      setSeeding(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Deactivate this training entry?')) return;
    try {
      await api.delete(`/ai-training/${id}`);
      showNotif('Entry deactivated.');
      fetchData();
    } catch {
      showNotif('Failed to delete.', 'error');
    }
  };

  const filteredEntries = entries.filter(e => {
    if (showPending && e.is_active) return false;
    if (!showPending && !e.is_active && e.tags?.includes("Auto-Generated")) return false; // Hide pending by default unless toggle is on

    if (!search.trim()) return true;
    const q = search.toLowerCase();
    return (
      e.title?.toLowerCase().includes(q) ||
      e.trigger_phrase?.toLowerCase().includes(q) ||
      e.ideal_response?.toLowerCase().includes(q)
    );
  });

  const handleSyncSalesforce = async () => {
    setSyncing(true);
    try {
      await api.post('/salesforce-knowledge/sync');
      showNotif('Salesforce Sync started in background. Documents will appear shortly.');
      setTimeout(fetchSfDocs, 3000);
    } catch (err) {
      showNotif('Sync failed.', 'error');
    } finally {
      setSyncing(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Notification Toast */}
      <AnimatePresence>
        {notification && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className={`fixed top-6 right-6 z-50 flex items-center gap-2 px-4 py-3 rounded-xl shadow-lg text-sm font-medium ${
              notification.type === 'error'
                ? 'bg-red-500/20 border border-red-500/30 text-red-300'
                : 'bg-green-500/20 border border-green-500/30 text-green-300'
            }`}
          >
            {notification.type === 'error' ? <XCircle size={16} /> : <CheckCircle2 size={16} />}
            {notification.msg}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Page Header */}
      <div className="flex items-start justify-between gap-4 flex-wrap">
        <div>
          <div className="flex items-center gap-3 mb-1">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500/30 to-pink-500/30 flex items-center justify-center border border-purple-500/20">
              <Brain size={20} className="text-purple-400" />
            </div>
            <h1 className="text-2xl font-bold text-white">AI Training & Knowledge Base</h1>
          </div>
          <p className="text-muted text-sm ml-13 pl-13">
            Curate scripts, objection handlers, and sync Salesforce Knowledge.
          </p>
        </div>
        
        {/* Tab Switcher */}
        <div className="flex bg-white/5 p-1 rounded-xl border border-white/10">
          <button
            onClick={() => setActiveTab('TRAINING')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${activeTab === 'TRAINING' ? 'bg-accent-primary text-white shadow' : 'text-muted hover:text-white'}`}
          >
            Rules & Scripts
          </button>
          <button
            onClick={() => setActiveTab('SALESFORCE')}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${activeTab === 'SALESFORCE' ? 'bg-[#00a1e0] text-white shadow' : 'text-muted hover:text-white'}`}
          >
            <Cloud size={14} />
            Salesforce RAG
          </button>
        </div>

        <div className="flex items-center gap-3 flex-wrap">
          {activeTab === 'TRAINING' ? (
            <>
              <button
                id="seed-defaults-btn"
                onClick={handleSeed}
                disabled={seeding}
                className="flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium border border-accent-primary/30 text-accent-primary hover:bg-accent-primary/10 transition-colors disabled:opacity-50"
              >
                {seeding ? <RefreshCw size={14} className="animate-spin" /> : <Sparkles size={14} />}
                {seeding ? 'Seeding...' : 'Seed Defaults'}
              </button>
              <button
                id="add-training-entry-btn"
                onClick={() => { setEditEntry(null); setShowModal(true); }}
                className="flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium bg-accent-primary text-white hover:bg-accent-primary/80 transition-colors"
              >
                <Plus size={16} />
                Add Entry
              </button>
            </>
          ) : (
             <button
                onClick={handleSyncSalesforce}
                disabled={syncing}
                className="flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium bg-[#00a1e0] text-white hover:bg-[#00a1e0]/80 transition-colors disabled:opacity-50"
              >
                {syncing ? <RefreshCw size={16} className="animate-spin" /> : <Database size={16} />}
                {syncing ? 'Syncing...' : 'Sync from Salesforce'}
              </button>
          )}
        </div>
      </div>

      {/* Seed Result Banner */}
      <AnimatePresence>
        {seedResult && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="glass-panel rounded-xl p-4 border border-green-500/20 bg-green-500/5"
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <CheckCircle2 size={18} className="text-green-400" />
                <div>
                  <p className="text-white text-sm font-medium">
                    Seeded {seedResult.seeded_count} new entries · Skipped {seedResult.skipped_count} existing
                  </p>
                  <p className="text-muted text-xs mt-0.5">
                    Industry-standard real estate scripts are now active in your AI engine.
                  </p>
                </div>
              </div>
              <button onClick={() => setSeedResult(null)} className="text-muted hover:text-white">
                <XCircle size={16} />
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Stats Cards */}
      {stats && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <StatCard
            icon={<Brain size={22} className="text-purple-400" />}
            label="Total Entries"
            value={stats.total_entries}
            accent="bg-purple-500/15"
          />
          <StatCard
            icon={<CheckCircle2 size={22} className="text-green-400" />}
            label="Active Entries"
            value={stats.active_entries}
            accent="bg-green-500/15"
          />
          <StatCard
            icon={<Zap size={22} className="text-yellow-400" />}
            label="Total Injections"
            value={stats.total_usage_across_all}
            accent="bg-yellow-500/15"
          />
          <StatCard
            icon={<TrendingUp size={22} className="text-blue-400" />}
            label="Top Entry Uses"
            value={stats.top_entries?.[0]?.usage_count ?? 0}
            accent="bg-blue-500/15"
          />
        </div>
      )}

      {/* Category Breakdown */}
      {stats?.by_category && stats.by_category.length > 0 && (
        <div className="glass-panel rounded-2xl border border-[rgba(255,255,255,0.06)] p-5">
          <div className="flex items-center gap-2 mb-4">
            <BarChart3 size={16} className="text-muted" />
            <h2 className="text-sm font-semibold text-white uppercase tracking-wider">Category Breakdown</h2>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
            {stats.by_category.map(cat => {
              const meta = CATEGORY_MAP[cat.category] || CATEGORIES[0];
              const pct = stats.total_entries > 0 ? Math.round((cat.total / stats.total_entries) * 100) : 0;
              return (
                <div key={cat.category} className={`rounded-xl p-3 ${meta.bg} border border-white/5`}>
                  <div className={`flex items-center gap-1.5 mb-2 ${meta.color}`}>
                    {meta.icon}
                    <span className="text-xs font-medium truncate">{meta.label}</span>
                  </div>
                  <p className="text-white font-bold text-xl">{cat.total}</p>
                  <div className="flex items-center justify-between mt-1">
                    <span className="text-muted/60 text-xs">{cat.active} active</span>
                    <span className={`text-xs font-medium ${meta.color}`}>{pct}%</span>
                  </div>
                  <div className="mt-2 h-1 rounded-full bg-white/10 overflow-hidden">
                    <div className={`h-full rounded-full bg-current ${meta.color}`} style={{ width: `${pct}%` }} />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Filter Bar (Only for Training Tab) */}
      {activeTab === 'TRAINING' && (
        <div className="flex items-center gap-3 flex-wrap">
          <div className="relative flex-1 min-w-[200px]">
            <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted" />
            <input
              id="training-search"
              value={search}
              onChange={e => setSearch(e.target.value)}
              placeholder="Search entries..."
              className="w-full bg-[rgba(255,255,255,0.04)] border border-[rgba(255,255,255,0.08)] rounded-xl pl-9 pr-4 py-2.5 text-white text-sm placeholder:text-muted/50 focus:outline-none focus:border-accent-primary/50 transition-colors"
            />
          </div>
          <div className="flex items-center gap-2 flex-wrap">
            <button
              onClick={() => { setShowPending(!showPending); setActiveCategory('ALL'); }}
              className={`flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-medium transition-colors ${
                showPending
                  ? 'bg-orange-500/20 text-orange-400 border border-orange-500/50'
                  : 'text-muted hover:text-white bg-white/5 hover:bg-white/10 border border-transparent'
              }`}
            >
              <AlertTriangle size={14} />
              Pending Approvals
            </button>
            <div className="w-px h-6 bg-white/10 mx-1"></div>
            {CATEGORIES.map(cat => (
              <button
                key={cat.value}
                id={`filter-${cat.value.toLowerCase()}`}
                onClick={() => { setActiveCategory(cat.value); setShowPending(false); }}
                className={`flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-medium transition-colors ${
                  activeCategory === cat.value && !showPending
                    ? 'bg-accent-primary text-white'
                    : 'text-muted hover:text-white bg-white/5 hover:bg-white/10'
                }`}
              >
                {cat.icon}
                {cat.label}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Main Content Area */}
      {activeTab === 'TRAINING' ? (
        <div className="space-y-3">
          {loading ? (
            <div className="flex items-center justify-center py-16">
              <div className="flex flex-col items-center gap-3">
                <RefreshCw size={28} className="text-accent-primary animate-spin" />
                <p className="text-muted text-sm">Loading knowledge base...</p>
              </div>
            </div>
          ) : filteredEntries.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-16 text-center">
              <div className="w-16 h-16 rounded-2xl bg-purple-500/10 flex items-center justify-center mb-4">
                <Brain size={32} className="text-purple-400/50" />
              </div>
              <p className="text-white font-medium mb-1">
                {showPending ? 'No pending approvals' : search ? 'No matching entries' : 'No training entries yet'}
              </p>
              <p className="text-muted text-sm max-w-sm">
                {showPending ? 'All auto-generated learning opportunities have been reviewed.' : search
                  ? 'Try a different search term or clear the filter.'
                  : 'Click "Seed Defaults" to instantly load real estate scripts, or "Add Entry" to create your own.'}
              </p>
            </div>
          ) : (
            <AnimatePresence mode="popLayout">
              {filteredEntries.map(entry => (
                <EntryRow
                  key={entry.id}
                  entry={entry}
                  onEdit={(e) => { setEditEntry(e); setShowModal(true); }}
                  onDelete={handleDelete}
                />
              ))}
            </AnimatePresence>
          )}
        </div>
      ) : (
        <div className="space-y-4">
          <div className="glass-panel p-6 rounded-2xl border border-[rgba(255,255,255,0.06)]">
            <div className="flex gap-4">
              <div className="w-12 h-12 rounded-xl bg-[#00a1e0]/20 flex items-center justify-center shrink-0">
                <Database size={24} className="text-[#00a1e0]" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-white mb-1">Salesforce Vector Knowledge Base</h3>
                <p className="text-muted text-sm">
                  Documents synced from Salesforce are chunked and converted into vector embeddings using Google Gemini. 
                  During a live call, the AI performs a semantic search to instantly recall accurate facts from these documents.
                </p>
              </div>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {sfDocs.map(doc => (
              <div key={doc.id} className="glass-panel rounded-xl p-5 border border-[rgba(255,255,255,0.06)]">
                <div className="flex justify-between items-start mb-3">
                  <div className="bg-[#00a1e0]/20 text-[#00a1e0] px-2 py-1 rounded-md text-xs font-bold uppercase">
                    {doc.type}
                  </div>
                  <button 
                    onClick={async () => {
                      if(window.confirm('Delete this synced document and all its vectors?')) {
                        await api.delete(`/salesforce-knowledge/${doc.id}`);
                        fetchSfDocs();
                      }
                    }}
                    className="text-muted hover:text-red-400"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
                <h4 className="text-white font-medium text-base mb-2">{doc.title}</h4>
                <div className="flex justify-between items-center text-xs text-muted mt-4">
                  <span>{doc.chunks_count} Vector Chunks</span>
                  <span>ID: {doc.id.substring(0, 8)}...</span>
                </div>
              </div>
            ))}
            {sfDocs.length === 0 && (
              <div className="col-span-full flex flex-col items-center justify-center py-16 text-center">
                <Cloud size={40} className="text-[#00a1e0]/40 mb-4" />
                <p className="text-white font-medium mb-1">No Salesforce Knowledge Synced</p>
                <p className="text-muted text-sm">Click "Sync from Salesforce" to pull Knowledge Articles and Property details.</p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Modal */}
      <AnimatePresence>
        {showModal && (
          <EntryModal
            entry={editEntry}
            onClose={() => { setShowModal(false); setEditEntry(null); }}
            onSave={() => { setShowModal(false); setEditEntry(null); fetchData(); showNotif('Entry saved successfully!'); }}
          />
        )}
      </AnimatePresence>
    </div>
  );
};

export default AITraining;
