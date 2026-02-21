import logging
from src.database.connection import db

logger = logging.getLogger(__name__)


def create_exchanges():
    """Create exchanges table to track multiple exchanges and their API credentials"""
    with db.get_cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exchanges (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL,
                api_key VARCHAR(500) NOT NULL,
                uuid VARCHAR(36) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX IF NOT EXISTS idx_exchanges_uuid ON exchanges(uuid);
            CREATE INDEX IF NOT EXISTS idx_exchanges_name ON exchanges(name);
        """)
    logger.info("Created 'exchanges' table")


def create_sources():
    """Create sources table to track Telegram groups and their signal sources"""
    with db.get_cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sources (
                id SERIAL PRIMARY KEY,
                uuid VARCHAR(36) UNIQUE NOT NULL,
                name VARCHAR(255) NOT NULL,
                exchange_uuid VARCHAR(36) NOT NULL,
                telegram_group_id BIGINT NOT NULL,
                message_sample_short TEXT,
                message_sample_long TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (exchange_uuid) REFERENCES exchanges(uuid) ON DELETE CASCADE
            );
            CREATE INDEX IF NOT EXISTS idx_sources_exchange_uuid ON sources(exchange_uuid);
            CREATE INDEX IF NOT EXISTS idx_sources_telegram_group_id ON sources(telegram_group_id);
            CREATE INDEX IF NOT EXISTS idx_sources_uuid ON sources(uuid);
        """)
    logger.info("Created 'sources' table")


def create_trading_pairs():
    """Create trading_pairs table to track unique trading pairs"""
    with db.get_cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trading_pairs (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL,
                uuid VARCHAR(36) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX IF NOT EXISTS idx_trading_pairs_uuid ON trading_pairs(uuid);
            CREATE INDEX IF NOT EXISTS idx_trading_pairs_name ON trading_pairs(name);
        """)
    logger.info("Created 'trading_pairs' table")


def create_exchange_trading_pairs():
    """Create exchange_trading_pairs table to map trading pairs to exchanges with their max leverage"""
    with db.get_cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exchange_trading_pairs (
                id SERIAL PRIMARY KEY,
                trading_pair_uuid VARCHAR(36) NOT NULL,
                exchange_name VARCHAR(100) NOT NULL,
                exchange_uuid VARCHAR(36) NOT NULL,
                max_leverage INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (trading_pair_uuid) REFERENCES trading_pairs(uuid) ON DELETE CASCADE,
                FOREIGN KEY (exchange_uuid) REFERENCES exchanges(uuid) ON DELETE CASCADE,
                UNIQUE(trading_pair_uuid, exchange_uuid)
            );
            CREATE INDEX IF NOT EXISTS idx_exchange_trading_pairs_trading_pair ON exchange_trading_pairs(trading_pair_uuid);
            CREATE INDEX IF NOT EXISTS idx_exchange_trading_pairs_exchange ON exchange_trading_pairs(exchange_uuid);
        """)
    logger.info("Created 'exchange_trading_pairs' table")


def create_signals():
    """Create signals table to track trading signals from sources"""
    with db.get_cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS signals (
                id SERIAL PRIMARY KEY,
                creation_time TIMESTAMP NOT NULL,
                source_uuid VARCHAR(36) NOT NULL,
                source_entry_price DECIMAL(18, 8),
                current_price DECIMAL(18, 8),
                tp1 DECIMAL(18, 8),
                tp2 DECIMAL(18, 8),
                tp3 DECIMAL(18, 8),
                tp4 DECIMAL(18, 8),
                sl DECIMAL(18, 8),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (source_uuid) REFERENCES sources(uuid) ON DELETE CASCADE
            );
            CREATE INDEX IF NOT EXISTS idx_signals_creation_time ON signals(creation_time);
            CREATE INDEX IF NOT EXISTS idx_signals_source_uuid ON signals(source_uuid);
        """)
    logger.info("Created 'signals' table")


def migrate_signals():
    """Run all signal-related migrations"""
    try:
        create_exchanges()
        create_sources()
        create_trading_pairs()
        create_exchange_trading_pairs()
        create_signals()
        logger.info("All signal tables created successfully")
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    db.connect()
    try:
        migrate_signals()
    finally:
        db.disconnect()
