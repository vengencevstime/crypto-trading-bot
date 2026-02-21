import { parseMessage } from '../parser/messageParser';
import { insertParsedMessage } from '../database/queries';
import { Message } from '../types';

export const handleIncomingMessage = async (message: string) => {
    try {
        const parsedData = parseMessage(message);
        
        if (parsedData) {
            await insertParsedMessage(parsedData);
            console.log('Message parsed and stored:', parsedData);
        } else {
            console.log('Invalid message format:', message);
        }
    } catch (error) {
        console.error('Error handling incoming message:', error);
    }
};