export interface TradeData {
    action: 'buy' | 'sell';
    symbol: string;
    quantity: number;
    price: number;
    timestamp: Date;
}

export function parseMessage(message: string): TradeData | null {
    const regex = /(?<action>buy|sell)\s+(?<symbol>[A-Z]{3,5})\s+(?<quantity>\d+(\.\d+)?)\s+at\s+(?<price>\d+(\.\d+)?)/i;
    const match = message.match(regex);

    if (match && match.groups) {
        return {
            action: match.groups.action.toLowerCase() as 'buy' | 'sell',
            symbol: match.groups.symbol,
            quantity: parseFloat(match.groups.quantity),
            price: parseFloat(match.groups.price),
            timestamp: new Date(),
        };
    }

    return null;
}