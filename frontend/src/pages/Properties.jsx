import React, { useState, useEffect } from 'react';
import api from '../api';
import { Plus, Trash2, Edit } from 'lucide-react';
import Modal from '../components/Modal';
import './Shared.css';

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
    <div className="page-container">
      <header className="page-header">
        <div>
          <h1>Properties</h1>
          <p className="text-secondary">Manage real estate listings and portfolios.</p>
        </div>
        <button className="btn btn-primary" onClick={handleAddClick}>
          <Plus size={16} /> Add Property
        </button>
      </header>

      <div className="glass table-container">
        {loading ? (
          <div className="loading">Loading properties...</div>
        ) : properties.length === 0 ? (
          <div className="empty-state">No properties found.</div>
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th>Title</th>
                <th>Location</th>
                <th>Type</th>
                <th>Price</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {properties.map((prop) => (
                <tr key={prop.id}>
                  <td>{prop.title}</td>
                  <td>{prop.locality}, {prop.city}</td>
                  <td>{prop.property_type} - {prop.listing_type}</td>
                  <td>${Number(prop.price).toLocaleString()}</td>
                  <td>
                    <span className={`badge ${prop.status.toLowerCase()}`}>
                      {prop.status}
                    </span>
                  </td>
                  <td>
                    <button className="icon-btn edit" onClick={() => handleEditClick(prop)}>
                      <Edit size={16} />
                    </button>
                    <button className="icon-btn delete" onClick={() => handleDelete(prop.id)}>
                      <Trash2 size={16} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title={isEditing ? "Edit Property" : "Add New Property"}>
        <form onSubmit={handleSubmit} className="grid grid-cols-2">
          
          <div className="input-group" style={{ gridColumn: 'span 2' }}>
            <label className="input-label">Property Title</label>
            <input type="text" name="title" className="input-field" value={formData.title} onChange={handleInputChange} required />
          </div>

          <div className="input-group">
            <label className="input-label">Property Type</label>
            <select name="property_type" className="input-field" value={formData.property_type} onChange={handleInputChange}>
              <option value="RESIDENTIAL">Residential</option>
              <option value="COMMERCIAL">Commercial</option>
              <option value="LAND">Land</option>
              <option value="OTHER">Other</option>
            </select>
          </div>

          <div className="input-group">
            <label className="input-label">Listing Type</label>
            <select name="listing_type" className="input-field" value={formData.listing_type} onChange={handleInputChange}>
              <option value="SALE">Sale</option>
              <option value="RENT">Rent</option>
              <option value="LEASE">Lease</option>
            </select>
          </div>

          <div className="input-group">
            <label className="input-label">Price</label>
            <input type="number" name="price" className="input-field" value={formData.price} onChange={handleInputChange} required />
          </div>

          <div className="input-group">
            <label className="input-label">City</label>
            <input type="text" name="city" className="input-field" value={formData.city} onChange={handleInputChange} required />
          </div>
          
          <div className="input-group">
            <label className="input-label">Locality</label>
            <input type="text" name="locality" className="input-field" value={formData.locality} onChange={handleInputChange} required />
          </div>

          <div className="input-group">
            <label className="input-label">Address</label>
            <input type="text" name="address" className="input-field" value={formData.address} onChange={handleInputChange} required />
          </div>

          <div className="input-group">
            <label className="input-label">Bedrooms</label>
            <input type="number" name="bedrooms" className="input-field" value={formData.bedrooms} onChange={handleInputChange} required />
          </div>

          <div className="input-group">
            <label className="input-label">Bathrooms</label>
            <input type="number" name="bathrooms" className="input-field" value={formData.bathrooms} onChange={handleInputChange} required />
          </div>
          
          <div className="input-group">
            <label className="input-label">Area (SqFt)</label>
            <input type="number" name="area_sqft" className="input-field" value={formData.area_sqft} onChange={handleInputChange} required />
          </div>

          <div className="input-group">
            <label className="input-label">Furnishing</label>
            <select name="furnishing" className="input-field" value={formData.furnishing} onChange={handleInputChange}>
              <option value="UNFURNISHED">Unfurnished</option>
              <option value="SEMI_FURNISHED">Semi-Furnished</option>
              <option value="FURNISHED">Furnished</option>
            </select>
          </div>

          <div className="input-group">
            <label className="input-label">Owner Name</label>
            <input type="text" name="owner_name" className="input-field" value={formData.owner_name} onChange={handleInputChange} required />
          </div>

          <div className="input-group">
            <label className="input-label">Owner Phone</label>
            <input type="text" name="owner_phone" className="input-field" value={formData.owner_phone} onChange={handleInputChange} required />
          </div>

          <div style={{ gridColumn: 'span 2', display: 'flex', justifyContent: 'flex-end', gap: '1rem', marginTop: '1rem' }}>
            <button type="button" className="btn" onClick={() => setIsModalOpen(false)}>Cancel</button>
            <button type="submit" className="btn btn-primary">Save Property</button>
          </div>

        </form>
      </Modal>
    </div>
  );
};

export default Properties;
