import React from 'react';
import { useOrder, useUpdateOrderStatus } from '../../hooks/useOrders';
import { Card, CardContent } from '../ui/Card';
import { Button } from '../ui/Button';
import { Spinner } from '../ui/Spinner';
import { OrderStatusBadge } from '../ui/OrderStatusBadge';
import { formatCurrency, formatDate } from '../../lib/utils';
import { X, Clock, User, CreditCard, ChevronRight } from 'lucide-react';
import '../../styles/Modal.css';

interface OrderDetailsModalProps {
    orderId: number;
    onClose: () => void;
}

export function OrderDetailsModal({ orderId, onClose }: OrderDetailsModalProps) {
    const { data: order, isLoading } = useOrder(orderId);
    const updateStatusResult = useUpdateOrderStatus();

    if (!orderId) return null;

    const handleStatusChange = (newStatus: any) => {
        updateStatusResult.mutate({ id: orderId, status: newStatus });
    };

    const renderActionButtons = () => {
        if (!order) return null;

        switch (order.status) {
            case 'pending':
                return (
                    <>
                        <Button variant="danger" outline onClick={() => handleStatusChange('cancelled')} isLoading={updateStatusResult.isPending}>
                            Cancel Order
                        </Button>
                        <Button onClick={() => handleStatusChange('preparing')} isLoading={updateStatusResult.isPending}>
                            Start Preparing <ChevronRight size={16} />
                        </Button>
                    </>
                );
            case 'preparing':
                return (
                    <>
                        <Button variant="danger" outline onClick={() => handleStatusChange('cancelled')} isLoading={updateStatusResult.isPending}>
                            Cancel Order
                        </Button>
                        <Button onClick={() => handleStatusChange('ready')} isLoading={updateStatusResult.isPending}>
                            Mark Ready <ChevronRight size={16} />
                        </Button>
                    </>
                );
            case 'ready':
                return (
                    <>
                        <Button variant="danger" outline onClick={() => handleStatusChange('cancelled')} isLoading={updateStatusResult.isPending}>
                            Cancel Order
                        </Button>
                        <Button onClick={() => handleStatusChange('completed')} isLoading={updateStatusResult.isPending}>
                            Complete Order <ChevronRight size={16} />
                        </Button>
                    </>
                );
            default:
                return null; // completed or cancelled
        }
    };

    return (
        <div className="modal-backdrop" onClick={onClose}>
            <div className="modal-content" onClick={e => e.stopPropagation()}>
                {isLoading || !order ? (
                    <div style={{ height: '400px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                        <Spinner />
                    </div>
                ) : (
                    <>
                        <div className="modal-header border-b">
                            <div>
                                <h2 className="modal-title">{order.order_number}</h2>
                                <div className="flex items-center gap-2 mt-1 text-secondary text-sm">
                                    <Clock size={14} />
                                    <span>{formatDate(order.created_at)}</span>
                                    <span className="mx-2">•</span>
                                    <OrderStatusBadge status={order.status} />
                                </div>
                            </div>
                            <button className="modal-close-btn" onClick={onClose}>
                                <X size={24} />
                            </button>
                        </div>

                        <div className="modal-body bg-primary">
                            <div className="order-grid">
                                <div className="order-main-info">
                                    <div className="items-list">
                                        <h3 className="section-title">Order Items</h3>
                                        {order.items.map(item => (
                                            <div key={item.id} className="order-line-item">
                                                <div className="item-qty-name">
                                                    <span className="item-qty">{item.quantity}x</span>
                                                    <span className="item-name font-medium">{item.item_name}</span>
                                                </div>
                                                <div className="item-price font-medium">{formatCurrency(item.subtotal)}</div>

                                                {item.addons.length > 0 && (
                                                    <div className="item-addons ml-6 mt-1 text-sm text-secondary">
                                                        {item.addons.map(addon => (
                                                            <div key={addon.id} className="flex justify-between">
                                                                <span>+ {addon.addon_name}</span>
                                                                <span>{formatCurrency(addon.price)}</span>
                                                            </div>
                                                        ))}
                                                    </div>
                                                )}
                                            </div>
                                        ))}
                                    </div>

                                    <div className="order-totals mt-6 pt-4 border-t">
                                        <div className="total-line text-secondary">
                                            <span>Subtotal</span>
                                            <span>{formatCurrency(order.subtotal)}</span>
                                        </div>
                                        {order.discount_amount > 0 && (
                                            <div className="total-line text-success">
                                                <span>Discount</span>
                                                <span>-{formatCurrency(order.discount_amount)}</span>
                                            </div>
                                        )}
                                        <div className="total-line text-secondary">
                                            <span>Tax (8%)</span>
                                            <span>{formatCurrency(order.tax_amount)}</span>
                                        </div>
                                        <div className="total-line grand-total mt-4 pt-4 border-t font-bold text-lg">
                                            <span>Total</span>
                                            <span>{formatCurrency(order.total)}</span>
                                        </div>
                                    </div>
                                </div>

                                <div className="order-sidebar">
                                    <Card className="shadow-none">
                                        <CardContent className="p-4 flex flex-col gap-4">
                                            <div>
                                                <h4 className="text-sm font-medium text-secondary mb-1 flex items-center gap-2">
                                                    <User size={16} /> Customer
                                                </h4>
                                                <p className="font-medium">{order.customer_name || 'Walk-in'}</p>
                                            </div>

                                            <div>
                                                <h4 className="text-sm font-medium text-secondary mb-1 flex items-center gap-2">
                                                    <CreditCard size={16} /> Payment Method
                                                </h4>
                                                <p className="font-medium capitalize">{order.payment_method}</p>
                                            </div>

                                            {order.notes && (
                                                <div>
                                                    <h4 className="text-sm font-medium text-secondary mb-1">Notes</h4>
                                                    <p className="text-sm bg-accent p-2 rounded">{order.notes}</p>
                                                </div>
                                            )}
                                        </CardContent>
                                    </Card>

                                    <div className="modal-actions mt-6 flex flex-col gap-2">
                                        {renderActionButtons()}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </>
                )}
            </div>
        </div>
    );
}
