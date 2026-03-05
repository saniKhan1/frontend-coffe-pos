import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { OrderStatusBadge } from '../src/components/ui/OrderStatusBadge';
import React from 'react';

// Using the Badge component as a simple UI state test
// In a full environment we would render the whole Orders page with mocked react-query
describe('Order Status Operational UI Behavior', () => {
    it('renders correct badge styling based on status', () => {
        const { container, rerender } = render(<OrderStatusBadge status="pending" />);

        let badge = container.querySelector('.ui-badge');
        expect(badge).toHaveTextContent('pending');
        expect(badge).toHaveClass('ui-badge--default');

        // Simulate an status transition to preparing
        rerender(<OrderStatusBadge status="preparing" />);
        badge = container.querySelector('.ui-badge');
        expect(badge).toHaveTextContent('preparing');
        expect(badge).toHaveClass('ui-badge--warning');

        // Simulate transition to completed
        rerender(<OrderStatusBadge status="completed" />);
        badge = container.querySelector('.ui-badge');
        expect(badge).toHaveTextContent('completed');
        expect(badge).toHaveClass('ui-badge--success');
    });
});
