# Crypto Trading Bot - Management Dashboard

A modern web application for managing crypto trading bot databases with advanced table features.

## Features

✨ **Advanced Table Management**
- 📊 Data tables for all 5 databases (Exchanges, Sources, Trading Pairs, Exchange Trading Pairs, Signals)
- ✅ Full CRUD operations (Create, Read, Update, Delete)
- 🔍 **Column Selector** - Select/deselect columns to display
- 🔎 **Column Filters** - Filter data by any column value
- 📐 **Resizable Columns** - Drag column borders to resize
- 🎨 **Drag-Drop Reordering** - Rearrange columns by dragging headers
- 📱 Responsive design for all screen sizes
- ⚡ Real-time data loading with error handling

## Tech Stack

### Backend
- **Python 3.14** with Flask
- **PostgreSQL** database
- **Flask-CORS** for cross-origin requests
- RESTful API architecture

### Frontend
- **React 18** - Modern UI framework
- **AG Grid Community** - Advanced data table component
- **React Router** - Navigation between tables
- **Axios** - HTTP client for API calls
- **CSS3** - Beautiful styling with gradients and animations

## Installation

### Backend Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure PostgreSQL is running with the `crypto_trading_bot` database created.

3. Run database migrations:
```bash
python -m src.database.migrations
python -m src.database.migrations_signals
```

4. Start the Flask server:
```bash
python src/web/app.py
```

The API will be available at `http://localhost:5000`

### Frontend Setup

1. Navigate to the web directory:
```bash
cd web
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will open at `http://localhost:3000`

## Usage

### Navigating the Dashboard

The dashboard has 5 main sections accessible from the navigation bar:

1. **Exchanges** - Manage exchange configurations and API keys
2. **Sources** - Manage Telegram groups and signal sources
3. **Trading Pairs** - Manage available trading pairs
4. **Exchange Pairs** - Map trading pairs to exchanges with leverage settings
5. **Signals** - View and manage trading signals with TP/SL levels

### Working with Tables

#### Column Management
- Click the **"🔍 Columns"** button to open the column selector
- Check/uncheck columns to show/hide them
- Click **"Select All"** to toggle all columns at once

#### Filtering Data
- Each column header shows a filter icon
- Click to enter filter values
- Supports text matching and numeric comparisons

#### Resizing Columns
- Hover over the column border in the header
- Drag left/right to resize
- Sizes are preserved during the session

#### Reordering Columns
- Drag column headers left/right to change order
- Columns stay ordered as you rearrange them

### Managing Data

#### Adding Records
- Click the **"➕ Add"** button
- Fill in the form fields
- Foreign key fields (like Exchange, Source) show dropdown lists with names
- Click "Create" to save

#### Editing Records
- Click the **"✎ Edit"** button on any row
- Modify the fields
- Click "Update" to save changes

#### Deleting Records
- Click the **"🗑 Delete"** button on any row
- Confirm deletion in the dialog
- Record is removed from the database

#### Refreshing Data
- Click the **"🔄 Refresh"** button to reload latest data from server

## API Endpoints

### Exchanges
- `GET /api/exchanges` - List all exchanges
- `POST /api/exchanges` - Create exchange
- `GET /api/exchanges/<uuid>` - Get exchange
- `PUT /api/exchanges/<uuid>` - Update exchange
- `DELETE /api/exchanges/<uuid>` - Delete exchange

### Sources
- `GET /api/sources` - List all sources
- `POST /api/sources` - Create source
- `PUT /api/sources/<uuid>` - Update source
- `DELETE /api/sources/<uuid>` - Delete source

### Trading Pairs
- `GET /api/trading-pairs` - List all pairs
- `POST /api/trading-pairs` - Create pair
- `PUT /api/trading-pairs/<uuid>` - Update pair
- `DELETE /api/trading-pairs/<uuid>` - Delete pair

### Exchange Trading Pairs
- `GET /api/exchange-trading-pairs` - List all mappings
- `POST /api/exchange-trading-pairs` - Create mapping
- `PUT /api/exchange-trading-pairs/<id>` - Update mapping
- `DELETE /api/exchange-trading-pairs/<id>` - Delete mapping

### Signals
- `GET /api/signals` - List signals (with limit parameter)
- `POST /api/signals` - Create signal
- `PUT /api/signals/<id>` - Update signal
- `DELETE /api/signals/<id>` - Delete signal

## Database Schema

### exchanges
- id, name, api_key, uuid, created_at, updated_at

### sources
- id, uuid, name, exchange_uuid, telegram_group_id, message_sample_short, message_sample_long, created_at, updated_at

### trading_pairs
- id, name, uuid, created_at, updated_at

### exchange_trading_pairs
- id, trading_pair_uuid, exchange_uuid, exchange_name, max_leverage, created_at, updated_at

### signals
- id, creation_time, source_uuid, source_entry_price, current_price, tp1, tp2, tp3, tp4, sl, created_at, updated_at

## Configuration

### Backend (.env)
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=crypto_trading_bot
DB_USER=postgres
DB_PASSWORD=your_password
```

### Frontend API URL
Edit `web/src/components/*Table.js` to change the `API_URL` if your backend is on a different server:
```javascript
const API_URL = 'http://your-server:5000/api';
```

## Features in Detail

### Column Selector Button
- 🔍 Icon indicates column management
- Dropdown menu shows all available columns
- "Select All" checkbox to toggle all columns
- Real-time filtering of table display

### Column Filters
- Integrated floating filters on each column
- Text input for string columns
- Numeric comparisons for number columns
- Multiple column filtering supported

### Resizable Columns
- Smooth drag-to-resize functionality
- Maintains column proportions
- Works with all column types

### Drag-Drop Reordering
- Drag column headers to rearrange
- Visual feedback during dragging
- Order persists in current session

### Foreign Key Resolution
- Exchange UUID → Exchange Name in sources
- Trading Pair UUID → Pair Name in exchange_trading_pairs
- Source UUID → Source Name in signals
- Dropdowns automatically populated from related tables

## Error Handling

- API errors are displayed in red error messages
- Success messages confirm CRUD operations
- Loading states prevent double-submission
- Network errors are gracefully handled

## Performance

- Pagination: 20 rows per page by default
- Lazy loading of dropdown data
- Optimized re-renders with React
- Efficient database queries

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Modern browsers with ES6 support

## Development

### Building for Production

Frontend:
```bash
cd web
npm run build
```

This creates an optimized production build in `web/build/`

## Troubleshooting

### Backend Connection Issues
- Verify Flask is running on port 5000
- Check CORS is enabled (Flask-CORS installed)
- Ensure PostgreSQL is running
- Check database credentials in .env

### Frontend Not Loading Data
- Open browser DevTools (F12)
- Check Console for API errors
- Verify API_URL is correct in component files
- Check Network tab to see API requests

### Port Already in Use
```bash
# Kill process on port 5000 (Flask)
lsof -ti:5000 | xargs kill -9

# Kill process on port 3000 (React)
lsof -ti:3000 | xargs kill -9
```

## License

Part of the Crypto Trading Bot Project
