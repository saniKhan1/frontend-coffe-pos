import React from 'react';
import { Loader2 } from 'lucide-react';

interface SpinnerProps {
    size?: number;
    className?: string;
    fullScreen?: boolean;
}

export function Spinner({ size = 24, className = '', fullScreen = false }: SpinnerProps) {
    const spinner = (
        <Loader2
            size={size}
            className={`animate-spin ${className}`}
            style={{ color: 'var(--brand-primary)', animation: 'spin 1s linear infinite' }}
        />
    );

    if (fullScreen) {
        return (
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%', width: '100%', minHeight: '300px' }}>
                {spinner}
            </div>
        );
    }

    return spinner;
}
