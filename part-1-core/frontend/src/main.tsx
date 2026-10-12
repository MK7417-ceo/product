import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import './styles/theme.css';
import { AuthProvider, useAuth } from './lib/auth';
import Shell from './components/Shell';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Placeholder from './pages/Placeholder';
import type { JSX } from 'react';

function Guard({ children }: { children: JSX.Element }) {
  const { user, loading } = useAuth();
  if (loading) return <div className="auth-wrap"><p style={{ color: '#8b93a7' }}>Loading…</p></div>;
  if (!user) return <Navigate to="/login" replace />;
  return children;
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route
            path="/"
            element={
              <Guard>
                <Shell />
              </Guard>
            }
          >
            <Route index element={<Dashboard />} />
            <Route path="assessment" element={<Placeholder title="Assessment" note="Take level-matched tests — MCQ, coding, theory." />} />
            <Route path="roadmap" element={<Placeholder title="Roadmap" note="Your personalized learning plan, built from skill gaps." />} />
            <Route path="practice" element={<Placeholder title="Practice" note="Daily questions and weekly mock tests." />} />
            <Route path="code" element={<Placeholder title="Code Runner" note="Write and run code right in the browser." />} />
            <Route path="portfolio" element={<Placeholder title="Portfolio" note="Build and publish your expert portfolio." />} />
          </Route>
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  </StrictMode>,
);
