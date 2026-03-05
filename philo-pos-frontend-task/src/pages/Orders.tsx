import { useState } from 'react';
import { PageHeader } from '../components/layout/PageHeader';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Spinner } from '../components/ui/Spinner';
import { ErrorState } from '../components/ui/ErrorState';
import { OrderStatusBadge } from '../components/ui/OrderStatusBadge';
import { useOrders, OrderFilters } from '../hooks/useOrders';
import { formatCurrency, formatDate } from '../lib/utils';
import { ChevronLeft, ChevronRight, Eye, Filter } from 'lucide-react';
import { OrderDetailsModal } from '../components/orders/OrderDetailsModal';
import '../styles/Table.css';

const STATUS_OPTIONS = ['all', 'pending', 'preparing', 'ready', 'completed', 'cancelled'];
const PAYMENT_OPTIONS = [
    { value: 'all', label: 'All Payments' },
    { value: 'cash', label: 'Cash' },
    { value: 'card', label: 'Card' },
    { value: 'mobile', label: 'Mobile' },
];

export default function Orders() {
    const [filters, setFilters] = useState<OrderFilters>({
        page: 1,
        per_page: 15,
        status: 'all',
    });
    const [dateFrom, setDateFrom] = useState('');
    const [dateTo, setDateTo] = useState('');
    const [paymentFilter, setPaymentFilter] = useState('all');
    const [selectedOrderId, setSelectedOrderId] = useState<number | null>(null);

    const activeFilters: OrderFilters = {
        ...filters,
        start_date: dateFrom || undefined,
        end_date: dateTo || undefined,
    };

    const { data, isLoading, isError, refetch } = useOrders(activeFilters);

    const handleStatusFilter = (status: string) => {
        setFilters(prev => ({ ...prev, status, page: 1 }));
    };

    const handlePageChange = (newPage: number) => {
        setFilters(prev => ({ ...prev, page: newPage }));
    };

    // Client-side payment filter (backend may not support this parameter)
    const displayOrders = data?.items.filter(order =>
        paymentFilter === 'all' || order.payment_method === paymentFilter
    );

    return (
        <div className="orders-page animate-fade-in">
            <PageHeader
                title="Orders"
                description="Manage current and past orders."
            />

            <div className="page-content" style={{ padding: '24px' }}>
                {/* Status filter tabs */}
                <div style={{ display: 'flex', gap: '8px', marginBottom: '16px', flexWrap: 'wrap' }}>
                    {STATUS_OPTIONS.map(status => (
                        <Button
                            key={status}
                            variant={filters.status === status ? 'primary' : 'outline'}
                            size="sm"
                            onClick={() => handleStatusFilter(status)}
                            className="capitalize"
                        >
                            {status}
                        </Button>
                    ))}
                </div>

                {/* Date and Payment filters */}
                <Card className="glass-panel" style={{ marginBottom: '16px' }}>
                    <div style={{ padding: '12px 20px', display: 'flex', gap: '16px', alignItems: 'center', flexWrap: 'wrap' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
                            <Filter size={14} /> Filters:
                        </div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <label style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>From</label>
                            <input
                                type="date"
                                value={dateFrom}
                                onChange={e => { setDateFrom(e.target.value); setFilters(p => ({ ...p, page: 1 })); }}
                                style={{
                                    padding: '6px 10px',
                                    borderRadius: 'var(--radius-md)',
                                    border: '1px solid var(--border-color)',
                                    background: 'var(--bg-secondary)',
                                    color: 'var(--text-primary)',
                                    fontSize: '0.8rem',
                                }}
                            />
                        </div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <label style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>To</label>
                            <input
                                type="date"
                                value={dateTo}
                                onChange={e => { setDateTo(e.target.value); setFilters(p => ({ ...p, page: 1 })); }}
                                style={{
                                    padding: '6px 10px',
                                    borderRadius: 'var(--radius-md)',
                                    border: '1px solid var(--border-color)',
                                    background: 'var(--bg-secondary)',
                                    color: 'var(--text-primary)',
                                    fontSize: '0.8rem',
                                }}
                            />
                        </div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <label style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Payment</label>
                            <select
                                value={paymentFilter}
                                onChange={e => setPaymentFilter(e.target.value)}
                                style={{
                                    padding: '6px 10px',
                                    borderRadius: 'var(--radius-md)',
                                    border: '1px solid var(--border-color)',
                                    background: 'var(--bg-secondary)',
                                    color: 'var(--text-primary)',
                                    fontSize: '0.8rem',
                                }}
                            >
                                {PAYMENT_OPTIONS.map(p => <option key={p.value} value={p.value}>{p.label}</option>)}
                            </select>
                        </div>
                        {(dateFrom || dateTo || paymentFilter !== 'all') && (
                            <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => { setDateFrom(''); setDateTo(''); setPaymentFilter('all'); }}
                            >
                                Clear
                            </Button>
                        )}
                    </div>
                </Card>

                <Card className="glass-panel">
                    {isLoading ? (
                        <div style={{ padding: '48px 0' }}><Spinner fullScreen /></div>
                    ) : isError ? (
                        <ErrorState onRetry={refetch} />
                    ) : displayOrders?.length === 0 ? (
                        <div style={{ padding: '48px 24px', textAlign: 'center', color: 'var(--text-secondary)' }}>
                            No orders found matching the criteria.
                        </div>
                    ) : (
                        <>
                            <div className="table-container">
                                <table className="ui-table">
                                    <thead>
                                        <tr>
                                            <th>Order #</th>
                                            <th>Date</th>
                                            <th>Customer</th>
                                            <th>Status</th>
                                            <th>Payment</th>
                                            <th>Total</th>
                                            <th align="right">Details</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {displayOrders?.map(order => (
                                            <tr key={order.id} onClick={() => setSelectedOrderId(order.id)} style={{ cursor: 'pointer' }}>
                                                <td className="font-medium">{order.order_number}</td>
                                                <td className="text-secondary">{formatDate(order.created_at)}</td>
                                                <td>{order.customer_name || 'Walk-in'}</td>
                                                <td><OrderStatusBadge status={order.status} /></td>
                                                <td className="capitalize text-secondary">{order.payment_method}</td>
                                                <td className="font-medium">{formatCurrency(order.total)}</td>
                                                <td align="right">
                                                    <Button variant="ghost" size="sm">
                                                        <Eye size={16} />
                                                    </Button>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>

                            {data && data.total_pages > 1 && (
                                <div className="table-pagination" style={{ padding: '16px 24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid var(--border-color)' }}>
                                    <span className="text-secondary text-sm">
                                        Showing {(data.page - 1) * data.per_page + 1} to {Math.min(data.page * data.per_page, data.total)} of {data.total} orders
                                    </span>
                                    <div style={{ display: 'flex', gap: '8px' }}>
                                        <Button
                                            variant="outline"
                                            size="sm"
                                            disabled={data.page === 1}
                                            onClick={() => handlePageChange(data.page - 1)}
                                        >
                                            <ChevronLeft size={16} /> Prev
                                        </Button>
                                        <span style={{ padding: '0 8px', alignSelf: 'center', fontSize: '14px' }}>Page {data.page} of {data.total_pages}</span>
                                        <Button
                                            variant="outline"
                                            size="sm"
                                            disabled={data.page === data.total_pages}
                                            onClick={() => handlePageChange(data.page + 1)}
                                        >
                                            Next <ChevronRight size={16} />
                                        </Button>
                                    </div>
                                </div>
                            )}
                        </>
                    )}
                </Card>
            </div>

            {selectedOrderId && (
                <OrderDetailsModal
                    orderId={selectedOrderId}
                    onClose={() => setSelectedOrderId(null)}
                />
            )}
        </div>
    );
}
