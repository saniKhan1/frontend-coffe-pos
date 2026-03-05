import React from 'react';
import { cn } from '../../lib/utils';
import '../../styles/Button.css';
import { Loader2 } from 'lucide-react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
    size?: 'sm' | 'md' | 'lg';
    isLoading?: boolean;
}

export function Button({
    className,
    variant = 'primary',
    size = 'md',
    isLoading = false,
    children,
    disabled,
    ...props
}: ButtonProps) {
    return (
        <button
            className={cn(
                'ui-button',
                `ui-button--${variant}`,
                `ui-button--${size}`,
                isLoading && 'ui-button--loading',
                className
            )}
            disabled={disabled || isLoading}
            {...props}
        >
            {isLoading && <Loader2 className="animate-spin" size={16} />}
            <span className={isLoading ? 'opacity-0' : ''}>{children}</span>
        </button>
    );
}
