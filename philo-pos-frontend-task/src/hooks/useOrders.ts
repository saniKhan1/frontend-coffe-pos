import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient, Order, PaginatedResponse } from '../lib/api';

export interface OrderFilters {
    page: number;
    per_page: number;
    status?: string;
    start_date?: string;
    end_date?: string;
}

export function useOrders(filters: OrderFilters) {
    return useQuery({
        queryKey: ['orders', filters],
        queryFn: async () => {
            const params = new URLSearchParams();
            params.append('page', filters.page.toString());
            params.append('per_page', filters.per_page.toString());

            if (filters.status && filters.status !== 'all') params.append('status', filters.status);
            if (filters.start_date) params.append('start_date', filters.start_date);
            if (filters.end_date) params.append('end_date', filters.end_date);

            const { data } = await apiClient.get<PaginatedResponse<Order>>('/orders', {
                params
            });
            return data;
        }
    });
}

export function useOrder(id: number | null) {
    return useQuery({
        queryKey: ['order', id],
        queryFn: async () => {
            if (!id) return null;
            const { data } = await apiClient.get<Order>(`/orders/${id}`);
            return data;
        },
        enabled: !!id,
    });
}

export function useUpdateOrderStatus() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async ({ id, status }: { id: number, status: Order['status'] }) => {
            const { data } = await apiClient.patch<Order>(`/orders/${id}/status`, { status });
            return data;
        },
        onSuccess: (data) => {
            queryClient.invalidateQueries({ queryKey: ['orders'] });
            queryClient.invalidateQueries({ queryKey: ['order', data.id] });
            // Invalidate dashboard stats since orders changed
            queryClient.invalidateQueries({ queryKey: ['dashboard'] });
        }
    });
}
