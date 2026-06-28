import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Compass, User, LogOut, History } from 'lucide-react';

export const Navbar: React.FC = () => {
  const { logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  // Hide navbar completely on the landing page
  if (location.pathname === '/') return null;

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const isActive = (path: string) => location.pathname === path ? 'active' : '';

  return (
    <nav className="navbar">
      <div className="navbar-content">
        <Link to="/" className="flex items-center gap-2" style={{ color: 'var(--primary)', fontWeight: 700, fontSize: '1.25rem' }}>
          <Compass size={24} />
          <span>CareerAI</span>
        </Link>
        
        <div className="nav-links">
          {isAuthenticated ? (
            <>
              <Link to="/dashboard" className={`nav-link flex items-center gap-2 ${isActive('/dashboard')}`}>
                <User size={18} /> Dashboard
              </Link>
              <Link to="/recommend" className={`nav-link flex items-center gap-2 ${isActive('/recommend')}`}>
                <Compass size={18} /> Discover
              </Link>
              <Link to="/history" className={`nav-link flex items-center gap-2 ${isActive('/history')}`}>
                <History size={18} /> History
              </Link>
              <button onClick={handleLogout} className="btn-secondary flex items-center gap-2" style={{ padding: '0.5rem 1rem' }}>
                <LogOut size={18} /> Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="btn-secondary">Login</Link>
              <Link to="/register" className="btn-primary">Register</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};
