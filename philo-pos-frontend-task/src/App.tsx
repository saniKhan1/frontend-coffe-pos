import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { DateFilterProvider } from './context/DateFilterContext';
import { AppLayout } from './components/layout/AppLayout';

import Dashboard from './pages/Dashboard';
import Orders from './pages/Orders';
import Register from './pages/Register';

const queryClient = new QueryClient({
    defaultOptions: {
        queries: {
            refetchOnWindowFocus: false,
            staleTime: 1000 * 60 * 5,
        },
    },
});

function App() {
    return (
        <QueryClientProvider client={queryClient}>
            <DateFilterProvider>
                <BrowserRouter>
                    <AppLayout>
                        <Routes>
                            <Route path="/" element={<Dashboard />} />
                            <Route path="/orders" element={<Orders />} />
                            <Route path="/register" element={<Register />} />
                            <Route path="*" element={<Navigate to="/" replace />} />
                        </Routes>
                    </AppLayout>
                </BrowserRouter>
            </DateFilterProvider>
        </QueryClientProvider>
    );
}

export default App;
