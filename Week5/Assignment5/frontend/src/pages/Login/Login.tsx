import { Link } from "react-router-dom";
import { useLogin } from "./useLogin";
import "./Login.css";

export default function Login() {
  const { email, setEmail, password, setPassword, error, loading, handleSubmit } = useLogin();

  return (
    <div className="page login-page">
      <form className="card login-form" onSubmit={handleSubmit}>
        <h2>Login</h2>
        <label>Email</label>
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        <label>Password</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        {error && <p className="error-text">{error}</p>}
        <button className="btn" type="submit" disabled={loading}>
          {loading ? "Logging in..." : "Login"}
        </button>
        <p className="login-switch">
          No account? <Link to="/register">Register</Link>
        </p>
      </form>
    </div>
  );
}
