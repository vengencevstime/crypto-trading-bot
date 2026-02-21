import { Telegraf } from 'telegraf';
import { handleIncomingMessage } from './handlers';
import { config } from '../config';

export class TelegramClient {
    private bot: Telegraf;

    constructor() {
        this.bot = new Telegraf(config.TELEGRAM_BOT_TOKEN);
        this.initialize();
    }

    private initialize() {
        this.bot.on('text', (ctx) => {
            const message = ctx.message.text;
            handleIncomingMessage(message);
        });

        this.bot.launch().then(() => {
            console.log('Telegram bot is running...');
        }).catch(err => {
            console.error('Failed to launch Telegram bot:', err);
        });
    }
}