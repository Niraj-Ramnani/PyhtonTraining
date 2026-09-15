import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import type { useAuth } from '../../hooks/useAuth';
import '../LoginPage/LoginPage.css';

interface RegisterPageProps {
  onRegister: ReturnType<typeof useAuth>['register'];
}

function RegisterPage({ onRegister }: RegisterPageProps) {
  const [name, setName] = useState('');
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await onRegister({ name, username, email, password });
      navigate('/');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-card__logo">✅</div>
        <h1 className="auth-card__heading">Create account</h1>
        <p className="auth-card__sub">Start managing your tasks today</p>

        {error && <div className="auth-card__error">{error}</div>}

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="auth-form__field">
            <label htmlFor="reg-name" className="auth-form__label">Full Name</label>
            <input
              id="reg-name"
              type="text"
              className="auth-form__input"
              placeholder="Enter your full name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              autoFocus
            />
          </div>

          <div className="auth-form__field">
            <label htmlFor="reg-username" className="auth-form__label">Username</label>
            <input
              id="reg-username"
              type="text"
              className="auth-form__input"
              placeholder="Choose a username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>

          <div className="auth-form__field">
            <label htmlFor="reg-email" className="auth-form__label">Email</label>
            <input
              id="reg-email"
              type="email"
              className="auth-form__input"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="auth-form__field">
            <label htmlFor="reg-password" className="auth-form__label">Password</label>
            <input
              id="reg-password"
              type="password"
              className="auth-form__input"
              placeholder="Create a password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button
            id="register-submit-btn"
            type="submit"
            className="auth-form__submit"
            disabled={loading}
          >
            {loading ? 'Creating account...' : 'Create Account'}
          </button>
        </form>

        <p className="auth-card__footer">
          Already have an account?{' '}
          <Link to="/login" className="auth-card__link">Sign in</Link>
        </p>
      </div>
    </div>
  );
}

export default RegisterPage;
