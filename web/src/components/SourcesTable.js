import React, { useState, useEffect } from 'react';
import axios from 'axios';
import DataTable from './DataTable';
import Modal from './Modal';
import '../App.css';

const API_URL = 'http://localhost:5000/api';

const SourcesTable = () => {
  const [data, setData] = useState([]);
  const [exchanges, setExchanges] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingData, setEditingData] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    exchange_uuid: '',
    telegram_group_id: '',
    message_sample_short: '',
    message_sample_long: ''
  });
  const [successMessage, setSuccessMessage] = useState('');

  const columns = [
    { headerName: 'Name', field: 'name', width: 150 },
    { headerName: 'Exchange', field: 'exchange_name', width: 120 },
    { headerName: 'Telegram Group ID', field: 'telegram_group_id', width: 150 },
    { headerName: 'Sample (Short)', field: 'message_sample_short', width: 200 },
    { headerName: 'Sample (Long)', field: 'message_sample_long', width: 200 },
    { headerName: 'Created', field: 'created_at', width: 180 },
    { headerName: 'Updated', field: 'updated_at', width: 180 }
  ];

  const fetchData = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await axios.get(`${API_URL}/sources`);
      setData(response.data);
    } catch (err) {
      setError(`Failed to load sources: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const fetchExchanges = async () => {
    try {
      const response = await axios.get(`${API_URL}/exchanges`);
      setExchanges(response.data);
    } catch (err) {
      console.error('Failed to load exchanges:', err);
    }
  };

  useEffect(() => {
    fetchData();
    fetchExchanges();
  }, []);

  const handleAddClick = () => {
    setEditingData(null);
    setFormData({
      name: '',
      exchange_uuid: '',
      telegram_group_id: '',
      message_sample_short: '',
      message_sample_long: ''
    });
    setIsModalOpen(true);
  };

  const handleEditClick = (row) => {
    setEditingData(row);
    setFormData({
      name: row.name,
      exchange_uuid: row.exchange_uuid,
      telegram_group_id: row.telegram_group_id,
      message_sample_short: row.message_sample_short || '',
      message_sample_long: row.message_sample_long || ''
    });
    setIsModalOpen(true);
  };

  const handleDeleteClick = async (row) => {
    try {
      await axios.delete(`${API_URL}/sources/${row.uuid}`);
      setSuccessMessage('Source deleted successfully');
      setTimeout(() => setSuccessMessage(''), 3000);
      fetchData();
    } catch (err) {
      setError(`Failed to delete source: ${err.message}`);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (editingData) {
        await axios.put(`${API_URL}/sources/${editingData.uuid}`, formData);
        setSuccessMessage('Source updated successfully');
      } else {
        await axios.post(`${API_URL}/sources`, formData);
        setSuccessMessage('Source created successfully');
      }
      setTimeout(() => setSuccessMessage(''), 3000);
      setIsModalOpen(false);
      fetchData();
    } catch (err) {
      setError(`Failed to save source: ${err.message}`);
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
        title="Signal Sources"
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
        title={editingData ? 'Edit Source' : 'Add New Source'}
        onClose={() => setIsModalOpen(false)}
        onSubmit={handleSubmit}
        submitLabel={editingData ? 'Update' : 'Create'}
        loading={loading}
      >
        <div className="form-group">
          <label className="form-label">Source Name *</label>
          <input
            type="text"
            name="name"
            className="form-input"
            value={formData.name}
            onChange={handleInputChange}
            placeholder="e.g., My Trading Group"
            required
          />
        </div>

        <div className="form-group">
          <label className="form-label">Exchange *</label>
          <select
            name="exchange_uuid"
            className="form-select"
            value={formData.exchange_uuid}
            onChange={handleInputChange}
            required
          >
            <option value="">Select an exchange</option>
            {exchanges.map(ex => (
              <option key={ex.uuid} value={ex.uuid}>
                {ex.name}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label className="form-label">Telegram Group ID *</label>
          <input
            type="number"
            name="telegram_group_id"
            className="form-input"
            value={formData.telegram_group_id}
            onChange={handleInputChange}
            placeholder="e.g., -1001234567890"
            required
          />
        </div>

        <div className="form-group">
          <label className="form-label">Message Sample (Short)</label>
          <textarea
            name="message_sample_short"
            className="form-textarea"
            value={formData.message_sample_short}
            onChange={handleInputChange}
            placeholder="Short message example"
          />
        </div>

        <div className="form-group">
          <label className="form-label">Message Sample (Long)</label>
          <textarea
            name="message_sample_long"
            className="form-textarea"
            value={formData.message_sample_long}
            onChange={handleInputChange}
            placeholder="Long message example"
          />
        </div>
      </Modal>
    </>
  );
};

export default SourcesTable;
