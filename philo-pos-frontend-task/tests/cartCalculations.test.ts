/**
 * TEST 3 (D2): Cart State & Totals Calculation
 *
 * Tests the CartContext calculation logic: subtotal, discount, tax, total.
 * Mirrors CartContext.tsx's useMemo logic without needing React.
 */

import { describe, it, expect } from 'vitest';

interface MockAddon { id: number; price: number; name: string; }
interface MockMenuItem { id: number; price: number; name: string; }
interface MockCartItem { id: string; menuItem: MockMenuItem; quantity: number; addons: MockAddon[]; }
interface MockDiscount { id: number; type: 'percentage' | 'flat'; value: number; name: string; is_active: boolean; }

// Pure calculation functions extracted from CartContext.tsx
function calcSubtotal(items: MockCartItem[]): number {
    return items.reduce((acc, item) => {
        const addonSum = item.addons.reduce((sum, a) => sum + a.price, 0);
        return acc + (item.menuItem.price + addonSum) * item.quantity;
    }, 0);
}

function calcDiscount(subtotal: number, discount: MockDiscount | null): number {
    if (!discount || subtotal === 0) return 0;
    if (discount.type === 'percentage') return subtotal * (discount.value / 100);
    return Math.min(discount.value, subtotal);
}

function calcTax(subtotal: number, discountAmount: number): number {
    return (subtotal - discountAmount) * 0.08;
}

function calcTotal(subtotal: number, discountAmount: number, taxAmount: number): number {
    return subtotal - discountAmount + taxAmount;
}

const mockItem: MockMenuItem = { id: 1, price: 10, name: 'Latte' };
const mockAddon: MockAddon = { id: 1, price: 2, name: 'Extra Shot' };

describe('Cart Totals Calculation', () => {
    it('should calculate subtotal correctly with no addons', () => {
        const items: MockCartItem[] = [{ id: 'a', menuItem: mockItem, quantity: 2, addons: [] }];
        expect(calcSubtotal(items)).toBe(20); // 10 * 2
    });

    it('should include addon prices in subtotal', () => {
        const items: MockCartItem[] = [{ id: 'a', menuItem: mockItem, quantity: 1, addons: [mockAddon] }];
        expect(calcSubtotal(items)).toBe(12); // (10 + 2) * 1
    });

    it('should return 0 subtotal for empty cart', () => {
        expect(calcSubtotal([])).toBe(0);
    });

    it('should calculate percentage discount correctly', () => {
        const discount: MockDiscount = { id: 1, type: 'percentage', value: 10, name: '10%', is_active: true };
        expect(calcDiscount(100, discount)).toBe(10); // 10% of 100
    });

    it('should calculate flat discount correctly', () => {
        const discount: MockDiscount = { id: 2, type: 'flat', value: 5, name: '$5 Off', is_active: true };
        expect(calcDiscount(100, discount)).toBe(5);
    });

    it('should not make flat discount exceed subtotal', () => {
        const discount: MockDiscount = { id: 2, type: 'flat', value: 999, name: 'Huge discount', is_active: true };
        expect(calcDiscount(50, discount)).toBe(50); // capped at subtotal
    });

    it('should apply 8% tax on discounted amount', () => {
        const tax = calcTax(100, 10); // 8% of (100 - 10) = 7.2
        expect(tax).toBeCloseTo(7.2);
    });

    it('should calculate total as subtotal - discount + tax', () => {
        const total = calcTotal(100, 10, 7.2);
        expect(total).toBeCloseTo(97.2);
    });
});
