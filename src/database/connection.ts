import { Client } from 'pg';
import { config } from '../config/index';

export const connectToDatabase = async () => {
    const client = new Client({
        user: config.DB_USER,
        host: config.DB_HOST,
        database: config.DB_NAME,
        password: config.DB_PASSWORD,
        port: config.DB_PORT,
    });

    await client.connect();
    return client;
};