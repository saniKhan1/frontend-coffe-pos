import React, { useState } from 'react';
import { useCategories, useMenuItems } from '../../hooks/usePOS';
import { Card } from '../ui/Card';
import { Spinner } from '../ui/Spinner';
import { formatCurrency } from '../../lib/utils';
import { AddOnModal } from './AddOnModal';
import { MenuItem } from '../../lib/api';
import '../../styles/MenuGrid.css';

export function MenuGrid() {
    const [activeCategoryId, setActiveCategoryId] = useState<number | null>(null);
    const [selectedItem, setSelectedItem] = useState<MenuItem | null>(null);
    const { data: categories, isLoading: isCatsLoading } = useCategories();
    const { data: menuItems, isLoading: isItemsLoading } = useMenuItems(activeCategoryId || undefined);

    const handleItemClick = (item: MenuItem) => {
        if (item.stock_qty === 0) return;
        setSelectedItem(item);
    };

    return (
        <div className="menu-container">
            {/* Category Tabs */}
            <div className="category-tabs">
                <button
                    className={`category-tab ${activeCategoryId === null ? 'active' : ''}`}
                    onClick={() => setActiveCategoryId(null)}
                >
                    All Items
                </button>
                {isCatsLoading ? <Spinner size={16} /> : categories?.map(cat => (
                    <button
                        key={cat.id}
                        className={`category-tab ${activeCategoryId === cat.id ? 'active' : ''}`}
                        onClick={() => setActiveCategoryId(cat.id)}
                    >
                        {cat.name}
                    </button>
                ))}
            </div>

            {/* Item Grid */}
            <div className="item-grid-wrapper">
                {isItemsLoading ? (
                    <Spinner fullScreen />
                ) : menuItems?.length === 0 ? (
                    <div className="empty-state text-secondary p-8 text-center bg-primary rounded">No items found.</div>
                ) : (
                    <div className="items-grid">
                        {menuItems?.map(item => (
                            <Card
                                key={item.id}
                                className={`menu-item-card ${item.stock_qty === 0 ? 'out-of-stock' : 'in-stock'}`}
                                onClick={() => handleItemClick(item)}
                                style={{ cursor: item.stock_qty === 0 ? 'not-allowed' : 'pointer' }}
                            >
                                <div className="item-price-tag">{formatCurrency(item.price)}</div>
                                <div className="item-info">
                                    <h4 className="item-name">{item.name}</h4>
                                    <p className="item-category text-secondary text-sm">{item.category_name}</p>
                                </div>
                                {item.stock_qty === 0 && (
                                    <div className="stock-overlay">Sold Out</div>
                                )}
                                {item.stock_qty > 0 && item.stock_qty <= 10 && (
                                    <div className="stock-warning">Only {item.stock_qty} left</div>
                                )}
                            </Card>
                        ))}
                    </div>
                )}
            </div>

            {/* Add-On Modal */}
            {selectedItem && (
                <AddOnModal
                    item={selectedItem}
                    onClose={() => setSelectedItem(null)}
                />
            )}
        </div>
    );
}
