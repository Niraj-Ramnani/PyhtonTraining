import { useState, useEffect, useCallback } from 'react';
import type { User, LoginRequest, RegisterRequest } from '../types/types';
import { loginUser, registerUser, getCurrentUser } from '../services/api';

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // On mount, try to restore the user from the stored token
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      setLoading(false);
      return;
    }
    getCurrentUser()
      .then(setUser)
      .catch(() => {
        localStorage.removeItem('token');
      })
      .finally(() => setLoading(false));
  }, []);

  const login = useCallback(async (data: LoginRequest) => {
    setError(null);
    try {
      const { token } = await loginUser(data);
      localStorage.setItem('token', token);
      const currentUser = await getCurrentUser();
      setUser(currentUser);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Login failed';
      setError(message);
      throw err;
    }
  }, []);

  const register = useCallback(async (data: RegisterRequest) => {
    setError(null);
    try {
      await registerUser(data);
      // After register, log them in automatically
      await login({ username: data.username, password: data.password });
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Registration failed';
      setError(message);
      throw err;
    }
  }, [login]);

  const logout = useCallback(() => {
    localStorage.removeItem('token');
    setUser(null);
  }, []);

  return { user, loading, error, login, register, logout };
}
