import { useQuery, useMutation } from '@tanstack/react-query';
import { apiClient, Category, MenuItem, Addon, Customer, Discount, PaginatedResponse } from '../lib/api';

export function useCategories() {
    return useQuery({
        queryKey: ['categories'],
        queryFn: async () => {
            const { data } = await apiClient.get<PaginatedResponse<Category>>('/categories', { params: { per_page: 50, is_active: true } });
            return data.items;
        }
    });
}

export function useMenuItems(categoryId?: number) {
    return useQuery({
        queryKey: ['items', categoryId],
        queryFn: async () => {
            const params = new URLSearchParams({ per_page: '100', is_available: 'true' });
            if (categoryId) params.append('category_id', categoryId.toString());

            const { data } = await apiClient.get<PaginatedResponse<MenuItem>>('/items', { params });
            return data.items;
        }
    });
}

export function useAddons() {
    return useQuery({
        queryKey: ['addons'],
        queryFn: async () => {
            const { data } = await apiClient.get<PaginatedResponse<Addon>>('/addons', { params: { per_page: 50, is_available: true } });
            return data.items;
        }
    });
}

export function useCustomers() {
    return useQuery({
        queryKey: ['customers'],
        queryFn: async () => {
            const { data } = await apiClient.get<PaginatedResponse<Customer>>('/customers');
            return data.items;
        }
    });
}

export function useDiscounts() {
    return useQuery({
        queryKey: ['discounts'],
        queryFn: async () => {
            const { data } = await apiClient.get<PaginatedResponse<Discount>>('/discounts', { params: { is_active: true } });
            return data.items;
        }
    });
}

export interface CreateOrderPayload {
    customer_id?: number | null;
    payment_method: 'cash' | 'card' | 'mobile';
    discount_id?: number | null;
    notes?: string;
    items: {
        item_id: number;
        quantity: number;
        addon_ids: number[];
    }[];
}

export function useCreateOrder() {
    return useMutation({
        mutationFn: async (payload: CreateOrderPayload) => {
            const { data } = await apiClient.post('/orders', payload);
            return data;
        }
    });
}
