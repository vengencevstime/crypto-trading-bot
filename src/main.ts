import { connectToDatabase } from './database/connection';
import { TelegramClient } from './telegram/client';
import { startMessageHandling } from './telegram/handlers';
import { config } from './config';

async function main() {
    try {
        // Initialize database connection
        await connectToDatabase();

        // Initialize Telegram client
        const telegramClient = new TelegramClient(config.telegramToken);

        // Start handling messages
        startMessageHandling(telegramClient);
    } catch (error) {
        console.error('Error starting the application:', error);
    }
}

main();