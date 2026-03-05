import React from 'react';
import { PageHeader } from '../components/layout/PageHeader';
import { useDateFilter } from '../context/DateFilterContext';
import { useDashboardSummary, useInventoryAlerts } from '../hooks/useDashboard';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card';
import { Spinner } from '../components/ui/Spinner';
import { ErrorState } from '../components/ui/ErrorState';
import { Badge } from '../components/ui/Badge';
import { formatCurrency } from '../lib/utils';
import { DollarSign, ShoppingCart, TrendingUp, Users, AlertCircle } from 'lucide-react';
import { DashboardCharts } from '../components/dashboard/DashboardCharts';
import '../styles/Dashboard.css';

export default function Dashboard() {
    const { startDate, endDate } = useDateFilter();

    const {
        data: summary,
        isLoading: isSummaryLoading,
        isError: isSummaryError,
        refetch: refetchSummary
    } = useDashboardSummary({ startDate, endDate });

    const {
        data: alerts,
        isLoading: isAlertsLoading
    } = useInventoryAlerts();

    if (isSummaryLoading) return <Spinner fullScreen />;
    if (isSummaryError) return <ErrorState onRetry={refetchSummary} />;

    return (
        <div className="dashboard-page animate-fade-in">
            <PageHeader
                title="Dashboard Overview"
                description="Key performance indicators and business analytics."
                showDateFilter
            />

            <div className="dashboard-content">
                {/* KPI Grid */}
                <div className="kpi-grid">
                    <Card className="kpi-card glass-panel">
                        <CardContent className="kpi-content">
                            <div className="kpi-info">
                                <p className="kpi-label">Total Revenue</p>
                                <h2 className="kpi-value">{formatCurrency(summary?.total_revenue || 0)}</h2>
                                <div className="kpi-trend">
                                    <TrendingUp size={14} className={summary?.revenue_change_pct && summary.revenue_change_pct >= 0 ? 'text-success' : 'text-danger'} />
                                    <span className={summary?.revenue_change_pct && summary.revenue_change_pct >= 0 ? 'text-success' : 'text-danger'}>
                                        {summary?.revenue_change_pct}%
                                    </span>
                                    <span className="text-secondary ml-1">vs last period</span>
                                </div>
                            </div>
                            <div className="kpi-icon brand-primary">
                                <DollarSign size={24} />
                            </div>
                        </CardContent>
                    </Card>

                    <Card className="kpi-card glass-panel">
                        <CardContent className="kpi-content">
                            <div className="kpi-info">
                                <p className="kpi-label">Total Orders</p>
                                <h2 className="kpi-value">{summary?.total_orders || 0}</h2>
                                <div className="kpi-trend">
                                    <TrendingUp size={14} className={summary?.order_change_pct && summary.order_change_pct >= 0 ? 'text-success' : 'text-danger'} />
                                    <span className={summary?.order_change_pct && summary.order_change_pct >= 0 ? 'text-success' : 'text-danger'}>
                                        {summary?.order_change_pct}%
                                    </span>
                                    <span className="text-secondary ml-1">vs last period</span>
                                </div>
                            </div>
                            <div className="kpi-icon brand-secondary">
                                <ShoppingCart size={24} />
                            </div>
                        </CardContent>
                    </Card>

                    <Card className="kpi-card glass-panel">
                        <CardContent className="kpi-content">
                            <div className="kpi-info">
                                <p className="kpi-label">Avg Order Value</p>
                                <h2 className="kpi-value">{formatCurrency(summary?.avg_order_value || 0)}</h2>
                                <p className="kpi-subtext">Completed: {summary?.completed_orders} | Cancelled: {summary?.cancelled_orders}</p>
                            </div>
                            <div className="kpi-icon info">
                                <TrendingUp size={24} />
                            </div>
                        </CardContent>
                    </Card>

                    <Card className="kpi-card glass-panel">
                        <CardContent className="kpi-content">
                            <div className="kpi-info">
                                <p className="kpi-label">Customers</p>
                                <h2 className="kpi-value">{summary?.total_customers || 0}</h2>
                                <p className="kpi-subtext">New Customers: {summary?.new_customers}</p>
                            </div>
                            <div className="kpi-icon warning">
                                <Users size={24} />
                            </div>
                        </CardContent>
                    </Card>
                </div>

                {/* Next Section: Charts and Inventory... */}
                <DashboardCharts />

                <div className="dashboard-grid mt-6">
                    <Card className="alerts-card" style={{ gridColumn: '1 / span 2' }}>
                        <CardHeader className="flex items-center gap-2">
                            <AlertCircle size={20} className="text-danger" />
                            <CardTitle>Critical Inventory Alerts</CardTitle>
                        </CardHeader>
                        <CardContent>
                            {isAlertsLoading ? (
                                <Spinner />
                            ) : alerts?.length === 0 ? (
                                <p className="text-secondary">No low stock alerts.</p>
                            ) : (
                                <div className="alerts-list">
                                    {(alerts as any[])?.map(alert => (
                                        <div key={alert.item_id} className="alert-item">
                                            <div className="alert-info">
                                                <strong>{alert.name}</strong>
                                                <span className="text-secondary text-sm">{alert.category}</span>
                                            </div>
                                            <Badge variant={alert.status === 'out_of_stock' ? 'error' : 'warning'}>
                                                {alert.stock_qty} left
                                            </Badge>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    );
}
