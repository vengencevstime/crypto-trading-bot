import React, { useState, useEffect } from 'react';
import axios from 'axios';
import DataTable from './DataTable';
import Modal from './Modal';
import '../App.css';

const API_URL = 'http://localhost:5000/api';

const SignalsTable = () => {
  const [data, setData] = useState([]);
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingData, setEditingData] = useState(null);
  const [formData, setFormData] = useState({
    creation_time: new Date().toISOString().slice(0, 16),
    source_uuid: '',
    source_entry_price: '',
    current_price: '',
    tp1: '',
    tp2: '',
    tp3: '',
    tp4: '',
    sl: ''
  });
  const [successMessage, setSuccessMessage] = useState('');

  const columns = [
    { headerName: 'Creation Time', field: 'creation_time', width: 180 },
    { headerName: 'Source UUID', field: 'source_uuid', width: 200 },
    { headerName: 'Entry Price', field: 'source_entry_price', width: 130 },
    { headerName: 'Current Price', field: 'current_price', width: 130 },
    { headerName: 'TP1', field: 'tp1', width: 100 },
    { headerName: 'TP2', field: 'tp2', width: 100 },
    { headerName: 'TP3', field: 'tp3', width: 100 },
    { headerName: 'TP4', field: 'tp4', width: 100 },
    { headerName: 'SL', field: 'sl', width: 100 },
    { headerName: 'Created', field: 'created_at', width: 180 },
    { headerName: 'Updated', field: 'updated_at', width: 180 }
  ];

  const fetchData = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await axios.get(`${API_URL}/signals?limit=100`);
      setData(response.data);
    } catch (err) {
      setError(`Failed to load signals: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const fetchSources = async () => {
    try {
      const response = await axios.get(`${API_URL}/sources`);
      setSources(response.data);
    } catch (err) {
      console.error('Failed to load sources:', err);
    }
  };

  useEffect(() => {
    fetchData();
    fetchSources();
  }, []);

  const handleAddClick = () => {
    setEditingData(null);
    setFormData({
      creation_time: new Date().toISOString().slice(0, 16),
      source_uuid: '',
      source_entry_price: '',
      current_price: '',
      tp1: '',
      tp2: '',
      tp3: '',
      tp4: '',
      sl: ''
    });
    setIsModalOpen(true);
  };

  const handleEditClick = (row) => {
    setEditingData(row);
    setFormData({
      creation_time: row.creation_time?.slice(0, 16) || '',
      source_uuid: row.source_uuid,
      source_entry_price: row.source_entry_price || '',
      current_price: row.current_price || '',
      tp1: row.tp1 || '',
      tp2: row.tp2 || '',
      tp3: row.tp3 || '',
      tp4: row.tp4 || '',
      sl: row.sl || ''
    });
    setIsModalOpen(true);
  };

  const handleDeleteClick = async (row) => {
    try {
      await axios.delete(`${API_URL}/signals/${row.id}`);
      setSuccessMessage('Signal deleted successfully');
      setTimeout(() => setSuccessMessage(''), 3000);
      fetchData();
    } catch (err) {
      setError(`Failed to delete signal: ${err.message}`);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const submitData = {
        ...formData,
        source_entry_price: formData.source_entry_price ? parseFloat(formData.source_entry_price) : null,
        current_price: formData.current_price ? parseFloat(formData.current_price) : null,
        tp1: formData.tp1 ? parseFloat(formData.tp1) : null,
        tp2: formData.tp2 ? parseFloat(formData.tp2) : null,
        tp3: formData.tp3 ? parseFloat(formData.tp3) : null,
        tp4: formData.tp4 ? parseFloat(formData.tp4) : null,
        sl: formData.sl ? parseFloat(formData.sl) : null
      };

      if (editingData) {
        await axios.put(`${API_URL}/signals/${editingData.id}`, submitData);
        setSuccessMessage('Signal updated successfully');
      } else {
        await axios.post(`${API_URL}/signals`, submitData);
        setSuccessMessage('Signal created successfully');
      }
      setTimeout(() => setSuccessMessage(''), 3000);
      setIsModalOpen(false);
      fetchData();
    } catch (err) {
      setError(`Failed to save signal: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  return (
    <>
      {successMessage && <div className="success-message">{successMessage}</div>}
      
      <DataTable
        title="Trading Signals"
        data={data}
        columns={columns}
        onAdd={handleAddClick}
        onEdit={handleEditClick}
        onDelete={handleDeleteClick}
        onRefresh={fetchData}
        loading={loading}
        error={error}
      />

      <Modal
        isOpen={isModalOpen}
        title={editingData ? 'Edit Signal' : 'Add New Signal'}
        onClose={() => setIsModalOpen(false)}
        onSubmit={handleSubmit}
        submitLabel={editingData ? 'Update' : 'Create'}
        loading={loading}
      >
        <div className="form-group">
          <label className="form-label">Creation Time (Tbilisi) *</label>
          <input
            type="datetime-local"
            name="creation_time"
            className="form-input"
            value={formData.creation_time}
            onChange={handleInputChange}
            required
          />
        </div>

        <div className="form-group">
          <label className="form-label">Source *</label>
          <select
            name="source_uuid"
            className="form-select"
            value={formData.source_uuid}
            onChange={handleInputChange}
            required
          >
            <option value="">Select a source</option>
            {sources.map(source => (
              <option key={source.uuid} value={source.uuid}>
                {source.name}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label className="form-label">Source Entry Price</label>
          <input
            type="number"
            name="source_entry_price"
            className="form-input"
            value={formData.source_entry_price}
            onChange={handleInputChange}
            placeholder="e.g., 0.03077"
            step="0.00000001"
          />
        </div>

        <div className="form-group">
          <label className="form-label">Current Price</label>
          <input
            type="number"
            name="current_price"
            className="form-input"
            value={formData.current_price}
            onChange={handleInputChange}
            placeholder="e.g., 0.03100"
            step="0.00000001"
          />
        </div>

        <h4 style={{ marginTop: '1.5rem', marginBottom: '1rem', color: '#333' }}>Take Profit Levels</h4>

        <div className="form-group">
          <label className="form-label">TP1</label>
          <input
            type="number"
            name="tp1"
            className="form-input"
            value={formData.tp1}
            onChange={handleInputChange}
            placeholder="Take Profit 1"
            step="0.00000001"
          />
        </div>

        <div className="form-group">
          <label className="form-label">TP2</label>
          <input
            type="number"
            name="tp2"
            className="form-input"
            value={formData.tp2}
            onChange={handleInputChange}
            placeholder="Take Profit 2"
            step="0.00000001"
          />
        </div>

        <div className="form-group">
          <label className="form-label">TP3</label>
          <input
            type="number"
            name="tp3"
            className="form-input"
            value={formData.tp3}
            onChange={handleInputChange}
            placeholder="Take Profit 3"
            step="0.00000001"
          />
        </div>

        <div className="form-group">
          <label className="form-label">TP4</label>
          <input
            type="number"
            name="tp4"
            className="form-input"
            value={formData.tp4}
            onChange={handleInputChange}
            placeholder="Take Profit 4"
            step="0.00000001"
          />
        </div>

        <div className="form-group">
          <label className="form-label">Stop Loss (SL)</label>
          <input
            type="number"
            name="sl"
            className="form-input"
            value={formData.sl}
            onChange={handleInputChange}
            placeholder="Stop Loss Price"
            step="0.00000001"
          />
        </div>
      </Modal>
    </>
  );
};

export default SignalsTable;
