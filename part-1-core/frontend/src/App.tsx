import { Suspense, lazy } from 'react';
import { Navigate, Route, Routes } from 'react-router-dom';
import { useAuth } from './lib/auth';
import AppShell, { RequireAuth } from './components/layout/AppShell';

const Login = lazy(() => import('./pages/Login'));
const Register = lazy(() => import('./pages/Register'));
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Welcome = lazy(() => import('./pages/onboarding/Welcome'));
const Resume = lazy(() => import('./pages/onboarding/Resume'));
const Subscription = lazy(() => import('./pages/onboarding/Subscription'));
const MakePlan = lazy(() => import('./pages/onboarding/MakePlan'));
const Verification = lazy(() => import('./pages/onboarding/Verification'));
const CodeLab = lazy(() => import('./pages/CodeLab'));
const Roadmap = lazy(() => import('./pages/Roadmap'));
const Practice = lazy(() => import('./pages/Practice'));
const SkillProfile = lazy(() => import('./pages/SkillProfile'));
const SkillGaps = lazy(() => import('./pages/SkillGaps'));
const Evidence = lazy(() => import('./pages/Evidence'));
const Certificates = lazy(() => import('./pages/Certificates'));
const Portfolio = lazy(() => import('./pages/Portfolio'));
const InterviewPrep = lazy(() => import('./pages/InterviewPrep'));
const English = lazy(() => import('./pages/English'));
const Settings = lazy(() => import('./pages/Settings'));
const Profile = lazy(() => import('./pages/Profile'));
const Billing = lazy(() => import('./pages/Billing'));

function Fallback() {
  return <div className="route-loading">Loading…</div>;
}

/* Public routes: signed-in users go straight to the app. */
function PublicOnly({ children }: { children: React.ReactElement }) {
  const { user, loading } = useAuth();
  if (loading) return <Fallback />;
  if (user) return <Navigate to="/" replace />;
  return children;
}

export default function App() {
  return (
    <Suspense fallback={<Fallback />}>
      <Routes>
        <Route
          path="/login"
          element={
            <PublicOnly>
              <Login />
            </PublicOnly>
          }
        />
        <Route
          path="/register"
          element={
            <PublicOnly>
              <Register />
            </PublicOnly>
          }
        />
        <Route
          path="/"
          element={
            <RequireAuth>
              <AppShell />
            </RequireAuth>
          }
        >
          <Route index element={<Dashboard />} />
          <Route path="welcome" element={<Welcome />} />
          <Route path="resume" element={<Resume />} />
          <Route path="subscription" element={<Subscription />} />
          <Route path="plan" element={<MakePlan />} />
          <Route path="verification" element={<Verification />} />
          <Route path="assessment" element={<Navigate to="/plan" replace />} />
          <Route path="roadmap" element={<Roadmap />} />
          <Route path="practice" element={<Practice />} />
          <Route path="codelab" element={<CodeLab />} />
          <Route path="skills" element={<SkillProfile />} />
          <Route path="gaps" element={<SkillGaps />} />
          <Route path="evidence" element={<Evidence />} />
          <Route path="certificates" element={<Certificates />} />
          <Route path="portfolio" element={<Portfolio />} />
          <Route path="interview" element={<InterviewPrep />} />
          <Route path="english" element={<English />} />
          <Route path="settings" element={<Settings />} />
          <Route path="profile" element={<Profile />} />
          <Route path="billing" element={<Billing />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Suspense>
  );
}
