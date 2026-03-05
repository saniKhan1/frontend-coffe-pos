import { NavLink } from 'react-router-dom';
import { LayoutDashboard, ShoppingBag, Coffee } from 'lucide-react';
import '../../styles/Sidebar.css';

const navItems = [
    { path: '/', label: 'Dashboard', icon: LayoutDashboard, exact: true },
    { path: '/orders', label: 'Orders', icon: ShoppingBag, exact: false },
    { path: '/register', label: 'Register (POS)', icon: Coffee, exact: false },
];

export function Sidebar() {
    return (
        <aside className="sidebar">
            <div className="sidebar-header">
                <div className="logo-icon">☕</div>
                <h2>Philo POS</h2>
            </div>

            <nav className="sidebar-nav">
                {navItems.map((item) => {
                    const Icon = item.icon;
                    return (
                        <NavLink
                            key={item.path}
                            to={item.path}
                            end={item.exact}
                            className={({ isActive }) => `nav-item${isActive ? ' active' : ''}`}
                        >
                            <Icon size={20} />
                            <span>{item.label}</span>
                        </NavLink>
                    );
                })}
            </nav>

            <div className="sidebar-footer">
                <div className="system-status">
                    <span className="status-dot" style={{
                        display: 'inline-block',
                        width: 8,
                        height: 8,
                        borderRadius: '50%',
                        background: 'var(--success)',
                        marginRight: 6
                    }} />
                    <span>System Online</span>
                </div>
            </div>
        </aside>
    );
}
