import { Navigate } from 'react-router-dom';
import type { User } from '../../types/types';

interface ProtectedRouteProps {
  user: User | null;
  loading: boolean;
  children: React.ReactNode;
}

function ProtectedRoute({ user, loading, children }: ProtectedRouteProps) {
  if (loading) {
    return (
      <div className="loading-screen">
        <div className="spinner" />
      </div>
    );
  }
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  return <>{children}</>;
}

export default ProtectedRoute;
