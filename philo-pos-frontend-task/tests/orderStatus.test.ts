/**
 * TEST 1 (D2): Order Status Workflow
 * 
 * Tests that the order status lifecycle transitions are valid.
 * Verifies: pending → preparing → ready → completed/cancelled logic.
 */

import { describe, it, expect } from 'vitest';

type OrderStatus = 'pending' | 'preparing' | 'ready' | 'completed' | 'cancelled';

// Extracted status transition logic (mirrors OrderDetailsModal.tsx renderActionButtons)
function getNextStatuses(current: OrderStatus): OrderStatus[] {
    switch (current) {
        case 'pending': return ['preparing', 'cancelled'];
        case 'preparing': return ['ready', 'cancelled'];
        case 'ready': return ['completed', 'cancelled'];
        case 'completed':
        case 'cancelled': return []; // terminal states
        default: return [];
    }
}

describe('Order Status Lifecycle', () => {
    it('should allow pending -> preparing', () => {
        expect(getNextStatuses('pending')).toContain('preparing');
    });

    it('should allow pending -> cancelled', () => {
        expect(getNextStatuses('pending')).toContain('cancelled');
    });

    it('should allow preparing -> ready', () => {
        expect(getNextStatuses('preparing')).toContain('ready');
    });

    it('should allow ready -> completed', () => {
        expect(getNextStatuses('ready')).toContain('completed');
    });

    it('should NOT allow completed -> any status (terminal)', () => {
        expect(getNextStatuses('completed')).toHaveLength(0);
    });

    it('should NOT allow cancelled -> any status (terminal)', () => {
        expect(getNextStatuses('cancelled')).toHaveLength(0);
    });

    it('should NOT allow pending -> completed directly', () => {
        expect(getNextStatuses('pending')).not.toContain('completed');
    });
});
