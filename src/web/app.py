from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from src.database.connection import db
from src.database.queries_signals import (
    ExchangeQueries, SourceQueries, TradingPairQueries,
    ExchangeTradingPairQueries, SignalQueries
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize database connection
db.connect()

# ==================== EXCHANGES ====================

@app.route('/api/exchanges', methods=['GET'])
def get_exchanges():
    """Get all exchanges"""
    try:
        exchanges = ExchangeQueries.get_all_exchanges()
        return jsonify(exchanges)
    except Exception as e:
        logger.error(f"Error getting exchanges: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/exchanges', methods=['POST'])
def create_exchange():
    """Create a new exchange"""
    try:
        data = request.json
        name = data.get('name')
        api_key = data.get('api_key')
        
        if not name or not api_key:
            return jsonify({'error': 'Missing required fields'}), 400
        
        uuid = ExchangeQueries.create_exchange(name, api_key)
        return jsonify({'uuid': uuid, 'name': name, 'api_key': api_key}), 201
    except Exception as e:
        logger.error(f"Error creating exchange: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/exchanges/<exchange_uuid>', methods=['GET'])
def get_exchange(exchange_uuid):
    """Get exchange by UUID"""
    try:
        exchange = ExchangeQueries.get_exchange(exchange_uuid)
        if not exchange:
            return jsonify({'error': 'Exchange not found'}), 404
        return jsonify(exchange)
    except Exception as e:
        logger.error(f"Error getting exchange: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/exchanges/<exchange_uuid>', methods=['PUT'])
def update_exchange(exchange_uuid):
    """Update exchange"""
    try:
        data = request.json
        with db.get_cursor() as cursor:
            updates = []
            values = []
            for key in ['name', 'api_key']:
                if key in data:
                    updates.append(f"{key} = %s")
                    values.append(data[key])
            
            if not updates:
                return jsonify({'error': 'No fields to update'}), 400
            
            values.append(exchange_uuid)
            query = f"UPDATE exchanges SET {', '.join(updates)}, updated_at = CURRENT_TIMESTAMP WHERE uuid = %s"
            cursor.execute(query, values)
        
        return jsonify({'message': 'Exchange updated'}), 200
    except Exception as e:
        logger.error(f"Error updating exchange: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/exchanges/<exchange_uuid>', methods=['DELETE'])
def delete_exchange(exchange_uuid):
    """Delete exchange"""
    try:
        with db.get_cursor() as cursor:
            cursor.execute("DELETE FROM exchanges WHERE uuid = %s", (exchange_uuid,))
        return jsonify({'message': 'Exchange deleted'}), 200
    except Exception as e:
        logger.error(f"Error deleting exchange: {e}")
        return jsonify({'error': str(e)}), 500


# ==================== SOURCES ====================

@app.route('/api/sources', methods=['GET'])
def get_sources():
    """Get all sources"""
    try:
        with db.get_cursor() as cursor:
            cursor.execute("""
                SELECT s.id, s.uuid, s.name, s.exchange_uuid, e.name as exchange_name,
                       s.telegram_group_id, s.message_sample_short, s.message_sample_long,
                       s.created_at, s.updated_at
                FROM sources s
                LEFT JOIN exchanges e ON s.exchange_uuid = e.uuid
                ORDER BY s.name
            """)
            results = cursor.fetchall()
            sources = []
            for result in results:
                sources.append({
                    'id': result[0],
                    'uuid': result[1],
                    'name': result[2],
                    'exchange_uuid': result[3],
                    'exchange_name': result[4],
                    'telegram_group_id': result[5],
                    'message_sample_short': result[6],
                    'message_sample_long': result[7],
                    'created_at': result[8],
                    'updated_at': result[9]
                })
            return jsonify(sources)
    except Exception as e:
        logger.error(f"Error getting sources: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/sources', methods=['POST'])
def create_source():
    """Create a new source"""
    try:
        data = request.json
        name = data.get('name')
        exchange_uuid = data.get('exchange_uuid')
        telegram_group_id = data.get('telegram_group_id')
        
        if not all([name, exchange_uuid, telegram_group_id]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        uuid = SourceQueries.create_source(
            name, exchange_uuid, telegram_group_id,
            data.get('message_sample_short'),
            data.get('message_sample_long')
        )
        return jsonify({'uuid': uuid}), 201
    except Exception as e:
        logger.error(f"Error creating source: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/sources/<source_uuid>', methods=['PUT'])
def update_source(source_uuid):
    """Update source"""
    try:
        data = request.json
        with db.get_cursor() as cursor:
            updates = []
            values = []
            for key in ['name', 'exchange_uuid', 'telegram_group_id', 'message_sample_short', 'message_sample_long']:
                if key in data:
                    updates.append(f"{key} = %s")
                    values.append(data[key])
            
            if not updates:
                return jsonify({'error': 'No fields to update'}), 400
            
            values.append(source_uuid)
            query = f"UPDATE sources SET {', '.join(updates)}, updated_at = CURRENT_TIMESTAMP WHERE uuid = %s"
            cursor.execute(query, values)
        
        return jsonify({'message': 'Source updated'}), 200
    except Exception as e:
        logger.error(f"Error updating source: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/sources/<source_uuid>', methods=['DELETE'])
def delete_source(source_uuid):
    """Delete source"""
    try:
        with db.get_cursor() as cursor:
            cursor.execute("DELETE FROM sources WHERE uuid = %s", (source_uuid,))
        return jsonify({'message': 'Source deleted'}), 200
    except Exception as e:
        logger.error(f"Error deleting source: {e}")
        return jsonify({'error': str(e)}), 500


# ==================== TRADING PAIRS ====================

@app.route('/api/trading-pairs', methods=['GET'])
def get_trading_pairs():
    """Get all trading pairs"""
    try:
        pairs = TradingPairQueries.get_all_trading_pairs()
        return jsonify(pairs)
    except Exception as e:
        logger.error(f"Error getting trading pairs: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/trading-pairs', methods=['POST'])
def create_trading_pair():
    """Create a new trading pair"""
    try:
        data = request.json
        name = data.get('name')
        
        if not name:
            return jsonify({'error': 'Missing required field: name'}), 400
        
        uuid = TradingPairQueries.create_trading_pair(name)
        return jsonify({'uuid': uuid, 'name': name}), 201
    except Exception as e:
        logger.error(f"Error creating trading pair: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/trading-pairs/<pair_uuid>', methods=['PUT'])
def update_trading_pair(pair_uuid):
    """Update trading pair"""
    try:
        data = request.json
        with db.get_cursor() as cursor:
            cursor.execute("""
                UPDATE trading_pairs SET name = %s, updated_at = CURRENT_TIMESTAMP WHERE uuid = %s
            """, (data.get('name'), pair_uuid))
        
        return jsonify({'message': 'Trading pair updated'}), 200
    except Exception as e:
        logger.error(f"Error updating trading pair: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/trading-pairs/<pair_uuid>', methods=['DELETE'])
def delete_trading_pair(pair_uuid):
    """Delete trading pair"""
    try:
        with db.get_cursor() as cursor:
            cursor.execute("DELETE FROM trading_pairs WHERE uuid = %s", (pair_uuid,))
        return jsonify({'message': 'Trading pair deleted'}), 200
    except Exception as e:
        logger.error(f"Error deleting trading pair: {e}")
        return jsonify({'error': str(e)}), 500


# ==================== EXCHANGE TRADING PAIRS ====================

@app.route('/api/exchange-trading-pairs', methods=['GET'])
def get_exchange_trading_pairs():
    """Get all exchange-trading pair mappings"""
    try:
        with db.get_cursor() as cursor:
            cursor.execute("""
                SELECT etp.id, etp.trading_pair_uuid, tp.name as trading_pair_name,
                       etp.exchange_uuid, e.name as exchange_name, etp.max_leverage,
                       etp.created_at, etp.updated_at
                FROM exchange_trading_pairs etp
                LEFT JOIN trading_pairs tp ON etp.trading_pair_uuid = tp.uuid
                LEFT JOIN exchanges e ON etp.exchange_uuid = e.uuid
                ORDER BY tp.name, e.name
            """)
            results = cursor.fetchall()
            pairs = []
            for result in results:
                pairs.append({
                    'id': result[0],
                    'trading_pair_uuid': result[1],
                    'trading_pair_name': result[2],
                    'exchange_uuid': result[3],
                    'exchange_name': result[4],
                    'max_leverage': result[5],
                    'created_at': result[6],
                    'updated_at': result[7]
                })
            return jsonify(pairs)
    except Exception as e:
        logger.error(f"Error getting exchange trading pairs: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/exchange-trading-pairs', methods=['POST'])
def create_exchange_trading_pair():
    """Create exchange-trading pair mapping"""
    try:
        data = request.json
        pair_id = ExchangeTradingPairQueries.create_exchange_trading_pair(
            data.get('trading_pair_uuid'),
            data.get('exchange_name'),
            data.get('exchange_uuid'),
            data.get('max_leverage', 1)
        )
        return jsonify({'id': pair_id}), 201
    except Exception as e:
        logger.error(f"Error creating exchange trading pair: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/exchange-trading-pairs/<int:pair_id>', methods=['PUT'])
def update_exchange_trading_pair(pair_id):
    """Update exchange-trading pair"""
    try:
        data = request.json
        with db.get_cursor() as cursor:
            cursor.execute("""
                UPDATE exchange_trading_pairs SET max_leverage = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s
            """, (data.get('max_leverage'), pair_id))
        
        return jsonify({'message': 'Exchange trading pair updated'}), 200
    except Exception as e:
        logger.error(f"Error updating exchange trading pair: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/exchange-trading-pairs/<int:pair_id>', methods=['DELETE'])
def delete_exchange_trading_pair(pair_id):
    """Delete exchange-trading pair"""
    try:
        with db.get_cursor() as cursor:
            cursor.execute("DELETE FROM exchange_trading_pairs WHERE id = %s", (pair_id,))
        return jsonify({'message': 'Exchange trading pair deleted'}), 200
    except Exception as e:
        logger.error(f"Error deleting exchange trading pair: {e}")
        return jsonify({'error': str(e)}), 500


# ==================== SIGNALS ====================

@app.route('/api/signals', methods=['GET'])
def get_signals():
    """Get all signals"""
    try:
        limit = request.args.get('limit', 100, type=int)
        signals = SignalQueries.get_recent_signals(limit)
        return jsonify(signals)
    except Exception as e:
        logger.error(f"Error getting signals: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/signals', methods=['POST'])
def create_signal():
    """Create a new signal"""
    try:
        data = request.json
        signal_id = SignalQueries.create_signal(
            data.get('creation_time'),
            data.get('source_uuid'),
            data.get('source_entry_price'),
            data.get('current_price'),
            data.get('tp1'),
            data.get('tp2'),
            data.get('tp3'),
            data.get('tp4'),
            data.get('sl')
        )
        return jsonify({'id': signal_id}), 201
    except Exception as e:
        logger.error(f"Error creating signal: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/signals/<int:signal_id>', methods=['PUT'])
def update_signal(signal_id):
    """Update signal"""
    try:
        data = request.json
        with db.get_cursor() as cursor:
            updates = []
            values = []
            for key in ['creation_time', 'source_uuid', 'source_entry_price', 'current_price',
                       'tp1', 'tp2', 'tp3', 'tp4', 'sl']:
                if key in data:
                    updates.append(f"{key} = %s")
                    values.append(data[key])
            
            if not updates:
                return jsonify({'error': 'No fields to update'}), 400
            
            values.append(signal_id)
            query = f"UPDATE signals SET {', '.join(updates)}, updated_at = CURRENT_TIMESTAMP WHERE id = %s"
            cursor.execute(query, values)
        
        return jsonify({'message': 'Signal updated'}), 200
    except Exception as e:
        logger.error(f"Error updating signal: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/signals/<int:signal_id>', methods=['DELETE'])
def delete_signal(signal_id):
    """Delete signal"""
    try:
        with db.get_cursor() as cursor:
            cursor.execute("DELETE FROM signals WHERE id = %s", (signal_id,))
        return jsonify({'message': 'Signal deleted'}), 200
    except Exception as e:
        logger.error(f"Error deleting signal: {e}")
        return jsonify({'error': str(e)}), 500


# ==================== UTILITY ENDPOINTS ====================

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'}), 200


if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    finally:
        db.disconnect()
