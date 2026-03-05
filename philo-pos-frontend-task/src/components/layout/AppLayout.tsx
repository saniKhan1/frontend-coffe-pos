import React from 'react';
import { Sidebar } from './Sidebar';

interface AppLayoutProps {
    children: React.ReactNode;
}

export function AppLayout({ children }: AppLayoutProps) {
    return (
        <div className="app-layout animate-fade-in">
            <Sidebar />
            <main className="main-content">
                {children}
            </main>
        </div>
    );
}
