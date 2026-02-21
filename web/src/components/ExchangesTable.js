import React, { useState, useEffect } from 'react';
import axios from 'axios';
import DataTable from './DataTable';
import Modal from './Modal';
import '../App.css';

const API_URL = 'http://localhost:5000/api';

const ExchangesTable = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingData, setEditingData] = useState(null);
  const [formData, setFormData] = useState({ name: '', api_key: '' });
  const [successMessage, setSuccessMessage] = useState('');

  const columns = [
    { headerName: 'Name', field: 'name', width: 150 },
    { headerName: 'API Key', field: 'api_key', width: 200 },
    { headerName: 'UUID', field: 'uuid', width: 250 },
    { headerName: 'Created', field: 'created_at', width: 180 },
    { headerName: 'Updated', field: 'updated_at', width: 180 }
  ];

  const fetchData = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await axios.get(`${API_URL}/exchanges`);
      setData(response.data);
    } catch (err) {
      setError(`Failed to load exchanges: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleAddClick = () => {
    setEditingData(null);
    setFormData({ name: '', api_key: '' });
    setIsModalOpen(true);
  };

  const handleEditClick = (row) => {
    setEditingData(row);
    setFormData({ name: row.name, api_key: row.api_key });
    setIsModalOpen(true);
  };

  const handleDeleteClick = async (row) => {
    try {
      await axios.delete(`${API_URL}/exchanges/${row.uuid}`);
      setSuccessMessage('Exchange deleted successfully');
      setTimeout(() => setSuccessMessage(''), 3000);
      fetchData();
    } catch (err) {
      setError(`Failed to delete exchange: ${err.message}`);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (editingData) {
        await axios.put(`${API_URL}/exchanges/${editingData.uuid}`, formData);
        setSuccessMessage('Exchange updated successfully');
      } else {
        await axios.post(`${API_URL}/exchanges`, formData);
        setSuccessMessage('Exchange created successfully');
      }
      setTimeout(() => setSuccessMessage(''), 3000);
      setIsModalOpen(false);
      fetchData();
    } catch (err) {
      setError(`Failed to save exchange: ${err.message}`);
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
        title="Exchanges"
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
        title={editingData ? 'Edit Exchange' : 'Add New Exchange'}
        onClose={() => setIsModalOpen(false)}
        onSubmit={handleSubmit}
        submitLabel={editingData ? 'Update' : 'Create'}
        loading={loading}
      >
        <div className="form-group">
          <label className="form-label">Exchange Name *</label>
          <input
            type="text"
            name="name"
            className="form-input"
            value={formData.name}
            onChange={handleInputChange}
            placeholder="e.g., MEXC, Kraken"
            required
          />
        </div>

        <div className="form-group">
          <label className="form-label">API Key *</label>
          <input
            type="password"
            name="api_key"
            className="form-input"
            value={formData.api_key}
            onChange={handleInputChange}
            placeholder="Enter API Key"
            required
          />
        </div>
      </Modal>
    </>
  );
};

export default ExchangesTable;
