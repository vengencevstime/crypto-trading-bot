import { Pool } from 'pg';
import { TradeData } from '../types';

const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
});

export const insertTradeData = async (tradeData: TradeData) => {
    const query = `
        INSERT INTO trades (symbol, price, quantity, side, timestamp)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING id;
    `;
    const values = [tradeData.symbol, tradeData.price, tradeData.quantity, tradeData.side, tradeData.timestamp];
    
    const result = await pool.query(query, values);
    return result.rows[0].id;
};

export const getTradeData = async (symbol: string) => {
    const query = `
        SELECT * FROM trades
        WHERE symbol = $1
        ORDER BY timestamp DESC;
    `;
    const values = [symbol];
    
    const result = await pool.query(query, values);
    return result.rows;
};

export const closeConnection = async () => {
    await pool.end();
};