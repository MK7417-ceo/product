import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import './styles/theme.css';
import { AuthProvider, useAuth } from './lib/auth';
import Shell from './components/Shell';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Assessment from './pages/Assessment';
import RoadmapPage from './pages/Roadmap';
import Practice from './pages/Practice';
import Code from './pages/Code';
import Resume from './pages/Resume';
import Certificates from './pages/Certificates';
import PortfolioPage from './pages/Portfolio';
import Interview from './pages/Interview';
import English from './pages/English';
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
            <Route path="assessment" element={<Assessment />} />
            <Route path="roadmap" element={<RoadmapPage />} />
            <Route path="practice" element={<Practice />} />
            <Route path="code" element={<Code />} />
            <Route path="resume" element={<Resume />} />
            <Route path="certificates" element={<Certificates />} />
            <Route path="portfolio" element={<PortfolioPage />} />
            <Route path="interview" element={<Interview />} />
            <Route path="english" element={<English />} />
          </Route>
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  </StrictMode>,
);
