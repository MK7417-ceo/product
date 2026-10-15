import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../../lib/auth';
import TopNav from './TopNav';
import Sidebar from './Sidebar';
import BottomNav from './BottomNav';
import Guide from '../Guide/Guide';

/* Protected route: boots unauthenticated users to /login. */
export function RequireAuth({ children }: { children: React.ReactElement }) {
  const { user, loading } = useAuth();
  if (loading) return <div className="route-loading">Loading…</div>;
  if (!user) return <Navigate to="/login" replace />;
  return children;
}

/* App shell: TopNav + grouped sidebar + routed content + mobile bottom nav. */
export default function AppShell() {
  return (
    <>
      <TopNav />
      <div className="app">
        <Sidebar />
        <main className="content">
          <Outlet />
        </main>
      </div>
      <BottomNav />
      <Guide />
    </>
  );
}
