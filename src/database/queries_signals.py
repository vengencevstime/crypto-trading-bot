import logging
from src.database.connection import db
from typing import List, Dict, Optional
import uuid as uuid_lib

logger = logging.getLogger(__name__)


class ExchangeQueries:
    """Query operations for exchanges table"""
    
    @staticmethod
    def create_exchange(name: str, api_key: str) -> str:
        """Create a new exchange and return its UUID"""
        exchange_uuid = str(uuid_lib.uuid4())
        with db.get_cursor() as cursor:
            cursor.execute("""
                INSERT INTO exchanges (name, api_key, uuid)
                VALUES (%s, %s, %s)
                RETURNING uuid
            """, (name, api_key, exchange_uuid))
            result = cursor.fetchone()
            logger.info(f"Created exchange: {name} with UUID: {exchange_uuid}")
            return exchange_uuid
    
    @staticmethod
    def get_exchange(exchange_uuid: str) -> Optional[Dict]:
        """Get exchange by UUID"""
        with db.get_cursor() as cursor:
            cursor.execute("""
                SELECT id, name, api_key, uuid, created_at, updated_at
                FROM exchanges WHERE uuid = %s
            """, (exchange_uuid,))
            result = cursor.fetchone()
            if result:
                return {
                    'id': result[0],
                    'name': result[1],
                    'api_key': result[2],
                    'uuid': result[3],
                    'created_at': result[4],
                    'updated_at': result[5]
                }
        return None
    
    @staticmethod
    def get_all_exchanges() -> List[Dict]:
        """Get all exchanges"""
        with db.get_cursor() as cursor:
            cursor.execute("""
                SELECT id, name, api_key, uuid, created_at, updated_at
                FROM exchanges ORDER BY name
            """)
            results = cursor.fetchall()
            exchanges = []
            for result in results:
                exchanges.append({
                    'id': result[0],
                    'name': result[1],
                    'api_key': result[2],
                    'uuid': result[3],
                    'created_at': result[4],
                    'updated_at': result[5]
                })
            return exchanges


class SourceQueries:
    """Query operations for sources table"""
    
    @staticmethod
    def create_source(name: str, exchange_uuid: str, telegram_group_id: int,
                     message_sample_short: str = None,
                     message_sample_long: str = None) -> str:
        """Create a new source and return its UUID"""
        source_uuid = str(uuid_lib.uuid4())
        with db.get_cursor() as cursor:
            cursor.execute("""
                INSERT INTO sources (uuid, name, exchange_uuid, telegram_group_id,
                                    message_sample_short, message_sample_long)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING uuid
            """, (source_uuid, name, exchange_uuid, telegram_group_id,
                  message_sample_short, message_sample_long))
            result = cursor.fetchone()
            logger.info(f"Created source: {name} with UUID: {source_uuid}")
            return source_uuid
    
    @staticmethod
    def get_source(source_uuid: str) -> Optional[Dict]:
        """Get source by UUID"""
        with db.get_cursor() as cursor:
            cursor.execute("""
                SELECT id, uuid, name, exchange_uuid, telegram_group_id,
                       message_sample_short, message_sample_long, created_at, updated_at
                FROM sources WHERE uuid = %s
            """, (source_uuid,))
            result = cursor.fetchone()
            if result:
                return {
                    'id': result[0],
                    'uuid': result[1],
                    'name': result[2],
                    'exchange_uuid': result[3],
                    'telegram_group_id': result[4],
                    'message_sample_short': result[5],
                    'message_sample_long': result[6],
                    'created_at': result[7],
                    'updated_at': result[8]
                }
        return None
    
    @staticmethod
    def get_sources_by_exchange(exchange_uuid: str) -> List[Dict]:
        """Get all sources for an exchange"""
        with db.get_cursor() as cursor:
            cursor.execute("""
                SELECT id, uuid, name, exchange_uuid, telegram_group_id,
                       message_sample_short, message_sample_long, created_at, updated_at
                FROM sources WHERE exchange_uuid = %s ORDER BY name
            """, (exchange_uuid,))
            results = cursor.fetchall()
            sources = []
            for result in results:
                sources.append({
                    'id': result[0],
                    'uuid': result[1],
                    'name': result[2],
                    'exchange_uuid': result[3],
                    'telegram_group_id': result[4],
                    'message_sample_short': result[5],
                    'message_sample_long': result[6],
                    'created_at': result[7],
                    'updated_at': result[8]
                })
            return sources


class TradingPairQueries:
    """Query operations for trading_pairs table"""
    
    @staticmethod
    def create_trading_pair(name: str) -> str:
        """Create a new trading pair and return its UUID"""
        pair_uuid = str(uuid_lib.uuid4())
        with db.get_cursor() as cursor:
            cursor.execute("""
                INSERT INTO trading_pairs (name, uuid)
                VALUES (%s, %s)
                RETURNING uuid
            """, (name, pair_uuid))
            result = cursor.fetchone()
            logger.info(f"Created trading pair: {name} with UUID: {pair_uuid}")
            return pair_uuid
    
    @staticmethod
    def get_trading_pair(pair_uuid: str) -> Optional[Dict]:
        """Get trading pair by UUID"""
        with db.get_cursor() as cursor:
            cursor.execute("""
                SELECT id, name, uuid, created_at, updated_at
                FROM trading_pairs WHERE uuid = %s
            """, (pair_uuid,))
            result = cursor.fetchone()
            if result:
                return {
                    'id': result[0],
                    'name': result[1],
                    'uuid': result[2],
                    'created_at': result[3],
                    'updated_at': result[4]
                }
        return None
    
    @staticmethod
    def get_all_trading_pairs() -> List[Dict]:
        """Get all trading pairs"""
        with db.get_cursor() as cursor:
            cursor.execute("""
                SELECT id, name, uuid, created_at, updated_at
                FROM trading_pairs ORDER BY name
            """)
            results = cursor.fetchall()
            pairs = []
            for result in results:
                pairs.append({
                    'id': result[0],
                    'name': result[1],
                    'uuid': result[2],
                    'created_at': result[3],
                    'updated_at': result[4]
                })
            return pairs


class ExchangeTradingPairQueries:
    """Query operations for exchange_trading_pairs table"""
    
    @staticmethod
    def create_exchange_trading_pair(trading_pair_uuid: str, exchange_name: str,
                                    exchange_uuid: str, max_leverage: int = 1) -> int:
        """Create exchange-trading pair mapping and return its ID"""
        with db.get_cursor() as cursor:
            cursor.execute("""
                INSERT INTO exchange_trading_pairs (trading_pair_uuid, exchange_name,
                                                    exchange_uuid, max_leverage)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (trading_pair_uuid, exchange_name, exchange_uuid, max_leverage))
            result = cursor.fetchone()
            pair_id = result[0]
            logger.info(f"Created exchange trading pair mapping with ID: {pair_id}")
            return pair_id
    
    @staticmethod
    def get_pairs_by_exchange(exchange_uuid: str) -> List[Dict]:
        """Get all trading pairs available on an exchange"""
        with db.get_cursor() as cursor:
            cursor.execute("""
                SELECT etp.id, etp.trading_pair_uuid, tp.name, etp.exchange_name,
                       etp.exchange_uuid, etp.max_leverage, etp.created_at, etp.updated_at
                FROM exchange_trading_pairs etp
                JOIN trading_pairs tp ON etp.trading_pair_uuid = tp.uuid
                WHERE etp.exchange_uuid = %s
                ORDER BY tp.name
            """, (exchange_uuid,))
            results = cursor.fetchall()
            pairs = []
            for result in results:
                pairs.append({
                    'id': result[0],
                    'trading_pair_uuid': result[1],
                    'pair_name': result[2],
                    'exchange_name': result[3],
                    'exchange_uuid': result[4],
                    'max_leverage': result[5],
                    'created_at': result[6],
                    'updated_at': result[7]
                })
            return pairs
    
    @staticmethod
    def get_exchanges_for_pair(trading_pair_uuid: str) -> List[Dict]:
        """Get all exchanges that have a trading pair"""
        with db.get_cursor() as cursor:
            cursor.execute("""
                SELECT etp.id, etp.trading_pair_uuid, etp.exchange_name,
                       etp.exchange_uuid, etp.max_leverage, etp.created_at, etp.updated_at
                FROM exchange_trading_pairs etp
                WHERE etp.trading_pair_uuid = %s
                ORDER BY etp.exchange_name
            """, (trading_pair_uuid,))
            results = cursor.fetchall()
            exchanges = []
            for result in results:
                exchanges.append({
                    'id': result[0],
                    'trading_pair_uuid': result[1],
                    'exchange_name': result[2],
                    'exchange_uuid': result[3],
                    'max_leverage': result[4],
                    'created_at': result[5],
                    'updated_at': result[6]
                })
            return exchanges
    
    @staticmethod
    def update_max_leverage(trading_pair_uuid: str, exchange_uuid: str, max_leverage: int):
        """Update max leverage for a pair-exchange combination"""
        with db.get_cursor() as cursor:
            cursor.execute("""
                UPDATE exchange_trading_pairs
                SET max_leverage = %s, updated_at = CURRENT_TIMESTAMP
                WHERE trading_pair_uuid = %s AND exchange_uuid = %s
            """, (max_leverage, trading_pair_uuid, exchange_uuid))
            logger.info(f"Updated max leverage to {max_leverage}x for pair {trading_pair_uuid} on exchange {exchange_uuid}")


class SignalQueries:
    """Query operations for signals table"""
    
    @staticmethod
    def create_signal(creation_time, source_uuid: str, source_entry_price: float = None,
                     current_price: float = None, tp1: float = None, tp2: float = None,
                     tp3: float = None, tp4: float = None, sl: float = None) -> int:
        """Create a new signal and return its ID"""
        with db.get_cursor() as cursor:
            cursor.execute("""
                INSERT INTO signals (creation_time, source_uuid, source_entry_price,
                                    current_price, tp1, tp2, tp3, tp4, sl)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (creation_time, source_uuid, source_entry_price, current_price,
                  tp1, tp2, tp3, tp4, sl))
            result = cursor.fetchone()
            signal_id = result[0]
            logger.info(f"Created signal with ID: {signal_id}")
            return signal_id
    
    @staticmethod
    def get_signal(signal_id: int) -> Optional[Dict]:
        """Get signal by ID"""
        with db.get_cursor() as cursor:
            cursor.execute("""
                SELECT id, creation_time, source_uuid, source_entry_price, current_price,
                       tp1, tp2, tp3, tp4, sl, created_at, updated_at
                FROM signals WHERE id = %s
            """, (signal_id,))
            result = cursor.fetchone()
            if result:
                return {
                    'id': result[0],
                    'creation_time': result[1],
                    'source_uuid': result[2],
                    'source_entry_price': result[3],
                    'current_price': result[4],
                    'tp1': result[5],
                    'tp2': result[6],
                    'tp3': result[7],
                    'tp4': result[8],
                    'sl': result[9],
                    'created_at': result[10],
                    'updated_at': result[11]
                }
        return None
    
    @staticmethod
    def get_signals_by_source(source_uuid: str, limit: int = 100) -> List[Dict]:
        """Get signals from a specific source"""
        with db.get_cursor() as cursor:
            cursor.execute("""
                SELECT id, creation_time, source_uuid, source_entry_price, current_price,
                       tp1, tp2, tp3, tp4, sl, created_at, updated_at
                FROM signals
                WHERE source_uuid = %s
                ORDER BY creation_time DESC
                LIMIT %s
            """, (source_uuid, limit))
            results = cursor.fetchall()
            signals = []
            for result in results:
                signals.append({
                    'id': result[0],
                    'creation_time': result[1],
                    'source_uuid': result[2],
                    'source_entry_price': result[3],
                    'current_price': result[4],
                    'tp1': result[5],
                    'tp2': result[6],
                    'tp3': result[7],
                    'tp4': result[8],
                    'sl': result[9],
                    'created_at': result[10],
                    'updated_at': result[11]
                })
            return signals
    
    @staticmethod
    def update_signal_price(signal_id: int, current_price: float):
        """Update current price for a signal"""
        with db.get_cursor() as cursor:
            cursor.execute("""
                UPDATE signals
                SET current_price = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (current_price, signal_id))
            logger.info(f"Updated signal {signal_id} current price to {current_price}")
    
    @staticmethod
    def get_recent_signals(limit: int = 50) -> List[Dict]:
        """Get most recent signals"""
        with db.get_cursor() as cursor:
            cursor.execute("""
                SELECT id, creation_time, source_uuid, source_entry_price, current_price,
                       tp1, tp2, tp3, tp4, sl, created_at, updated_at
                FROM signals
                ORDER BY creation_time DESC
                LIMIT %s
            """, (limit,))
            results = cursor.fetchall()
            signals = []
            for result in results:
                signals.append({
                    'id': result[0],
                    'creation_time': result[1],
                    'source_uuid': result[2],
                    'source_entry_price': result[3],
                    'current_price': result[4],
                    'tp1': result[5],
                    'tp2': result[6],
                    'tp3': result[7],
                    'tp4': result[8],
                    'sl': result[9],
                    'created_at': result[10],
                    'updated_at': result[11]
                })
            return signals
