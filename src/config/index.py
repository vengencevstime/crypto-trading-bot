import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    # Database
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', 5432)
    DB_NAME = os.getenv('DB_NAME', 'crypto_trading_bot')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    
    # Database URL for SQLAlchemy
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    # Telegram
    TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID')
    TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')
    TELEGRAM_PHONE = os.getenv('TELEGRAM_PHONE')
    TELEGRAM_GROUP_ID = os.getenv('TELEGRAM_GROUP_ID')
    
    # MEXC Exchange
    MEXC_API_KEY = os.getenv('MEXC_API_KEY')
    MEXC_API_SECRET = os.getenv('MEXC_API_SECRET')
    
    # Kraken Exchange
    KRAKEN_API_KEY = os.getenv('KRAKEN_API_KEY')
    KRAKEN_API_SECRET = os.getenv('KRAKEN_API_SECRET')
    
    # Application
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
