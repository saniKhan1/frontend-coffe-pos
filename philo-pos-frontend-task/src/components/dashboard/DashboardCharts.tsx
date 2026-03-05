import React from 'react';
import {
    LineChart, Line,
    BarChart, Bar,
    PieChart, Pie, Cell,
    XAxis, YAxis, CartesianGrid, Tooltip,
    ResponsiveContainer, Legend,
    RadarChart, PolarGrid, PolarAngleAxis, Radar,
} from 'recharts';
import { formatCurrency } from '../../lib/utils';
import {
    useOrderTrends, useTopItems, usePaymentBreakdown,
    useHourlyHeatmap, useTopCategories, useRevenue,
} from '../../hooks/useDashboard';
import { useDateFilter } from '../../context/DateFilterContext';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/Card';
import { Spinner } from '../ui/Spinner';

const COLORS = ['#c2410c', '#4f46e5', '#10b981', '#f59e0b', '#8b5cf6', '#06b6d4'];

// Recharts calls tickFormatter with raw data values - handle non-date strings safely
function formatAxisDate(val: string): string {
    if (!val || typeof val !== 'string') return String(val ?? '');
    const d = new Date(val);
    if (isNaN(d.getTime())) return val;
    return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}

const tooltipStyle = {
    background: 'var(--bg-secondary)',
    border: '1px solid var(--border-color)',
    borderRadius: '8px',
};

export function DashboardCharts() {
    const { startDate, endDate } = useDateFilter();

    // All 6 real API calls
    // order-trends: [{date, order_count, revenue, ...}]
    const { data: orderTrends, isLoading: loadingTrends } = useOrderTrends({ startDate, endDate });
    // revenue: [{period, revenue, order_count, avg_order_value}]
    const { data: revenue, isLoading: loadingRevenue } = useRevenue({ startDate, endDate });
    // top-items: [{name, qty_sold, revenue, ...}]
    const { data: topItems, isLoading: loadingItems } = useTopItems({ startDate, endDate });
    // payment-breakdown: [{method, count, total_amount, percentage}]
    const { data: payments, isLoading: loadingPayments } = usePaymentBreakdown({ startDate, endDate });
    // hourly-heatmap: [{hour, order_count, revenue, ...}]
    const { data: heatmap, isLoading: loadingHeatmap } = useHourlyHeatmap({ startDate, endDate });
    // top-categories: [{name, total_revenue, order_count, qty_sold}]
    const { data: topCategories, isLoading: loadingCategories } = useTopCategories({ startDate, endDate });

    return (
        <>
            {/* Row 1: Revenue (period + revenue) | Order Trends (date + order_count) */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '20px' }}>
                <Card className="chart-card glass-panel">
                    <CardHeader><CardTitle>Revenue Over Time</CardTitle></CardHeader>
                    <CardContent>
                        <div style={{ height: '270px' }}>
                            {loadingRevenue ? <Spinner fullScreen /> : (
                                <ResponsiveContainer width="100%" height="100%">
                                    <LineChart data={revenue} margin={{ top: 5, right: 20, bottom: 5, left: 10 }}>
                                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--border-color)" />
                                        <XAxis dataKey="period" tickFormatter={formatAxisDate} tick={{ fill: 'var(--text-secondary)', fontSize: 11 }} />
                                        <YAxis tickFormatter={(v) => `$${v}`} tick={{ fill: 'var(--text-secondary)', fontSize: 11 }} />
                                        <Tooltip
                                            formatter={(v: number) => [formatCurrency(v), 'Revenue']}
                                            labelFormatter={formatAxisDate}
                                            contentStyle={tooltipStyle}
                                        />
                                        <Line type="monotone" dataKey="revenue" stroke="var(--brand-primary)" strokeWidth={3} dot={{ r: 2 }} activeDot={{ r: 6 }} />
                                    </LineChart>
                                </ResponsiveContainer>
                            )}
                        </div>
                    </CardContent>
                </Card>

                <Card className="chart-card glass-panel">
                    <CardHeader><CardTitle>Daily Order Trends</CardTitle></CardHeader>
                    <CardContent>
                        <div style={{ height: '270px' }}>
                            {loadingTrends ? <Spinner fullScreen /> : (
                                <ResponsiveContainer width="100%" height="100%">
                                    <BarChart data={orderTrends} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
                                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--border-color)" />
                                        {/* order-trends uses "date" not "period" */}
                                        <XAxis dataKey="date" tickFormatter={formatAxisDate} tick={{ fill: 'var(--text-secondary)', fontSize: 11 }} />
                                        <YAxis tick={{ fill: 'var(--text-secondary)', fontSize: 11 }} />
                                        <Tooltip
                                            formatter={(v: number, name) => [v, name === 'order_count' ? 'Orders' : 'Revenue']}
                                            labelFormatter={formatAxisDate}
                                            contentStyle={tooltipStyle}
                                        />
                                        <Legend formatter={(v) => v === 'order_count' ? 'Orders' : 'Revenue'} />
                                        <Bar dataKey="order_count" fill="#4f46e5" radius={[4, 4, 0, 0]} name="order_count" />
                                    </BarChart>
                                </ResponsiveContainer>
                            )}
                        </div>
                    </CardContent>
                </Card>
            </div>

            {/* Row 2: Top Items (name + qty_sold) | Payment Breakdown (method + count) */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '20px' }}>
                <Card className="chart-card glass-panel">
                    <CardHeader><CardTitle>Top Selling Items</CardTitle></CardHeader>
                    <CardContent>
                        <div style={{ height: '270px' }}>
                            {loadingItems ? <Spinner fullScreen /> : (
                                <ResponsiveContainer width="100%" height="100%">
                                    <BarChart data={topItems} layout="vertical" margin={{ top: 5, right: 30, left: 60, bottom: 5 }}>
                                        <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="var(--border-color)" />
                                        <XAxis type="number" tick={{ fill: 'var(--text-secondary)', fontSize: 11 }} />
                                        <YAxis dataKey="name" type="category" tick={{ fill: 'var(--text-primary)', fontSize: 11 }} width={120} />
                                        <Tooltip formatter={(v: number) => [v, 'Qty Sold']} contentStyle={tooltipStyle} />
                                        <Bar dataKey="qty_sold" fill="var(--brand-primary)" radius={[0, 4, 4, 0]}>
                                            {topItems?.map((_: any, i: number) => (
                                                <Cell key={i} fill={COLORS[i % COLORS.length]} />
                                            ))}
                                        </Bar>
                                    </BarChart>
                                </ResponsiveContainer>
                            )}
                        </div>
                    </CardContent>
                </Card>

                <Card className="chart-card glass-panel">
                    <CardHeader><CardTitle>Payment Methods</CardTitle></CardHeader>
                    <CardContent>
                        <div style={{ height: '270px' }}>
                            {loadingPayments ? <Spinner fullScreen /> : (
                                <ResponsiveContainer width="100%" height="100%">
                                    <PieChart>
                                        {/* payment uses "method" as name key and "count" as value */}
                                        <Pie
                                            data={payments}
                                            cx="50%" cy="50%"
                                            innerRadius={60} outerRadius={95}
                                            paddingAngle={5}
                                            dataKey="count"
                                            nameKey="method"
                                            label={({ method, percentage }: any) => `${method} ${percentage}%`}
                                        >
                                            {payments?.map((_: any, i: number) => (
                                                <Cell key={i} fill={COLORS[i % COLORS.length]} />
                                            ))}
                                        </Pie>
                                        <Tooltip
                                            formatter={(v: number, name: string, props: any) => [
                                                `${v} orders • ${formatCurrency(props.payload.total_amount)}`,
                                                (name || '').charAt(0).toUpperCase() + (name || '').slice(1)
                                            ]}
                                            contentStyle={tooltipStyle}
                                        />
                                    </PieChart>
                                </ResponsiveContainer>
                            )}
                        </div>
                    </CardContent>
                </Card>
            </div>

            {/* Row 3: Hourly Heatmap (hour + order_count) | Top Categories (name + total_revenue) */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '20px' }}>
                <Card className="chart-card glass-panel">
                    <CardHeader><CardTitle>Hourly Order Heatmap</CardTitle></CardHeader>
                    <CardContent>
                        <div style={{ height: '260px' }}>
                            {loadingHeatmap ? <Spinner fullScreen /> : (
                                <ResponsiveContainer width="100%" height="100%">
                                    <BarChart data={heatmap} margin={{ top: 5, right: 10, left: 0, bottom: 5 }}>
                                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--border-color)" />
                                        <XAxis dataKey="hour" tickFormatter={(v) => `${v}h`} tick={{ fill: 'var(--text-secondary)', fontSize: 10 }} />
                                        <YAxis tick={{ fill: 'var(--text-secondary)', fontSize: 11 }} />
                                        <Tooltip
                                            formatter={(v: number) => [v, 'Orders']}
                                            labelFormatter={(l) => `${l}:00 – ${l}:59`}
                                            contentStyle={tooltipStyle}
                                        />
                                        <Bar dataKey="order_count" radius={[4, 4, 0, 0]}>
                                            {heatmap?.map((entry: any, i: number) => {
                                                const max = Math.max(...(heatmap?.map((h: any) => h.order_count) || [1]));
                                                const opacity = entry.order_count === 0 ? 0.1 : 0.25 + (entry.order_count / max) * 0.75;
                                                return <Cell key={i} fill={`rgba(6,182,212,${opacity})`} />;
                                            })}
                                        </Bar>
                                    </BarChart>
                                </ResponsiveContainer>
                            )}
                        </div>
                    </CardContent>
                </Card>

                <Card className="chart-card glass-panel">
                    <CardHeader><CardTitle>Revenue by Category</CardTitle></CardHeader>
                    <CardContent>
                        <div style={{ height: '260px' }}>
                            {loadingCategories ? <Spinner fullScreen /> : (
                                <ResponsiveContainer width="100%" height="100%">
                                    {/* top-categories uses "total_revenue" not "revenue" */}
                                    <RadarChart data={topCategories} margin={{ top: 10, right: 30, left: 30, bottom: 10 }}>
                                        <PolarGrid stroke="var(--border-color)" />
                                        <PolarAngleAxis dataKey="name" tick={{ fill: 'var(--text-secondary)', fontSize: 11 }} />
                                        <Radar name="Revenue" dataKey="total_revenue" stroke="var(--brand-primary)" fill="var(--brand-primary)" fillOpacity={0.35} />
                                        <Tooltip formatter={(v: number) => [formatCurrency(v), 'Revenue']} contentStyle={tooltipStyle} />
                                    </RadarChart>
                                </ResponsiveContainer>
                            )}
                        </div>
                    </CardContent>
                </Card>
            </div>
        </>
    );
}
