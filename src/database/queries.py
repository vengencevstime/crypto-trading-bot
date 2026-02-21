import logging
from datetime import datetime
from src.database.connection import db

logger = logging.getLogger(__name__)

class TradeQueries:
    """Database queries for trades"""
    
    @staticmethod
    def create_trade(symbol, entry_price, quantity, position_type, exchange, exchange_order_id=None):
        """Create a new trade record"""
        query = """
        INSERT INTO trades (symbol, entry_price, quantity, position_type, exchange, exchange_order_id, status)
        VALUES (%s, %s, %s, %s, %s, %s, 'OPEN')
        RETURNING id;
        """
        result = db.execute_update(query, (symbol, entry_price, quantity, position_type, exchange, exchange_order_id))
        return result
    
    @staticmethod
    def get_trade(trade_id):
        """Get trade by ID"""
        query = "SELECT * FROM trades WHERE id = %s;"
        result = db.execute_query(query, (trade_id,))
        return result[0] if result else None
    
    @staticmethod
    def get_open_trades(exchange=None):
        """Get all open trades, optionally filtered by exchange"""
        if exchange:
            query = "SELECT * FROM trades WHERE status = 'OPEN' AND exchange = %s;"
            result = db.execute_query(query, (exchange,))
        else:
            query = "SELECT * FROM trades WHERE status = 'OPEN';"
            result = db.execute_query(query)
        return result
    
    @staticmethod
    def close_trade(trade_id, exit_price):
        """Close a trade with exit price"""
        query = """
        UPDATE trades 
        SET status = 'CLOSED', exit_price = %s, exit_time = CURRENT_TIMESTAMP,
            profit_loss = (quantity * exit_price) - (quantity * entry_price),
            updated_at = CURRENT_TIMESTAMP
        WHERE id = %s;
        """
        return db.execute_update(query, (exit_price, trade_id))

class MessageQueries:
    """Database queries for Telegram messages"""
    
    @staticmethod
    def save_message(message_text, message_date, sender_id, sender_name, group_id):
        """Save a Telegram message"""
        query = """
        INSERT INTO telegram_messages (message_text, message_date, sender_id, sender_name, group_id)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
        """
        result = db.execute_update(query, (message_text, message_date, sender_id, sender_name, group_id))
        return result
    
    @staticmethod
    def mark_message_parsed(message_id, trade_id=None):
        """Mark a message as parsed"""
        query = """
        UPDATE telegram_messages
        SET parsed = TRUE, trade_id = %s, created_at = CURRENT_TIMESTAMP
        WHERE id = %s;
        """
        return db.execute_update(query, (trade_id, message_id))
    
    @staticmethod
    def get_unparsed_messages():
        """Get all unparsed messages"""
        query = "SELECT * FROM telegram_messages WHERE parsed = FALSE ORDER BY created_at ASC;"
        return db.execute_query(query)

class PositionQueries:
    """Database queries for positions"""
    
    @staticmethod
    def create_position(trade_id, exchange, exchange_position_id, current_price):
        """Create a position record"""
        query = """
        INSERT INTO positions (trade_id, exchange, exchange_position_id, current_price, monitoring)
        VALUES (%s, %s, %s, %s, TRUE)
        RETURNING id;
        """
        result = db.execute_update(query, (trade_id, exchange, exchange_position_id, current_price))
        return result
    
    @staticmethod
    def get_monitoring_positions():
        """Get all positions being monitored"""
        query = "SELECT * FROM positions WHERE monitoring = TRUE;"
        return db.execute_query(query)
    
    @staticmethod
    def update_position_price(position_id, current_price, profit_loss):
        """Update position current price and P&L"""
        query = """
        UPDATE positions
        SET current_price = %s, current_profit_loss = %s, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s;
        """
        return db.execute_update(query, (current_price, profit_loss, position_id))
    
    @staticmethod
    def close_position(position_id):
        """Close a position"""
        query = """
        UPDATE positions
        SET monitoring = FALSE, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s;
        """
        return db.execute_update(query, (position_id,))

class ExchangeEventQueries:
    """Database queries for exchange events"""
    
    @staticmethod
    def log_event(trade_id, event_type, event_data, exchange):
        """Log an exchange event"""
        query = """
        INSERT INTO exchange_events (trade_id, event_type, event_data, exchange)
        VALUES (%s, %s, %s, %s);
        """
        return db.execute_update(query, (trade_id, event_type, event_data, exchange))
