import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || "https://philo-coffee-shop-production-dd93.up.railway.app/api/v1";

export const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export interface Category {
    id: number;
    name: string;
    description: string | null;
    display_order: number;
    is_active: boolean;
}

export interface MenuItem {
    id: number;
    category_id: number;
    category_name: string;
    name: string;
    description: string | null;
    price: number;
    image_url: string | null;
    is_available: boolean;
    stock_qty: number;
}

export interface Addon {
    id: number;
    name: string;
    price: number;
    is_available: boolean;
}

export interface Customer {
    id: number;
    name: string;
    phone: string;
    email: string;
    total_orders: number;
    total_spent: number;
}

export interface Discount {
    id: number;
    name: string;
    type: 'percentage' | 'flat';
    value: number;
    is_active: boolean;
}

export interface OrderItemAddon {
    id: number;
    addon_id: number;
    addon_name: string;
    price: number;
}

export interface OrderItem {
    id: number;
    item_id: number;
    item_name: string;
    quantity: number;
    unit_price: number;
    subtotal: number;
    addons: OrderItemAddon[];
}

export interface Order {
    id: number;
    order_number: string;
    customer_id: number | null;
    customer_name: string | null;
    status: 'pending' | 'preparing' | 'ready' | 'completed' | 'cancelled';
    payment_method: 'cash' | 'card' | 'mobile';
    subtotal: number;
    tax_amount: number;
    discount_amount: number;
    discount_id: number | null;
    total: number;
    shift_id: number | null;
    notes: string | null;
    items: OrderItem[];
    created_at: string;
    updated_at: string;
}

export interface KPISummary {
    total_revenue: number;
    total_orders: number;
    completed_orders: number;
    cancelled_orders: number;
    avg_order_value: number;
    total_customers: number;
    new_customers: number;
    total_items_sold: number;
    revenue_change_pct: number;
    order_change_pct: number;
    top_payment_method: string;
    busiest_hour: number;
}

export interface PaginatedResponse<T> {
    items: T[];
    total: number;
    page: number;
    per_page: number;
    total_pages: number;
}
