export interface Message {
    id: string;
    content: string;
    timestamp: Date;
    userId: string;
}

export interface TradeData {
    symbol: string;
    action: 'buy' | 'sell';
    quantity: number;
    price: number;
    timestamp: Date;
}

export interface Position {
    id: string;
    symbol: string;
    entryPrice: number;
    quantity: number;
    status: 'open' | 'closed';
    timestamp: Date;
}