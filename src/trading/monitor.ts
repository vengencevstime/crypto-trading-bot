import { PositionManager } from './positionManager';
import { Database } from '../database/queries';
import { MEXC } from '../exchanges/mexc';
import { Kraken } from '../exchanges/kraken';

const positionManager = new PositionManager();
const database = new Database();
const mexc = new MEXC();
const kraken = new Kraken();

export async function monitorPositions() {
    const openPositions = await database.getOpenPositions();

    for (const position of openPositions) {
        const status = await positionManager.checkPositionStatus(position);

        if (status === 'closed') {
            await database.updatePositionStatus(position.id, 'closed');
        } else if (status === 'monitor') {
            // Logic to monitor the position
            await positionManager.monitorPosition(position);
        }
    }
}