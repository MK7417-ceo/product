/* Typed API client for the SkillForge Part-1 backend.
   Auth: access token in memory + localStorage, refresh-token rotation on 401. */

export interface UserResponse {
  id: string;
  email: string;
  role: string;
  created_at: string;
}

export interface AuthResponse {
  user: UserResponse;
  access_token: string;
  refresh_token: string;
  token_type: string;
}

const ACCESS_KEY = 'sf_access_token';
const REFRESH_KEY = 'sf_refresh_token';

export function getAccessToken(): string | null {
  return localStorage.getItem(ACCESS_KEY);
}

export function getRefreshToken(): string | null {
  return localStorage.getItem(REFRESH_KEY);
}

export function saveTokens(access: string, refresh: string): void {
  localStorage.setItem(ACCESS_KEY, access);
  localStorage.setItem(REFRESH_KEY, refresh);
}

export function clearTokens(): void {
  localStorage.removeItem(ACCESS_KEY);
  localStorage.removeItem(REFRESH_KEY);
}

class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

async function raw(path: string, init: RequestInit, token?: string | null): Promise<Response> {
  const headers: Record<string, string> = { 'Content-Type': 'application/json' };
  const t = token ?? getAccessToken();
  if (t) headers['Authorization'] = `Bearer ${t}`;
  return fetch(path, { ...init, headers: { ...headers, ...(init.headers as Record<string, string>) } });
}

let refreshPromise: Promise<boolean> | null = null;

async function tryRefresh(): Promise<boolean> {
  if (!refreshPromise) {
    refreshPromise = (async () => {
      const rt = getRefreshToken();
      if (!rt) return false;
      const res = await fetch('/api/v1/auth/refresh', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh_token: rt }),
      });
      if (!res.ok) return false;
      const data = (await res.json()) as AuthResponse;
      saveTokens(data.access_token, data.refresh_token);
      return true;
    })().finally(() => {
      refreshPromise = null;
    });
  }
  return refreshPromise;
}

export async function api<T>(path: string, init: RequestInit = {}, retried = false): Promise<T> {
  const res = await raw(path, init);
  if (res.status === 401 && !retried && getRefreshToken()) {
    const ok = await tryRefresh();
    if (ok) return api<T>(path, init, true);
    clearTokens();
    window.location.href = '/login';
    throw new ApiError(401, 'session expired');
  }
  if (res.status === 204) return undefined as T;
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new ApiError(res.status, (data as { detail?: string }).detail ?? `request failed (${res.status})`);
  }
  return data as T;
}

export const authApi = {
  register: (email: string, password: string) =>
    api<AuthResponse>('/api/v1/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    }),
  login: (email: string, password: string) =>
    api<AuthResponse>('/api/v1/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    }),
  logout: () => {
    const rt = getRefreshToken();
    clearTokens();
    if (rt) {
      return api('/api/v1/auth/logout', {
        method: 'POST',
        body: JSON.stringify({ refresh_token: rt }),
      }).catch(() => undefined);
    }
    return Promise.resolve(undefined);
  },
  me: () => api<UserResponse>('/api/v1/auth/me'),
};

export { ApiError };

/* ---------- assessments (F3) ---------- */

export interface PublicQuestion {
  id: string;
  topic: string;
  level: string;
  prompt: string;
  choices: string[];
}

export interface AssessmentStart {
  assessment_id: string;
  topic: string;
  level: string;
  total: number;
  questions: PublicQuestion[];
}

export interface AssessmentResult {
  assessment_id: string;
  correct: number;
  total: number;
  ratio: number;
  per_skill: { skill: string; correct: number; total: number }[];
  gaps: string[];
}

export const assessmentApi = {
  start: (topic: string, level: string, count: number) =>
    api<AssessmentStart>('/api/v1/assessments/start', {
      method: 'POST',
      body: JSON.stringify({ topic, level, count }),
    }),
  submit: (id: string, answers: Record<string, number>) =>
    api<AssessmentResult>(`/api/v1/assessments/${id}/submit`, {
      method: 'POST',
      body: JSON.stringify({ answers }),
    }),
};

/* ---------- roadmaps (F4) + evidence (F5) ---------- */

export interface RoadmapTask {
  id: string;
  title: string;
  description: string;
  why_it_matters: string;
  target_skills: string[];
  prerequisites: string[];
  effort_minutes: number;
  priority: string;
  expected_evidence: string;
  acceptance_criteria: string;
  status: string;
}

export interface Roadmap {
  id: string;
  version: number;
  title: string;
  source: string;
  tasks: RoadmapTask[];
  task_counts: { total: number; pending: number; in_progress: number; completed: number };
}

export interface Evidence {
  id: string;
  task_key: string;
  kind: string;
  content: string;
  feedback: string;
  created_at: string;
}

export const roadmapApi = {
  generate: (gaps: { skill: string; mastery_pct: number }[], title = '') =>
    api<Roadmap>('/api/v1/roadmaps/generate', {
      method: 'POST',
      body: JSON.stringify({ gaps, title }),
    }),
  current: () => api<Roadmap>('/api/v1/roadmaps/current'),
  versions: () =>
    api<{ id: string; version: number; title: string; completed: number; task_total: number }[]>(
      '/api/v1/roadmaps',
    ),
  updateTask: (taskId: string, status: string) =>
    api<RoadmapTask>(`/api/v1/roadmaps/tasks/${taskId}`, {
      method: 'PATCH',
      body: JSON.stringify({ status }),
    }),
  regenerate: (gaps: { skill: string; mastery_pct: number }[]) =>
    api<Roadmap>('/api/v1/roadmaps/regenerate', {
      method: 'POST',
      body: JSON.stringify({ gaps }),
    }),
  submitEvidence: (taskId: string, kind: string, content: string) =>
    api<Evidence>(`/api/v1/roadmaps/tasks/${taskId}/evidence`, {
      method: 'POST',
      body: JSON.stringify({ kind, content }),
    }),
  listEvidence: (taskId: string) => api<Evidence[]>(`/api/v1/roadmaps/tasks/${taskId}/evidence`),
};

export interface DailyQuestion {
  id: string;
  topic: string;
  level: string;
  prompt: string;
  choices: string[];
}

export interface TodayPlan {
  date: string;
  questions: DailyQuestion[];
  tasks: { id: string; title: string; status: string; effort_minutes: number; priority: string }[];
  has_roadmap: boolean;
}

export const practiceApi = {
  daily: () => api<{ date: string; questions: DailyQuestion[] }>('/api/v1/practice/daily'),
  submitDaily: (answers: Record<string, number>) =>
    api<{ date: string; correct: number; total: number }>('/api/v1/practice/daily/submit', {
      method: 'POST',
      body: JSON.stringify({ answers }),
    }),
  today: () => api<TodayPlan>('/api/v1/practice/today'),
};
