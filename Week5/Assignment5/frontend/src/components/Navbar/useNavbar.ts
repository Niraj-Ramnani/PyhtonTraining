import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

export function useNavbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return { user, handleLogout };
}
