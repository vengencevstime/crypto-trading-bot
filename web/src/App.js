import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import ExchangesTable from './components/ExchangesTable';
import SourcesTable from './components/SourcesTable';
import TradingPairsTable from './components/TradingPairsTable';
import ExchangeTradingPairsTable from './components/ExchangeTradingPairsTable';
import SignalsTable from './components/SignalsTable';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app">
        <nav className="navbar">
          <div className="nav-container">
            <h1 className="nav-title">📊 Crypto Trading Bot - Management</h1>
            <ul className="nav-links">
              <li><Link to="/exchanges">Exchanges</Link></li>
              <li><Link to="/sources">Sources</Link></li>
              <li><Link to="/trading-pairs">Trading Pairs</Link></li>
              <li><Link to="/exchange-trading-pairs">Exchange Pairs</Link></li>
              <li><Link to="/signals">Signals</Link></li>
            </ul>
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/exchanges" element={<ExchangesTable />} />
            <Route path="/sources" element={<SourcesTable />} />
            <Route path="/trading-pairs" element={<TradingPairsTable />} />
            <Route path="/exchange-trading-pairs" element={<ExchangeTradingPairsTable />} />
            <Route path="/signals" element={<SignalsTable />} />
            <Route path="/" element={<ExchangesTable />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
