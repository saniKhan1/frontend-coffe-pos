import React from 'react';
import { MenuGrid } from '../components/pos/MenuGrid';
import { CartSidebar } from '../components/pos/CartSidebar';
import { CartProvider } from '../context/CartContext';
import { PageHeader } from '../components/layout/PageHeader';

export default function Register() {
    return (
        <CartProvider>
            <div className="register-page animate-fade-in flex flex-col h-full">
                <PageHeader
                    title="Point of Sale"
                    description="Create and take new orders."
                />

                <div className="pos-layout grid h-full" style={{ gridTemplateColumns: 'minmax(0, 1fr) 350px', flex: 1, overflow: 'hidden' }}>
                    <div className="menu-area h-full overflow-hidden">
                        <MenuGrid />
                    </div>

                    <div className="cart-area h-full">
                        <CartSidebar />
                    </div>
                </div>
            </div>
        </CartProvider>
    );
}
