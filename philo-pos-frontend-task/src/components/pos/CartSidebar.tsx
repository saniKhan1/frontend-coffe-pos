import React, { useState } from 'react';
import { useCart } from '../../context/CartContext';
import { useCustomers, useDiscounts, useCreateOrder } from '../../hooks/usePOS';
import { Button } from '../ui/Button';
import { formatCurrency } from '../../lib/utils';
import { Trash2, Plus, Minus, User, Tag, ShoppingBag, CreditCard, Banknote, Smartphone, CheckCircle, RotateCcw } from 'lucide-react';
import '../../styles/CartSidebar.css';

export function CartSidebar() {
    const {
        items, customerId, discount, paymentMethod, notes,
        updateItemQuantity, removeItem, clearCart,
        setCustomerId, setDiscount, setPaymentMethod, setNotes,
        subtotal, discountAmount, taxAmount, total
    } = useCart();

    const { data: customers } = useCustomers();
    const { data: discounts } = useDiscounts();
    const createOrderMutation = useCreateOrder();

    // Store the submitted order's confirmation data from the backend
    const [confirmedOrder, setConfirmedOrder] = useState<any>(null);

    const handleSubmit = () => {
        if (items.length === 0) return;

        createOrderMutation.mutate({
            customer_id: customerId,
            payment_method: paymentMethod,
            discount_id: discount?.id || null,
            notes: notes,
            items: items.map(item => ({
                item_id: item.menuItem.id,
                quantity: item.quantity,
                addon_ids: item.addons.map(a => a.id)
            }))
        }, {
            onSuccess: (data) => {
                setConfirmedOrder(data);
                clearCart();
            },
            onError: (err: any) => {
                alert('Failed to place order: ' + (err.response?.data?.detail || err.message));
            }
        });
    };

    // Success screen — shows backend-returned totals
    if (confirmedOrder) {
        return (
            <div className="cart-sidebar flex flex-col h-full bg-secondary border-l border-color">
                <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '2rem', textAlign: 'center' }}>
                    <div style={{ color: 'var(--success)', marginBottom: '16px' }}>
                        <CheckCircle size={64} />
                    </div>
                    <h2 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: '4px', color: 'var(--text-primary)' }}>Order Placed!</h2>
                    <p style={{ color: 'var(--text-secondary)', marginBottom: '24px' }}>
                        {confirmedOrder.order_number || `Order #${confirmedOrder.id}`}
                    </p>

                    {/* Backend-returned totals breakdown */}
                    <div style={{ width: '100%', background: 'var(--bg-primary)', borderRadius: 'var(--radius-lg)', padding: '1.25rem', border: '1px solid var(--border-color)', marginBottom: '24px' }}>
                        {confirmedOrder.subtotal !== undefined && (
                            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                                <span>Subtotal</span>
                                <span>{formatCurrency(confirmedOrder.subtotal)}</span>
                            </div>
                        )}
                        {confirmedOrder.discount_amount > 0 && (
                            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px', fontSize: '0.875rem', color: 'var(--success)', fontWeight: 500 }}>
                                <span>Discount</span>
                                <span>-{formatCurrency(confirmedOrder.discount_amount)}</span>
                            </div>
                        )}
                        {confirmedOrder.tax_amount !== undefined && (
                            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                                <span>Tax (8%)</span>
                                <span>{formatCurrency(confirmedOrder.tax_amount)}</span>
                            </div>
                        )}
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '12px', paddingTop: '12px', borderTop: '1px solid var(--border-color)', fontWeight: 700, fontSize: '1.25rem', color: 'var(--brand-primary)' }}>
                            <span>Total Charged</span>
                            <span>{formatCurrency(confirmedOrder.total)}</span>
                        </div>
                    </div>

                    <Button
                        variant="outline"
                        className="w-full"
                        onClick={() => setConfirmedOrder(null)}
                    >
                        <RotateCcw size={16} style={{ marginRight: '8px' }} />
                        New Order
                    </Button>
                </div>
            </div>
        );
    }

    return (
        <div className="cart-sidebar flex flex-col h-full bg-secondary border-l border-color">
            <div className="cart-header p-6 border-b">
                <h2 className="text-xl font-bold flex items-center gap-2">
                    <ShoppingBag /> Current Order
                </h2>
                {items.length > 0 && (
                    <button onClick={clearCart} className="text-danger text-sm hover:underline mt-2">
                        Clear all
                    </button>
                )}
            </div>

            <div className="cart-items flex-1 overflow-y-auto p-6">
                {items.length === 0 ? (
                    <div className="empty-cart flex flex-col items-center justify-center text-secondary h-full text-center">
                        <ShoppingBag size={48} className="mb-4 opacity-50" />
                        <p>No items selected.</p>
                        <p className="text-sm mt-2">Click items on the left to add them to the order.</p>
                    </div>
                ) : (
                    <div className="flex flex-col gap-4">
                        {items.map((item) => (
                            <div key={item.id} className="cart-line-item flex flex-col gap-2 pb-4 border-b">
                                <div className="flex justify-between items-start">
                                    <div>
                                        <h4 className="font-semibold">{item.menuItem.name}</h4>
                                        <p className="text-sm font-medium" style={{ color: 'var(--brand-primary)' }}>{formatCurrency(item.menuItem.price)}</p>
                                    </div>
                                    <div className="qty-controls flex items-center gap-3 bg-accent rounded-full p-1">
                                        <button
                                            onClick={() => updateItemQuantity(item.id, item.quantity - 1)}
                                            className="qty-btn"
                                        >
                                            {item.quantity === 1 ? <Trash2 size={14} style={{ color: 'var(--danger)' }} /> : <Minus size={14} />}
                                        </button>
                                        <span className="w-4 text-center text-sm font-medium">{item.quantity}</span>
                                        <button
                                            onClick={() => updateItemQuantity(item.id, item.quantity + 1)}
                                            className="qty-btn"
                                        >
                                            <Plus size={14} />
                                        </button>
                                    </div>
                                </div>
                                {item.addons.length > 0 && (
                                    <div className="cart-addons pl-2" style={{ borderLeft: '2px solid var(--brand-primary)', opacity: 0.7 }}>
                                        {item.addons.map(addon => (
                                            <div key={addon.id} className="text-xs text-secondary flex justify-between">
                                                <span>+ {addon.name}</span>
                                                <span>{formatCurrency(addon.price)}</span>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                )}
            </div>

            <div className="cart-footer p-6 border-t bg-primary">
                <div className="cart-meta flex flex-col gap-3 mb-6">
                    <div className="meta-row">
                        <label className="text-sm font-medium text-secondary flex items-center gap-2 mb-1"><User size={14} /> Customer</label>
                        <select
                            value={customerId || ''}
                            onChange={e => setCustomerId(e.target.value ? Number(e.target.value) : null)}
                            className="w-full p-2 rounded border border-color bg-secondary text-sm"
                        >
                            <option value="">Walk-in</option>
                            {customers?.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
                        </select>
                    </div>

                    <div className="meta-row">
                        <label className="text-sm font-medium text-secondary flex items-center gap-2 mb-1"><Tag size={14} /> Discount</label>
                        <select
                            value={discount?.id || ''}
                            onChange={e => {
                                const selectedId = Number(e.target.value);
                                setDiscount(discounts?.find(d => d.id === selectedId) || null);
                            }}
                            className="w-full p-2 rounded border border-color bg-secondary text-sm"
                        >
                            <option value="">None</option>
                            {discounts?.map(d => <option key={d.id} value={d.id}>{d.name} ({d.type === 'percentage' ? `${d.value}%` : `$${d.value}`})</option>)}
                        </select>
                    </div>

                    <div className="meta-row mt-2">
                        <label className="text-sm font-medium text-secondary mb-2 block">Payment Method</label>
                        <div className="flex gap-2">
                            {[
                                { id: 'cash', icon: Banknote, label: 'Cash' },
                                { id: 'card', icon: CreditCard, label: 'Card' },
                                { id: 'mobile', icon: Smartphone, label: 'Mobile' }
                            ].map(method => (
                                <button
                                    key={method.id}
                                    onClick={() => setPaymentMethod(method.id as any)}
                                    style={{
                                        flex: 1,
                                        display: 'flex',
                                        flexDirection: 'column',
                                        alignItems: 'center',
                                        padding: '8px',
                                        borderRadius: 'var(--radius-md)',
                                        border: paymentMethod === method.id ? '2px solid var(--brand-primary)' : '1px solid var(--border-color)',
                                        background: paymentMethod === method.id ? 'var(--brand-secondary)' : 'var(--bg-secondary)',
                                        color: paymentMethod === method.id ? 'var(--brand-primary)' : 'var(--text-secondary)',
                                        cursor: 'pointer',
                                        transition: 'all 0.15s ease',
                                    }}
                                >
                                    <method.icon size={16} style={{ marginBottom: '4px' }} />
                                    <span style={{ fontSize: '0.75rem' }}>{method.label}</span>
                                </button>
                            ))}
                        </div>
                    </div>

                    <div className="meta-row">
                        <label className="text-sm font-medium text-secondary mb-1 block">Notes (optional)</label>
                        <textarea
                            value={notes}
                            onChange={e => setNotes(e.target.value)}
                            rows={2}
                            placeholder="Special instructions..."
                            style={{
                                width: '100%',
                                padding: '8px',
                                borderRadius: 'var(--radius-md)',
                                border: '1px solid var(--border-color)',
                                background: 'var(--bg-secondary)',
                                color: 'var(--text-primary)',
                                fontSize: '0.875rem',
                                resize: 'none',
                            }}
                        />
                    </div>
                </div>

                <div className="cart-totals pt-4 border-t border-color flex flex-col gap-2">
                    <div className="flex justify-between text-sm text-secondary">
                        <span>Subtotal</span>
                        <span>{formatCurrency(subtotal)}</span>
                    </div>
                    {discountAmount > 0 && (
                        <div className="flex justify-between text-sm font-medium" style={{ color: 'var(--success)' }}>
                            <span>Discount ({discount?.name})</span>
                            <span>-{formatCurrency(discountAmount)}</span>
                        </div>
                    )}
                    <div className="flex justify-between text-sm text-secondary">
                        <span>Tax (8%)</span>
                        <span>{formatCurrency(taxAmount)}</span>
                    </div>
                    <div className="flex justify-between font-bold text-xl mt-2 pt-2 border-t border-color" style={{ color: 'var(--text-primary)' }}>
                        <span>Total</span>
                        <span>{formatCurrency(total)}</span>
                    </div>
                </div>

                <Button
                    className="w-full mt-6"
                    size="lg"
                    disabled={items.length === 0}
                    isLoading={createOrderMutation.isPending}
                    onClick={handleSubmit}
                >
                    Charge {formatCurrency(total)}
                </Button>
            </div>
        </div>
    );
}
