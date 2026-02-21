import { Client } from 'pg';

const client = new Client({
    user: process.env.DB_USER,
    host: process.env.DB_HOST,
    database: process.env.DB_NAME,
    password: process.env.DB_PASSWORD,
    port: Number(process.env.DB_PORT),
});

async function createTables() {
    const createMessagesTable = `
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    `;

    const createTradesTable = `
        CREATE TABLE IF NOT EXISTS trades (
            id SERIAL PRIMARY KEY,
            position_id VARCHAR(255) NOT NULL,
            status VARCHAR(50) NOT NULL,
            entry_price NUMERIC NOT NULL,
            exit_price NUMERIC,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    `;

    await client.query(createMessagesTable);
    await client.query(createTradesTable);
}

export async function runMigrations() {
    await client.connect();
    await createTables();
    await client.end();
}