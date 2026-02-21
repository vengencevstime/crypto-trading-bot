export function validateTradeData(data: any): boolean {
    if (!data.symbol || typeof data.symbol !== 'string') {
        return false;
    }
    if (!data.amount || typeof data.amount !== 'number' || data.amount <= 0) {
        return false;
    }
    if (!data.price || typeof data.price !== 'number' || data.price <= 0) {
        return false;
    }
    return true;
}

export function validateMessageFormat(message: string): boolean {
    const messagePattern = /^Trade: (\w+) Amount: (\d+(\.\d+)?) Price: (\d+(\.\d+)?)$/;
    return messagePattern.test(message);
}