import logging
from src.database.connection import db

logger = logging.getLogger(__name__)

def create_tables():
    """Create all necessary tables for the trading bot"""
    
    db.connect()
    
    create_trades_table = """
    CREATE TABLE IF NOT EXISTS trades (
        id SERIAL PRIMARY KEY,
        symbol VARCHAR(20) NOT NULL,
        entry_price DECIMAL(18, 8) NOT NULL,
        quantity DECIMAL(18, 8) NOT NULL,
        position_type VARCHAR(10) NOT NULL, -- 'LONG' or 'SHORT'
        entry_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        exit_price DECIMAL(18, 8),
        exit_time TIMESTAMP,
        status VARCHAR(20) DEFAULT 'OPEN', -- 'OPEN', 'CLOSED', 'CANCELLED'
        exchange VARCHAR(20) NOT NULL, -- 'MEXC', 'KRAKEN'
        exchange_order_id VARCHAR(100),
        profit_loss DECIMAL(18, 8),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    create_messages_table = """
    CREATE TABLE IF NOT EXISTS telegram_messages (
        id SERIAL PRIMARY KEY,
        message_text TEXT NOT NULL,
        message_date TIMESTAMP,
        sender_id BIGINT,
        sender_name VARCHAR(255),
        group_id BIGINT NOT NULL,
        parsed BOOLEAN DEFAULT FALSE,
        trade_id INTEGER REFERENCES trades(id),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    create_positions_table = """
    CREATE TABLE IF NOT EXISTS positions (
        id SERIAL PRIMARY KEY,
        trade_id INTEGER NOT NULL REFERENCES trades(id),
        exchange VARCHAR(20) NOT NULL,
        exchange_position_id VARCHAR(100),
        current_price DECIMAL(18, 8),
        current_profit_loss DECIMAL(18, 8),
        monitoring BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    create_exchange_events_table = """
    CREATE TABLE IF NOT EXISTS exchange_events (
        id SERIAL PRIMARY KEY,
        trade_id INTEGER REFERENCES trades(id),
        event_type VARCHAR(50) NOT NULL, -- 'POSITION_OPENED', 'POSITION_CLOSED', 'ERROR'
        event_data JSON,
        exchange VARCHAR(20) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    try:
        with db.get_cursor() as cursor:
            cursor.execute(create_trades_table)
            logger.info("Created 'trades' table")
            
            cursor.execute(create_messages_table)
            logger.info("Created 'telegram_messages' table")
            
            cursor.execute(create_positions_table)
            logger.info("Created 'positions' table")
            
            cursor.execute(create_exchange_events_table)
            logger.info("Created 'exchange_events' table")
        
        logger.info("All tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create tables: {e}")
        raise
    finally:
        db.disconnect()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    create_tables()
