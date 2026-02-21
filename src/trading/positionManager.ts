export class PositionManager {
    private positions: Map<string, any>;

    constructor() {
        this.positions = new Map();
    }

    public openPosition(positionId: string, tradeData: any): void {
        if (!this.positions.has(positionId)) {
            this.positions.set(positionId, tradeData);
            // Logic to open position on exchange can be added here
        } else {
            throw new Error(`Position with ID ${positionId} already exists.`);
        }
    }

    public closePosition(positionId: string): void {
        if (this.positions.has(positionId)) {
            this.positions.delete(positionId);
            // Logic to close position on exchange can be added here
        } else {
            throw new Error(`Position with ID ${positionId} does not exist.`);
        }
    }

    public getPosition(positionId: string): any | undefined {
        return this.positions.get(positionId);
    }

    public getAllPositions(): Map<string, any> {
        return this.positions;
    }

    public updatePosition(positionId: string, updatedData: any): void {
        if (this.positions.has(positionId)) {
            this.positions.set(positionId, { ...this.positions.get(positionId), ...updatedData });
        } else {
            throw new Error(`Position with ID ${positionId} does not exist.`);
        }
    }
}