import logging
from src.database.connection import db

logger = logging.getLogger(__name__)

def add_leverage_and_tp_levels():
    """Add leverage and take-profit levels support to trades table"""
    
    db.connect()
    
    # Add columns to trades table if they don't exist
    add_leverage = """
    ALTER TABLE trades
    ADD COLUMN IF NOT EXISTS leverage INTEGER DEFAULT 1;
    """
    
    add_stop_loss = """
    ALTER TABLE trades
    ADD COLUMN IF NOT EXISTS stop_loss DECIMAL(18, 8);
    """
    
    # Create take_profit_levels table
    create_tp_table = """
    CREATE TABLE IF NOT EXISTS take_profit_levels (
        id SERIAL PRIMARY KEY,
        trade_id INTEGER NOT NULL REFERENCES trades(id) ON DELETE CASCADE,
        price DECIMAL(18, 8) NOT NULL,
        percentage INTEGER NOT NULL,
        status VARCHAR(20) DEFAULT 'PENDING', -- 'PENDING', 'FILLED', 'CLOSED'
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    try:
        with db.get_cursor() as cursor:
            cursor.execute(add_leverage)
            logger.info("Added leverage column to trades table")
            
            cursor.execute(add_stop_loss)
            logger.info("Added stop_loss column to trades table")
            
            cursor.execute(create_tp_table)
            logger.info("Created take_profit_levels table")
        
        logger.info("Database schema extended successfully")
    except Exception as e:
        logger.error(f"Failed to extend database schema: {e}")
        raise
    finally:
        db.disconnect()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    add_leverage_and_tp_levels()
