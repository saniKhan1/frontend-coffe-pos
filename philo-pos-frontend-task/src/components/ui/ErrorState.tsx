import React from 'react';
import { AlertTriangle, RefreshCcw } from 'lucide-react';
import '../../styles/ErrorState.css';

interface ErrorStateProps {
    message?: string;
    onRetry?: () => void;
}

export function ErrorState({ message = 'An error occurred while fetching data.', onRetry }: ErrorStateProps) {
    return (
        <div className="error-state">
            <div className="error-icon-wrapper">
                <AlertTriangle size={32} />
            </div>
            <h3>Something went wrong</h3>
            <p>{message}</p>
            {onRetry && (
                <button className="retry-btn" onClick={onRetry}>
                    <RefreshCcw size={16} />
                    Try Again
                </button>
            )}
        </div>
    );
}
