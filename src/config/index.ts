import { config } from 'dotenv';

config();

const configuration = {
    telegram: {
        botToken: process.env.TELEGRAM_BOT_TOKEN || '',
        chatId: process.env.TELEGRAM_CHAT_ID || '',
    },
    database: {
        host: process.env.DB_HOST || 'localhost',
        port: parseInt(process.env.DB_PORT || '5432', 10),
        user: process.env.DB_USER || 'user',
        password: process.env.DB_PASSWORD || 'password',
        database: process.env.DB_NAME || 'crypto_trading',
    },
    exchanges: {
        mexcApiKey: process.env.MEXC_API_KEY || '',
        mexcApiSecret: process.env.MEXC_API_SECRET || '',
        krakenApiKey: process.env.KRAKEN_API_KEY || '',
        krakenApiSecret: process.env.KRAKEN_API_SECRET || '',
    },
};

export default configuration;