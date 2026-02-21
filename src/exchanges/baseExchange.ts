export abstract class BaseExchange {
    abstract openPosition(tradeData: any): Promise<string>;
    abstract closePosition(positionId: string): Promise<boolean>;
    abstract monitorPosition(positionId: string): Promise<any>;
}