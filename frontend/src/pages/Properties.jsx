import React, { useState, useEffect } from 'react';
import api from '../api';
import { Plus, Trash2, Edit, Download, Building } from 'lucide-react';
import Modal from '../components/Modal';
import EmptyState from '../components/EmptyState';
import { downloadCSV } from '../utils/exportUtils';


const Properties = () => {
  const [properties, setProperties] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [formData, setFormData] = useState({
    title: '',
    property_type: 'RESIDENTIAL',
    listing_type: 'SALE',
    status: 'AVAILABLE',
    city: '',
    locality: '',
    address: '',
    price: '',
    bedrooms: 0,
    bathrooms: 0,
    area_sqft: 0,
    furnishing: 'UNFURNISHED',
    owner_name: '',
    owner_phone: ''
  });

  const fetchProperties = async () => {
    setLoading(true);
    try {
      const res = await api.get('/properties');
      setProperties(res.data);
    } catch (error) {
      console.error('Failed to fetch properties', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProperties();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'price' || name === 'bedrooms' || name === 'bathrooms' || name === 'area_sqft' 
        ? Number(value) 
        : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (isEditing) {
        await api.put(`/properties/${editingId}`, formData);
      } else {
        await api.post('/properties', formData);
      }
      setIsModalOpen(false);
      setIsEditing(false);
      setEditingId(null);
      setFormData({
        title: '', property_type: 'RESIDENTIAL', listing_type: 'SALE', status: 'AVAILABLE',
        city: '', locality: '', address: '', price: '', bedrooms: 0, bathrooms: 0, area_sqft: 0,
        furnishing: 'UNFURNISHED', owner_name: '', owner_phone: ''
      });
      fetchProperties();
    } catch (error) {
      console.error('Failed to save property', error);
      alert('Failed to save property. Please check inputs.');
    }
  };

  const handleEditClick = (prop) => {
    setFormData(prop);
    setEditingId(prop.id);
    setIsEditing(true);
    setIsModalOpen(true);
  };

  const handleAddClick = () => {
    setFormData({
      title: '', property_type: 'RESIDENTIAL', listing_type: 'SALE', status: 'AVAILABLE',
      city: '', locality: '', address: '', price: '', bedrooms: 0, bathrooms: 0, area_sqft: 0,
      furnishing: 'UNFURNISHED', owner_name: '', owner_phone: ''
    });
    setIsEditing(false);
    setEditingId(null);
    setIsModalOpen(true);
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this property?")) return;
    try {
      await api.delete(`/properties/${id}`);
      fetchProperties();
    } catch (error) {
      console.error('Failed to delete property', error);
    }
  };

  return (
    <div className="flex flex-col gap-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <header className="flex justify-between items-start mb-2">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight">Properties</h1>
          <p className="text-muted mt-1">Manage real estate listings and portfolios.</p>
        </div>
        <div className="flex gap-3">
          <button 
            className="px-4 py-2 rounded-lg font-medium inline-flex items-center gap-2 glass-panel border border-[rgba(255,255,255,0.08)] text-gray-200 hover:bg-[rgba(255,255,255,0.02)] transition-colors shadow-sm"
            onClick={() => downloadCSV(properties, 'properties_export')}
            disabled={properties.length === 0}
          >
            <Download size={16} className="text-muted" /> Export
          </button>
          <button 
            className="px-4 py-2 rounded-lg font-medium inline-flex items-center gap-2 bg-accent-primary text-white hover:bg-accent-primary/80 transition-colors shadow-sm"
            onClick={handleAddClick}
          >
            <Plus size={16} /> Add Property
          </button>
        </div>
      </header>

      <div className="glass-panel rounded-xl shadow-sm border border-[rgba(255,255,255,0.08)] overflow-hidden">
        {loading ? (
          <div className="p-12 text-center text-muted">Loading properties...</div>
        ) : properties.length === 0 ? (
          <EmptyState 
            icon={Building}
            title="No properties listed"
            description="Add your first real estate listing to begin managing your portfolio and running AI agent campaigns."
            actionButton={
              <button className="px-4 py-2 rounded-lg font-medium inline-flex items-center gap-2 bg-accent-primary text-white hover:bg-accent-primary/80 transition-colors shadow-sm" onClick={handleAddClick}>
                <Plus size={16} /> Add First Property
              </button>
            }
          />
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-[rgba(255,255,255,0.08)] bg-[rgba(255,255,255,0.02)]/50">
                  <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Title</th>
                  <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Location</th>
                  <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Type</th>
                  <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Price</th>
                  <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider">Status</th>
                  <th className="px-6 py-4 text-xs font-semibold text-muted uppercase tracking-wider text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
              {properties.map((prop) => (
                <tr key={prop.id} className="hover:bg-[rgba(255,255,255,0.02)]/50 transition-colors group">
                  <td className="px-6 py-4 whitespace-nowrap font-medium text-white">{prop.title}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-muted">{prop.locality}, {prop.city}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-muted">{prop.property_type} - {prop.listing_type}</td>
                  <td className="px-6 py-4 whitespace-nowrap font-medium text-white">${Number(prop.price).toLocaleString()}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      prop.status === 'AVAILABLE' ? 'bg-green-100 text-green-800' :
                      prop.status === 'SOLD' ? 'bg-[rgba(255,255,255,0.05)] text-white' :
                      'bg-blue-100 text-blue-800'
                    }`}>
                      {prop.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right">
                    <div className="flex items-center justify-end gap-2">
                      <button 
                        className="p-1.5 text-muted hover:text-accent-primary hover:bg-[rgba(139,92,246,0.1)] rounded-lg transition-colors" 
                        onClick={() => handleEditClick(prop)}
                      >
                        <Edit size={18} />
                      </button>
                      <button 
                        className="p-1.5 text-muted hover:text-accent-danger hover:bg-red-50 rounded-lg transition-colors" 
                        onClick={() => handleDelete(prop.id)}
                      >
                        <Trash2 size={18} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          </div>
        )}
      </div>

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title={isEditing ? "Edit Property" : "Add New Property"}>
        <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4">
          
          <div className="col-span-2 flex flex-col gap-1.5">
            <label className="text-sm font-medium text-gray-200">Property Title</label>
            <input type="text" name="title" className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow" value={formData.title} onChange={handleInputChange} required />
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-sm font-medium text-gray-200">Property Type</label>
            <select name="property_type" className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow" value={formData.property_type} onChange={handleInputChange}>
              <option value="RESIDENTIAL">Residential</option>
              <option value="COMMERCIAL">Commercial</option>
              <option value="LAND">Land</option>
              <option value="OTHER">Other</option>
            </select>
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-sm font-medium text-gray-200">Listing Type</label>
            <select name="listing_type" className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow" value={formData.listing_type} onChange={handleInputChange}>
              <option value="SALE">Sale</option>
              <option value="RENT">Rent</option>
              <option value="LEASE">Lease</option>
            </select>
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-sm font-medium text-gray-200">Price</label>
            <input type="number" name="price" className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow" value={formData.price} onChange={handleInputChange} required />
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-sm font-medium text-gray-200">City</label>
            <input type="text" name="city" className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow" value={formData.city} onChange={handleInputChange} required />
          </div>
          
          <div className="flex flex-col gap-1.5">
            <label className="text-sm font-medium text-gray-200">Locality</label>
            <input type="text" name="locality" className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow" value={formData.locality} onChange={handleInputChange} required />
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-sm font-medium text-gray-200">Address</label>
            <input type="text" name="address" className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow" value={formData.address} onChange={handleInputChange} required />
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-sm font-medium text-gray-200">Bedrooms</label>
            <input type="number" name="bedrooms" className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow" value={formData.bedrooms} onChange={handleInputChange} required />
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-sm font-medium text-gray-200">Bathrooms</label>
            <input type="number" name="bathrooms" className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow" value={formData.bathrooms} onChange={handleInputChange} required />
          </div>
          
          <div className="flex flex-col gap-1.5">
            <label className="text-sm font-medium text-gray-200">Area (SqFt)</label>
            <input type="number" name="area_sqft" className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow" value={formData.area_sqft} onChange={handleInputChange} required />
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-sm font-medium text-gray-200">Furnishing</label>
            <select name="furnishing" className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow" value={formData.furnishing} onChange={handleInputChange}>
              <option value="UNFURNISHED">Unfurnished</option>
              <option value="SEMI_FURNISHED">Semi-Furnished</option>
              <option value="FURNISHED">Furnished</option>
            </select>
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-sm font-medium text-gray-200">Owner Name</label>
            <input type="text" name="owner_name" className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow" value={formData.owner_name} onChange={handleInputChange} required />
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-sm font-medium text-gray-200">Owner Phone</label>
            <input type="text" name="owner_phone" className="px-3 py-2 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-accent-primary transition-shadow" value={formData.owner_phone} onChange={handleInputChange} required />
          </div>

          <div className="col-span-2 flex justify-end gap-3 mt-4 pt-4 border-t border-[rgba(255,255,255,0.08)]">
            <button type="button" className="px-4 py-2 text-sm font-medium text-gray-200 glass-panel border border-[rgba(255,255,255,0.15)] rounded-lg hover:bg-[rgba(255,255,255,0.02)] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent-primary transition-colors" onClick={() => setIsModalOpen(false)}>Cancel</button>
            <button type="submit" className="px-4 py-2 text-sm font-medium text-white bg-accent-primary border border-transparent rounded-lg hover:bg-accent-primary/80 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent-primary transition-colors">Save Property</button>
          </div>

        </form>
      </Modal>
    </div>
  );
};

export default Properties;
