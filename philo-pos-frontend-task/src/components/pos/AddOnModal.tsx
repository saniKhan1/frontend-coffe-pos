import React, { useState } from 'react';
import { MenuItem, Addon } from '../../lib/api';
import { useAddons } from '../../hooks/usePOS';
import { useCart } from '../../context/CartContext';
import { Button } from '../ui/Button';
import { Spinner } from '../ui/Spinner';
import { formatCurrency } from '../../lib/utils';
import { X, Plus, Minus, ShoppingBag } from 'lucide-react';
import '../../styles/Modal.css';

interface AddOnModalProps {
    item: MenuItem;
    onClose: () => void;
}

export function AddOnModal({ item, onClose }: AddOnModalProps) {
    const { data: allAddons, isLoading } = useAddons();
    const { addItem } = useCart();
    const [selectedAddons, setSelectedAddons] = useState<Addon[]>([]);
    const [quantity, setQuantity] = useState(1);

    const toggleAddon = (addon: Addon) => {
        setSelectedAddons(prev =>
            prev.find(a => a.id === addon.id)
                ? prev.filter(a => a.id !== addon.id)
                : [...prev, addon]
        );
    };

    const addonsTotal = selectedAddons.reduce((sum, a) => sum + a.price, 0);
    const lineTotal = (item.price + addonsTotal) * quantity;

    const handleAddToCart = () => {
        addItem(item, selectedAddons, quantity);
        onClose();
    };

    return (
        <div className="modal-backdrop" onClick={onClose}>
            <div className="modal-content" style={{ maxWidth: '480px' }} onClick={e => e.stopPropagation()}>
                <div className="modal-header border-b">
                    <div>
                        <h2 className="modal-title">{item.name}</h2>
                        <p className="text-secondary text-sm mt-1">{item.description || 'Add to your order'}</p>
                    </div>
                    <button className="modal-close-btn" onClick={onClose}>
                        <X size={24} />
                    </button>
                </div>

                <div className="modal-body bg-primary" style={{ padding: '1.5rem' }}>
                    {/* Quantity selector */}
                    <div className="flex items-center justify-between mb-6">
                        <span className="font-semibold text-primary">Quantity</span>
                        <div className="flex items-center gap-4 bg-accent rounded-full px-4 py-2">
                            <button
                                onClick={() => setQuantity(q => Math.max(1, q - 1))}
                                className="qty-btn"
                            >
                                <Minus size={16} />
                            </button>
                            <span className="font-bold text-xl w-6 text-center">{quantity}</span>
                            <button
                                onClick={() => setQuantity(q => q + 1)}
                                className="qty-btn"
                            >
                                <Plus size={16} />
                            </button>
                        </div>
                    </div>

                    {/* Add-ons */}
                    <div>
                        <h3 className="font-semibold text-primary mb-3">Add-Ons <span className="text-secondary font-normal text-sm">(optional)</span></h3>
                        {isLoading ? (
                            <div className="flex justify-center py-4"><Spinner /></div>
                        ) : allAddons && allAddons.length > 0 ? (
                            <div className="flex flex-col gap-2">
                                {allAddons.map(addon => {
                                    const isSelected = !!selectedAddons.find(a => a.id === addon.id);
                                    return (
                                        <button
                                            key={addon.id}
                                            onClick={() => toggleAddon(addon)}
                                            style={{
                                                display: 'flex',
                                                alignItems: 'center',
                                                justifyContent: 'space-between',
                                                padding: '12px 16px',
                                                borderRadius: 'var(--radius-md)',
                                                border: isSelected ? '2px solid var(--brand-primary)' : '1px solid var(--border-color)',
                                                background: isSelected ? 'var(--brand-secondary)' : 'var(--bg-secondary)',
                                                cursor: 'pointer',
                                                transition: 'all 0.15s ease',
                                                textAlign: 'left',
                                            }}
                                        >
                                            <span style={{ color: isSelected ? 'var(--brand-primary)' : 'var(--text-primary)', fontWeight: isSelected ? 600 : 400 }}>
                                                {addon.name}
                                            </span>
                                            <span style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
                                                +{formatCurrency(addon.price)}
                                            </span>
                                        </button>
                                    );
                                })}
                            </div>
                        ) : (
                            <p className="text-secondary text-sm">No add-ons available.</p>
                        )}
                    </div>

                    {/* Price summary */}
                    <div className="mt-6 pt-4 border-t border-color flex flex-col gap-1">
                        <div className="flex justify-between text-sm text-secondary">
                            <span>Base price ({quantity}x)</span>
                            <span>{formatCurrency(item.price * quantity)}</span>
                        </div>
                        {selectedAddons.length > 0 && (
                            <div className="flex justify-between text-sm text-secondary">
                                <span>Add-ons ({quantity}x)</span>
                                <span>+{formatCurrency(addonsTotal * quantity)}</span>
                            </div>
                        )}
                        <div className="flex justify-between font-bold text-lg mt-2" style={{ color: 'var(--brand-primary)' }}>
                            <span>Line Total</span>
                            <span>{formatCurrency(lineTotal)}</span>
                        </div>
                    </div>
                </div>

                <div style={{ padding: '1.5rem', borderTop: '1px solid var(--border-color)', background: 'var(--bg-secondary)' }}>
                    <Button className="w-full" size="lg" onClick={handleAddToCart}>
                        <ShoppingBag size={18} style={{ marginRight: '8px' }} />
                        Add to Cart — {formatCurrency(lineTotal)}
                    </Button>
                </div>
            </div>
        </div>
    );
}
