# 🚀 Quick Start Guide - Web Dashboard

## Prerequisites

Ensure you have:
- Python 3.14 ✓
- PostgreSQL running with `crypto_trading_bot` database ✓
- Node.js 16+ (for React frontend)
- All Python dependencies installed

## Installation Steps

### 1️⃣ Install Python Web Dependencies

```bash
python -m pip install Flask Flask-CORS
```

Or install all project dependencies at once:
```bash
python -m pip install -r requirements.txt
```

### 2️⃣ Install React Dependencies

```bash
cd web
npm install
```

## Running the Application

### Option A: Run Both Backend & Frontend (Recommended)

**Terminal 1 - Start Flask Backend:**
```bash
python src/web/app.py
```
Backend will be running at: `http://localhost:5000`

**Terminal 2 - Start React Frontend:**
```bash
cd web
npm start
```
Frontend will open at: `http://localhost:3000`

### Option B: Run Only Backend API

If you only want to interact with the API directly:
```bash
python src/web/app.py
```

API documentation automatically available at any `/api/*` endpoint.

## 📊 Dashboard Tables

Once running, access these tables in the dashboard:

1. **Exchanges** (`/exchanges`)
   - Manage exchange configurations
   - Store API keys securely
   - UUID-based references

2. **Sources** (`/sources`)
   - Telegram group configurations
   - Message templates for trading signals
   - Link to exchanges

3. **Trading Pairs** (`/trading-pairs`)
   - Standardized pair naming
   - UUID identifier generation

4. **Exchange Trading Pairs** (`/exchange-trading-pairs`)
   - Map pairs to specific exchanges
   - Set max leverage per exchange-pair combination
   - Cross-exchange compatibility tracking

5. **Signals** (`/signals`)
   - View all trading signals
   - Entry prices, TP levels (1-4), stop loss
   - Timestamp in Tbilisi timezone

## 🎮 Table Features Demo

### Column Selector
```
1. Click "🔍 Columns" button
2. Uncheck columns you don't want to see
3. Click "Select All" to toggle all at once
```

### Column Filtering
```
1. Look for filter icon in each column header
2. Enter search term or value
3. Table updates in real-time
```

### Resize Columns
```
1. Hover over column border in header
2. Drag left/right to resize
3. Width adjusts smoothly
```

### Reorder Columns
```
1. Click and hold column header
2. Drag left or right
3. Drop to new position
```

### CRUD Operations
```
• ADD: Click "➕ Add" button → Fill form → Click "Create"
• EDIT: Click "✎ Edit" on row → Modify fields → Click "Update"
• DELETE: Click "🗑 Delete" → Confirm → Record removed
• REFRESH: Click "🔄 Refresh" to reload data
```

## 🔌 API Endpoints Quick Reference

### Exchanges
```
GET    /api/exchanges              # List all
POST   /api/exchanges              # Create new
GET    /api/exchanges/<uuid>       # Get one
PUT    /api/exchanges/<uuid>       # Update
DELETE /api/exchanges/<uuid>       # Delete
```

### Sources  
```
GET    /api/sources                # List all
POST   /api/sources                # Create new
PUT    /api/sources/<uuid>         # Update
DELETE /api/sources/<uuid>         # Delete
```

### Trading Pairs
```
GET    /api/trading-pairs          # List all
POST   /api/trading-pairs          # Create new
PUT    /api/trading-pairs/<uuid>   # Update
DELETE /api/trading-pairs/<uuid>   # Delete
```

### Exchange Trading Pairs
```
GET    /api/exchange-trading-pairs        # List all
POST   /api/exchange-trading-pairs        # Create new
PUT    /api/exchange-trading-pairs/<id>   # Update
DELETE /api/exchange-trading-pairs/<id>   # Delete
```

### Signals
```
GET    /api/signals                # List all (supports ?limit=50)
POST   /api/signals                # Create new
PUT    /api/signals/<id>           # Update
DELETE /api/signals/<id>           # Delete
```

## 🧪 Testing the API

### Using cURL
```bash
# Get all exchanges
curl http://localhost:5000/api/exchanges

# Create new exchange
curl -X POST http://localhost:5000/api/exchanges \
  -H "Content-Type: application/json" \
  -d '{"name":"MEXC","api_key":"your-key-here"}'

# Get specific exchange
curl http://localhost:5000/api/exchanges/<uuid>
```

### Using Python
```python
import requests

# Get all exchanges
response = requests.get('http://localhost:5000/api/exchanges')
print(response.json())

# Create exchange
data = {'name': 'Kraken', 'api_key': 'secret-key'}
response = requests.post('http://localhost:5000/api/exchanges', json=data)
print(response.json())
```

## 🐛 Troubleshooting

### Flask won't start
```bash
# Check if port 5000 is in use
lsof -i :5000

# Kill the process if needed
kill -9 <PID>
```

### React won't start
```bash
# Clear node modules and reinstall
cd web
rm -rf node_modules package-lock.json
npm install

# Try starting again
npm start
```

### API connection errors
1. Verify Flask is running: `http://localhost:5000/api/health`
2. Check CORS is enabled (Flask-CORS installed)
3. Verify API_URL in React components matches backend
4. Check PostgreSQL connection in Flask logs

### Database connection errors
1. Ensure PostgreSQL is running
2. Verify credentials in `.env`
3. Check database `crypto_trading_bot` exists
4. Run migrations: `python -m src.database.migrations_signals`

## 📝 Example Workflow

### Adding a Complete Trading Setup

1. **Create Exchange**
   - Go to Exchanges tab
   - Click "➕ Add"
   - Enter: Name=MEXC, API Key=your_key
   - Click "Create"

2. **Create Source (Telegram Group)**
   - Go to Sources tab
   - Click "➕ Add"
   - Select your MEXC exchange
   - Enter Telegram group ID
   - Click "Create"

3. **Create Trading Pairs**
   - Go to Trading Pairs tab
   - Add: BTC/USDT, ETH/USDT, etc.

4. **Map Pairs to Exchange**
   - Go to Exchange Trading Pairs
   - Select BTC/USDT and MEXC
   - Set max leverage (e.g., 20x)
   - Create mapping

5. **Receive Trading Signal**
   - Telegram signal sent to group
   - Bot receives and parses signal
   - Manually add to Signals table
   - Set TP levels (TP1, TP2, TP3, TP4)
   - Set stop loss

## 🌐 Network Access

### Run on Network
To access dashboard from other computers:

**Backend:**
```bash
# Edit Flask host in src/web/app.py
# Change: app.run(host='0.0.0.0')  # Listen on all interfaces
python src/web/app.py
```

**Frontend:**
Create `.env.local` in web folder:
```
REACT_APP_API_URL=http://your-machine-ip:5000/api
```

Then update API_URL in component files.

## 📚 Project Structure

```
crypto-trading-bot/
├── src/
│   ├── web/
│   │   └── app.py              # Flask API server
│   └── database/
│       ├── migrations_signals.py
│       └── queries_signals.py
├── web/                         # React frontend
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   └── components/
│   │       ├── DataTable.js
│   │       ├── Modal.js
│   │       ├── ExchangesTable.js
│   │       ├── SourcesTable.js
│   │       └── ...
│   ├── package.json
│   └── README.md
└── requirements.txt
```

## 🎯 Next Steps

1. ✅ Start Flask backend
2. ✅ Start React frontend
3. ✅ Create exchanges
4. ✅ Create sources
5. ✅ Create trading pairs
6. ✅ Map pairs to exchanges
7. ✅ Add trading signals
8. 🔄 Integrate with Telegram bot (next phase)

## 📞 Support

For issues:
1. Check terminal output for error messages
2. Review browser console (F12)
3. Check .env configuration
4. Verify PostgreSQL connection
5. Check Flask/React port availability

---

**Happy Trading! 📈**
