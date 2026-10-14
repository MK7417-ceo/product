import { useCallback, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../lib/auth';
import {
  dashboardApi,
  type AssessmentSummary,
  type PlacementTopicsOut,
  type ProfileOut,
  type RoadmapOut,
  type TodayOut,
} from '../lib/api-dashboard';
import HeroCard from '../components/dashboard/HeroCard';
import StatCards, { topActionableTask } from '../components/dashboard/StatCards';
import ContinueCard from '../components/dashboard/ContinueCard';
import WeekStrip from '../components/dashboard/WeekStrip';
import TodayRail from '../components/dashboard/TodayRail';
import '../components/dashboard/dashboard.css';
import RightSidebar from '../components/RightSidebar';

interface Source<T> {
  data: T;
  loading: boolean;
  error: string | null;
}

const init = <T,>(data: T): Source<T> => ({ data, loading: true, error: null });

function greetingFor(hour: number): string {
  if (hour < 12) return 'Good morning';
  if (hour < 17) return 'Good afternoon';
  return 'Good evening';
}

/** "aarav.sharma" → "Aarav". Falls back to the full local part. */
function displayName(email: string | undefined): string {
  if (!email) return 'there';
  const local = email.split('@')[0];
  const first = local.split(/[._-]+/)[0];
  return first ? first.charAt(0).toUpperCase() + first.slice(1) : local;
}

export default function Dashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();

  const [roadmap, setRoadmap] = useState<Source<RoadmapOut | null>>(init(null));
  const [today, setToday] = useState<Source<TodayOut | null>>(init(null));
  const [assessments, setAssessments] = useState<Source<AssessmentSummary[]>>(init([]));
  const [profile, setProfile] = useState<Source<ProfileOut | null>>(init(null));
  const [topics, setTopics] = useState<Source<PlacementTopicsOut | null>>(init(null));

  const load = useCallback(async () => {
    setRoadmap((s) => ({ ...s, loading: true, error: null }));
    setToday((s) => ({ ...s, loading: true, error: null }));
    setAssessments((s) => ({ ...s, loading: true, error: null }));
    setProfile((s) => ({ ...s, loading: true, error: null }));
    setTopics((s) => ({ ...s, loading: true, error: null }));

    const [r, t, a, p, tp] = await Promise.allSettled([
      dashboardApi.getRoadmap(),
      dashboardApi.getToday(),
      dashboardApi.getAssessments(),
      dashboardApi.getProfile(),
      dashboardApi.getPlacementTopics(),
    ]);

    const label = (e: unknown) =>
      e instanceof Error ? e.message : 'Request failed';

    setRoadmap(
      r.status === 'fulfilled'
        ? { data: r.value, loading: false, error: null }
        : { data: null, loading: false, error: label(r.reason) },
    );
    setToday(
      t.status === 'fulfilled'
        ? { data: t.value, loading: false, error: null }
        : { data: null, loading: false, error: label(t.reason) },
    );
    setAssessments(
      a.status === 'fulfilled'
        ? { data: a.value, loading: false, error: null }
        : { data: [], loading: false, error: label(a.reason) },
    );
    setProfile(
      p.status === 'fulfilled'
        ? { data: p.value, loading: false, error: null }
        : { data: null, loading: false, error: label(p.reason) },
    );
    setTopics(
      tp.status === 'fulfilled'
        ? { data: tp.value, loading: false, error: null }
        : { data: null, loading: false, error: label(tp.reason) },
    );
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  const diagnosticName =
    topics.data?.topics?.[0] ? `${topics.data.topics[0]} diagnostic` : 'the diagnostic';

  /* ---- next best action, derived from real state ---- */
  const openTask = roadmap.data ? topActionableTask(roadmap.data) : null;
  let nba: React.ReactNode;
  let nbaTo = '/plan';
  if (openTask) {
    nba = (
      <>
        continue <strong>{openTask.title}</strong> to close your top skill gap.
      </>
    );
    nbaTo = '/roadmap';
  } else if (roadmap.data) {
    nba = (
      <>
        your roadmap is complete — <strong>take today&apos;s practice</strong> to stay sharp.
      </>
    );
    nbaTo = '/practice';
  } else if (profile.data || assessments.data.length > 0) {
    nba = (
      <>
        <strong>generate your roadmap</strong> from your skill gaps.
      </>
    );
    nbaTo = '/roadmap';
  } else {
    nba = (
      <>
        complete <strong>{diagnosticName}</strong> to unlock your roadmap.
      </>
    );
  }

  return (
    <div className="sf-dash">
      <div className="sf-greet">
        <h1>
          {greetingFor(new Date().getHours())}, {displayName(user?.email)}
        </h1>
        <p className="sf-nba">
          Your next best step:{' '}
          <button
            type="button"
            onClick={() => navigate(nbaTo)}
            style={{
              background: 'none',
              border: 'none',
              padding: 0,
              cursor: 'pointer',
              font: 'inherit',
              color: 'var(--cyan, #36c5f0)',
              fontWeight: 600,
            }}
            aria-label="Go to your next best step"
          >
            {nba}
          </button>
        </p>
      </div>

      <div className="sf-dashboard-with-sidebar">
        <div className="sf-dashboard-main">
          <HeroCard
            profile={profile.data}
            assessments={assessments.data}
            roadmap={roadmap.data}
            loading={roadmap.loading || profile.loading || assessments.loading}
            error={roadmap.error ?? profile.error ?? assessments.error}
            onRetry={load}
          />

          <StatCards
            roadmap={roadmap.data}
            assessments={assessments.data}
            today={today.data}
            loading={roadmap.loading || assessments.loading || today.loading}
          />

          <div className="sf-body">
            <div className="sf-main-col">
              <ContinueCard
                roadmap={roadmap.data}
                loading={roadmap.loading}
                error={roadmap.error}
                onRetry={load}
              />
              <div style={{ marginTop: 14 }}>
                <WeekStrip today={today.data} loading={today.loading} error={today.error} onRetry={load} />
              </div>
            </div>
            <TodayRail today={today.data} loading={today.loading} error={today.error} onRetry={load} />
          </div>
        </div>
        <RightSidebar />
      </div>
    </div>
  );
}
