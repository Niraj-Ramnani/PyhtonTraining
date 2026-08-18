import { Link } from "react-router-dom";
import { useRegister } from "./useRegister";
import "./Register.css";

export default function Register() {
  const {
    name, setName, email, setEmail, password, setPassword, phone, setPhone,
    error, success, loading, handleSubmit,
  } = useRegister();

  return (
    <div className="page register-page">
      <form className="card register-form" onSubmit={handleSubmit}>
        <h2>Create Account</h2>
        <label>Name</label>
        <input value={name} onChange={(e) => setName(e.target.value)} required />
        <label>Email</label>
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        <label>Phone</label>
        <input value={phone} onChange={(e) => setPhone(e.target.value)} />
        <label>Password</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required minLength={6} />
        {error && <p className="error-text">{error}</p>}
        {success && <p className="success-text">Account created! Redirecting to login...</p>}
        <button className="btn" type="submit" disabled={loading}>
          {loading ? "Creating..." : "Register"}
        </button>
        <p className="register-switch">
          Already have an account? <Link to="/login">Login</Link>
        </p>
      </form>
    </div>
  );
}
