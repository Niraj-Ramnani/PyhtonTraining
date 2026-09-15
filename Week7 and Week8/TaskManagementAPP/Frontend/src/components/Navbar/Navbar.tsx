import type { User } from '../../types/types';
import './Navbar.css';

interface NavbarProps {
  user: User;
  onLogout: () => void;
}

function Navbar({ user, onLogout }: NavbarProps) {
  return (
    <nav className="navbar">
      <div className="navbar__brand">
        <span className="navbar__icon">✅</span>
        <span className="navbar__title">TaskManager</span>
      </div>
      <div className="navbar__user">
        <span className="navbar__username">Hello, {user.name}</span>
        <button id="logout-btn" className="navbar__logout" onClick={onLogout}>
          Logout
        </button>
      </div>
    </nav>
  );
}

export default Navbar;
