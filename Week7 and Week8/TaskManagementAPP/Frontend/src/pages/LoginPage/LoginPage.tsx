import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import type { useAuth } from '../../hooks/useAuth';
import './LoginPage.css';

interface LoginPageProps {
  onLogin: ReturnType<typeof useAuth>['login'];
}

function LoginPage({ onLogin }: LoginPageProps) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await onLogin({ username, password });
      navigate('/');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-card__logo">✅</div>
        <h1 className="auth-card__heading">Welcome back</h1>
        <p className="auth-card__sub">Sign in to manage your tasks</p>

        {error && <div className="auth-card__error">{error}</div>}

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="auth-form__field">
            <label htmlFor="login-username" className="auth-form__label">Username</label>
            <input
              id="login-username"
              type="text"
              className="auth-form__input"
              placeholder="Enter your username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              autoFocus
            />
          </div>

          <div className="auth-form__field">
            <label htmlFor="login-password" className="auth-form__label">Password</label>
            <input
              id="login-password"
              type="password"
              className="auth-form__input"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button
            id="login-submit-btn"
            type="submit"
            className="auth-form__submit"
            disabled={loading}
          >
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <p className="auth-card__footer">
          Don't have an account?{' '}
          <Link to="/register" className="auth-card__link">Create one</Link>
        </p>
      </div>
    </div>
  );
}

export default LoginPage;
