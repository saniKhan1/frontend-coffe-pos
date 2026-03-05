import React from 'react';
import { cn } from '../../lib/utils';
import '../../styles/Badge.css';

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
    variant?: 'default' | 'success' | 'warning' | 'error' | 'info';
}

export function Badge({ className, variant = 'default', children, ...props }: BadgeProps) {
    return (
        <span className={cn('ui-badge', `ui-badge--${variant}`, className)} {...props}>
            {children}
        </span>
    );
}
