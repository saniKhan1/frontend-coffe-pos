import { Order } from '../lib/api';
import { Badge } from './Badge';

export function OrderStatusBadge({ status }: { status: Order['status'] }) {
    let variant: 'default' | 'success' | 'warning' | 'error' | 'info' = 'default';

    switch (status) {
        case 'pending':
            variant = 'default';
            break;
        case 'preparing':
            variant = 'warning';
            break;
        case 'ready':
            variant = 'info';
            break;
        case 'completed':
            variant = 'success';
            break;
        case 'cancelled':
            variant = 'error';
            break;
    }

    return <Badge variant={variant}>{status}</Badge>;
}
