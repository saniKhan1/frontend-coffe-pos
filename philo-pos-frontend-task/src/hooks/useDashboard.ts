import { useQuery } from '@tanstack/react-query';
import { apiClient, KPISummary } from '../lib/api';

interface DashboardFilters {
    startDate: string;
    endDate: string;
}

// 9.1 Summary KPIs
export function useDashboardSummary({ startDate, endDate }: DashboardFilters) {
    return useQuery({
        queryKey: ['dashboard', 'summary', startDate, endDate],
        queryFn: async () => {
            const { data } = await apiClient.get<KPISummary>('/dashboard/summary', {
                params: { start_date: startDate, end_date: endDate }
            });
            return data;
        }
    });
}

// 9.2 Revenue Breakdown (Order Trends for Chart)
export function useOrderTrends({ startDate, endDate }: DashboardFilters) {
    return useQuery({
        queryKey: ['dashboard', 'order-trends', startDate, endDate],
        queryFn: async () => {
            const { data } = await apiClient.get('/dashboard/order-trends', {
                params: { start_date: startDate, end_date: endDate, group_by: 'daily' }
            });
            return data;
        }
    });
}

// 9.3 Top Selling Items
export function useTopItems({ startDate, endDate }: DashboardFilters) {
    return useQuery({
        queryKey: ['dashboard', 'top-items', startDate, endDate],
        queryFn: async () => {
            const { data } = await apiClient.get('/dashboard/top-items', {
                params: { limit: 5, start_date: startDate, end_date: endDate }
            });
            return data;
        }
    });
}

// 9.6 Hourly Sales Heatmap
export function useHourlyHeatmap({ startDate, endDate }: DashboardFilters) {
    return useQuery({
        queryKey: ['dashboard', 'hourly-heatmap', startDate, endDate],
        queryFn: async () => {
            const { data } = await apiClient.get('/dashboard/hourly-heatmap', {
                params: { start_date: startDate, end_date: endDate }
            });
            return data;
        }
    });
}

// 9.8 Payment Method Breakdown
export function usePaymentBreakdown({ startDate, endDate }: DashboardFilters) {
    return useQuery({
        queryKey: ['dashboard', 'payment-breakdown', startDate, endDate],
        queryFn: async () => {
            const { data } = await apiClient.get('/dashboard/payment-breakdown', {
                params: { start_date: startDate, end_date: endDate }
            });
            return data;
        }
    });
}

// 9.9 Inventory Alerts
export function useInventoryAlerts() {
    return useQuery({
        queryKey: ['dashboard', 'inventory-alerts'],
        queryFn: async () => {
            const { data } = await apiClient.get('/dashboard/inventory-alerts');
            return data;
        }
    });
}

// 9.4 Top Categories
export function useTopCategories({ startDate, endDate }: DashboardFilters) {
    return useQuery({
        queryKey: ['dashboard', 'top-categories', startDate, endDate],
        queryFn: async () => {
            const { data } = await apiClient.get('/dashboard/top-categories', {
                params: { limit: 6, start_date: startDate, end_date: endDate }
            });
            return data;
        }
    });
}

// 9.2 Revenue over time
export function useRevenue({ startDate, endDate }: DashboardFilters) {
    return useQuery({
        queryKey: ['dashboard', 'revenue', startDate, endDate],
        queryFn: async () => {
            const { data } = await apiClient.get('/dashboard/revenue', {
                params: { start_date: startDate, end_date: endDate, group_by: 'daily' }
            });
            return data;
        }
    });
}

// 9.7 Customer Insights
export function useCustomerInsights({ startDate, endDate }: DashboardFilters) {
    return useQuery({
        queryKey: ['dashboard', 'customer-insights', startDate, endDate],
        queryFn: async () => {
            const { data } = await apiClient.get('/dashboard/customer-insights', {
                params: { start_date: startDate, end_date: endDate }
            });
            return data;
        }
    });
}
