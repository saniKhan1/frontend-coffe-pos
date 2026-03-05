import { describe, it, expect } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { CartProvider, useCart } from '../src/context/CartContext';
import React from 'react';

// Mock data
const mockMenuItem = {
    id: 1,
    category_id: 1,
    category_name: 'Hot Coffee',
    name: 'Caramel Latte',
    description: 'Espresso with steamed milk and caramel',
    price: 5.50,
    image_url: null,
    is_available: true,
    stock_qty: -1,
};

describe('Cart State Management', () => {
    it('should add an item to the cart and calculate subtotal correctly', () => {
        const wrapper = ({ children }: { children: React.ReactNode }) => <CartProvider>{children}</CartProvider>;
        const { result } = renderHook(() => useCart(), { wrapper });

        act(() => {
            result.current.addItem(mockMenuItem, [], 2); // 2 Caramel Lattes
        });

        expect(result.current.items.length).toBe(1);
        expect(result.current.items[0].quantity).toBe(2);
        expect(result.current.subtotal).toBe(11.00); // 5.50 * 2

        // Test tax calculation (8% of 11.00 = 0.88)
        expect(result.current.taxAmount).toBe(0.88);

        // Total should be 11.88
        expect(result.current.total).toBe(11.88);
    });

    it('should calculate discounts correctly (flat amount)', () => {
        const wrapper = ({ children }: { children: React.ReactNode }) => <CartProvider>{children}</CartProvider>;
        const { result } = renderHook(() => useCart(), { wrapper });

        act(() => {
            result.current.addItem(mockMenuItem, [], 2); // Subtotal: 11.00
            result.current.setDiscount({ id: 1, name: '$2 Off', type: 'flat', value: 2.00, is_active: true });
        });

        expect(result.current.discountAmount).toBe(2.00);
        // Tax should now be on the discounted amount: (11.00 - 2.00) * 0.08 = 0.72
        expect(result.current.taxAmount).toBe(0.72);
        // Total: 9.00 sub-discount + 0.72 tax = 9.72
        expect(result.current.total).toBe(9.72);
    });
});
