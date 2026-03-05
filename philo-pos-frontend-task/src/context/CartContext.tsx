import React, { createContext, useContext, useState, useMemo } from 'react';
import { MenuItem, Addon, Discount } from '../lib/api';

export interface CartItem {
    id: string; // Unique local ID for cart management
    menuItem: MenuItem;
    quantity: number;
    addons: Addon[];
}

interface CartContextType {
    items: CartItem[];
    customerId: number | null;
    discount: Discount | null;
    paymentMethod: 'cash' | 'card' | 'mobile';
    notes: string;

    addItem: (menuItem: MenuItem, addons?: Addon[], quantity?: number) => void;
    updateItemQuantity: (id: string, quantity: number) => void;
    removeItem: (id: string) => void;
    clearCart: () => void;

    setCustomerId: (id: number | null) => void;
    setDiscount: (discount: Discount | null) => void;
    setPaymentMethod: (method: 'cash' | 'card' | 'mobile') => void;
    setNotes: (notes: string) => void;

    subtotal: number;
    discountAmount: number;
    taxAmount: number;
    total: number;
}

const CartContext = createContext<CartContextType | undefined>(undefined);

export function CartProvider({ children }: { children: React.ReactNode }) {
    const [items, setItems] = useState<CartItem[]>([]);
    const [customerId, setCustomerId] = useState<number | null>(null);
    const [discount, setDiscount] = useState<Discount | null>(null);
    const [paymentMethod, setPaymentMethod] = useState<'cash' | 'card' | 'mobile'>('card');
    const [notes, setNotes] = useState('');

    const addItem = (menuItem: MenuItem, addons: Addon[] = [], quantity: number = 1) => {
        const newItem: CartItem = {
            id: Math.random().toString(36).substring(7),
            menuItem,
            quantity,
            addons
        };
        setItems(prev => [...prev, newItem]);
    };

    const updateItemQuantity = (id: string, quantity: number) => {
        if (quantity <= 0) {
            removeItem(id);
            return;
        }
        setItems(prev => prev.map(item => item.id === id ? { ...item, quantity } : item));
    };

    const removeItem = (id: string) => {
        setItems(prev => prev.filter(item => item.id !== id));
    };

    const clearCart = () => {
        setItems([]);
        setCustomerId(null);
        setDiscount(null);
        setNotes('');
    };

    // Local calculations to match backend logic
    const subtotal = useMemo(() => {
        return items.reduce((acc, item) => {
            const addonSum = item.addons.reduce((sum, a) => sum + a.price, 0);
            const lineTotal = (item.menuItem.price + addonSum) * item.quantity;
            return acc + lineTotal;
        }, 0);
    }, [items]);

    const discountAmount = useMemo(() => {
        if (!discount || subtotal === 0) return 0;
        if (discount.type === 'percentage') {
            return subtotal * (discount.value / 100);
        }
        return Math.min(discount.value, subtotal); // flat amount
    }, [discount, subtotal]);

    const taxAmount = useMemo(() => {
        return (subtotal - discountAmount) * 0.08; // 8% tax hardcoded per requirements
    }, [subtotal, discountAmount]);

    const total = useMemo(() => {
        return subtotal - discountAmount + taxAmount;
    }, [subtotal, discountAmount, taxAmount]);

    return (
        <CartContext.Provider value={{
            items, customerId, discount, paymentMethod, notes,
            addItem, updateItemQuantity, removeItem, clearCart,
            setCustomerId, setDiscount, setPaymentMethod, setNotes,
            subtotal, discountAmount, taxAmount, total
        }}>
            {children}
        </CartContext.Provider>
    );
}

export function useCart() {
    const context = useContext(CartContext);
    if (context === undefined) {
        throw new Error('useCart must be used within a CartProvider');
    }
    return context;
}
