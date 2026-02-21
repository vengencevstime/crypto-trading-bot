import React, { useState, useEffect } from 'react';
import axios from 'axios';
import DataTable from './DataTable';
import Modal from './Modal';
import '../App.css';

const API_URL = 'http://localhost:5000/api';

const TradingPairsTable = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingData, setEditingData] = useState(null);
  const [formData, setFormData] = useState({ name: '' });
  const [successMessage, setSuccessMessage] = useState('');

  const columns = [
    { headerName: 'Name', field: 'name', width: 150 },
    { headerName: 'UUID', field: 'uuid', width: 250 },
    { headerName: 'Created', field: 'created_at', width: 180 },
    { headerName: 'Updated', field: 'updated_at', width: 180 }
  ];

  const fetchData = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await axios.get(`${API_URL}/trading-pairs`);
      setData(response.data);
    } catch (err) {
      setError(`Failed to load trading pairs: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleAddClick = () => {
    setEditingData(null);
    setFormData({ name: '' });
    setIsModalOpen(true);
  };

  const handleEditClick = (row) => {
    setEditingData(row);
    setFormData({ name: row.name });
    setIsModalOpen(true);
  };

  const handleDeleteClick = async (row) => {
    try {
      await axios.delete(`${API_URL}/trading-pairs/${row.uuid}`);
      setSuccessMessage('Trading pair deleted successfully');
      setTimeout(() => setSuccessMessage(''), 3000);
      fetchData();
    } catch (err) {
      setError(`Failed to delete trading pair: ${err.message}`);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (editingData) {
        await axios.put(`${API_URL}/trading-pairs/${editingData.uuid}`, formData);
        setSuccessMessage('Trading pair updated successfully');
      } else {
        await axios.post(`${API_URL}/trading-pairs`, formData);
        setSuccessMessage('Trading pair created successfully');
      }
      setTimeout(() => setSuccessMessage(''), 3000);
      setIsModalOpen(false);
      fetchData();
    } catch (err) {
      setError(`Failed to save trading pair: ${err.message}`);
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
        title="Trading Pairs"
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
        title={editingData ? 'Edit Trading Pair' : 'Add New Trading Pair'}
        onClose={() => setIsModalOpen(false)}
        onSubmit={handleSubmit}
        submitLabel={editingData ? 'Update' : 'Create'}
        loading={loading}
      >
        <div className="form-group">
          <label className="form-label">Pair Name *</label>
          <input
            type="text"
            name="name"
            className="form-input"
            value={formData.name}
            onChange={handleInputChange}
            placeholder="e.g., BTC/USDT"
            required
          />
        </div>
      </Modal>
    </>
  );
};

export default TradingPairsTable;
