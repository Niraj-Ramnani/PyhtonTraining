import { Link } from "react-router-dom";
import { useNavbar } from "./useNavbar";
import "./Navbar.css";

export default function Navbar() {
  const { user, handleLogout } = useNavbar();

  return (
    <nav className="navbar">
      <Link to="/" className="navbar-brand"> Food Ordering Assignment</Link>
      <div className="navbar-links">
        <Link to="/">Restaurants</Link>
        {user && <Link to="/orders">My Orders</Link>}
        {user && <Link to="/profile">Profile</Link>}
        {user ? (
          <button className="btn btn-secondary" onClick={handleLogout}>Logout</button>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        )}
      </div>
    </nav>
  );
}
