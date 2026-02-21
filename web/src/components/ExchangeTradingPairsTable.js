import React, { useState, useEffect } from 'react';
import axios from 'axios';
import DataTable from './DataTable';
import Modal from './Modal';
import '../App.css';

const API_URL = 'http://localhost:5000/api';

const ExchangeTradingPairsTable = () => {
  const [data, setData] = useState([]);
  const [tradingPairs, setTradingPairs] = useState([]);
  const [exchanges, setExchanges] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingData, setEditingData] = useState(null);
  const [formData, setFormData] = useState({
    trading_pair_uuid: '',
    exchange_uuid: '',
    exchange_name: '',
    max_leverage: 1
  });
  const [successMessage, setSuccessMessage] = useState('');

  const columns = [
    { headerName: 'Trading Pair', field: 'trading_pair_name', width: 150 },
    { headerName: 'Exchange', field: 'exchange_name', width: 120 },
    { headerName: 'Max Leverage', field: 'max_leverage', width: 120 },
    { headerName: 'Created', field: 'created_at', width: 180 },
    { headerName: 'Updated', field: 'updated_at', width: 180 }
  ];

  const fetchData = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await axios.get(`${API_URL}/exchange-trading-pairs`);
      setData(response.data);
    } catch (err) {
      setError(`Failed to load exchange trading pairs: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const fetchDropdownData = async () => {
    try {
      const pairsRes = await axios.get(`${API_URL}/trading-pairs`);
      const exchangesRes = await axios.get(`${API_URL}/exchanges`);
      setTradingPairs(pairsRes.data);
      setExchanges(exchangesRes.data);
    } catch (err) {
      console.error('Failed to load dropdown data:', err);
    }
  };

  useEffect(() => {
    fetchData();
    fetchDropdownData();
  }, []);

  const handleAddClick = () => {
    setEditingData(null);
    setFormData({
      trading_pair_uuid: '',
      exchange_uuid: '',
      exchange_name: '',
      max_leverage: 1
    });
    setIsModalOpen(true);
  };

  const handleEditClick = (row) => {
    setEditingData(row);
    const selectedExchange = exchanges.find(e => e.uuid === row.exchange_uuid);
    setFormData({
      trading_pair_uuid: row.trading_pair_uuid,
      exchange_uuid: row.exchange_uuid,
      exchange_name: selectedExchange?.name || '',
      max_leverage: row.max_leverage || 1
    });
    setIsModalOpen(true);
  };

  const handleDeleteClick = async (row) => {
    try {
      await axios.delete(`${API_URL}/exchange-trading-pairs/${row.id}`);
      setSuccessMessage('Exchange trading pair deleted successfully');
      setTimeout(() => setSuccessMessage(''), 3000);
      fetchData();
    } catch (err) {
      setError(`Failed to delete exchange trading pair: ${err.message}`);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (editingData) {
        await axios.put(`${API_URL}/exchange-trading-pairs/${editingData.id}`, {
          max_leverage: parseInt(formData.max_leverage)
        });
        setSuccessMessage('Exchange trading pair updated successfully');
      } else {
        await axios.post(`${API_URL}/exchange-trading-pairs`, formData);
        setSuccessMessage('Exchange trading pair created successfully');
      }
      setTimeout(() => setSuccessMessage(''), 3000);
      setIsModalOpen(false);
      fetchData();
    } catch (err) {
      setError(`Failed to save exchange trading pair: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    
    if (name === 'exchange_uuid') {
      const selectedEx = exchanges.find(ex => ex.uuid === value);
      setFormData(prev => ({
        ...prev,
        [name]: value,
        exchange_name: selectedEx?.name || ''
      }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
  };

  return (
    <>
      {successMessage && <div className="success-message">{successMessage}</div>}
      
      <DataTable
        title="Exchange Trading Pairs"
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
        title={editingData ? 'Edit Exchange Trading Pair' : 'Add New Exchange Trading Pair'}
        onClose={() => setIsModalOpen(false)}
        onSubmit={handleSubmit}
        submitLabel={editingData ? 'Update' : 'Create'}
        loading={loading}
      >
        {!editingData && (
          <>
            <div className="form-group">
              <label className="form-label">Trading Pair *</label>
              <select
                name="trading_pair_uuid"
                className="form-select"
                value={formData.trading_pair_uuid}
                onChange={handleInputChange}
                required
              >
                <option value="">Select a trading pair</option>
                {tradingPairs.map(pair => (
                  <option key={pair.uuid} value={pair.uuid}>
                    {pair.name}
                  </option>
                ))}
              </select>
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
                {exchanges.map(exchange => (
                  <option key={exchange.uuid} value={exchange.uuid}>
                    {exchange.name}
                  </option>
                ))}
              </select>
            </div>
          </>
        )}

        <div className="form-group">
          <label className="form-label">Max Leverage *</label>
          <input
            type="number"
            name="max_leverage"
            className="form-input"
            value={formData.max_leverage}
            onChange={handleInputChange}
            placeholder="e.g., 20"
            min="1"
            required
          />
        </div>
      </Modal>
    </>
  );
};

export default ExchangeTradingPairsTable;
