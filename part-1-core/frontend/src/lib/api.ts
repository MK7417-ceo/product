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

export interface CodeRunResult {
  run_id: string;
  verdict: string;
  stdout: string;
  stderr: string;
  truncated: boolean;
  exit_code: number | null;
  cpu_ms: number | null;
  peak_ram_mb: number | null;
  timed_out: boolean;
}

export interface EngineLanguage {
  id: string;
  compile: string[] | null;
  run: string[];
  available: boolean;
}

export const codeApi = {
  run: (language: string, code: string, stdin: string) =>
    api<CodeRunResult>('/api/v1/code/run', {
      method: 'POST',
      body: JSON.stringify({ language, code, stdin }),
    }),
  languages: () => api<{ languages: EngineLanguage[] }>('/api/v1/code/languages'),
};

export interface ResumeData {
  id: string;
  title: string;
  summary: string;
  skills: string[];
  experience: { title: string; company: string; start: string; end: string; bullets: string[] }[];
  projects: { name: string; description: string; tech: string[]; link: string }[];
  education: { degree: string; school: string; year: string }[];
  links: Record<string, string>;
}

export interface JDMatchResult {
  score: number;
  jd_keyword_count: number;
  matched: { keyword: string; jd_count: number }[];
  missing: { keyword: string; jd_count: number }[];
  suggestions: string[];
}

export const launchpadApi = {
  getResume: () => api<ResumeData>('/api/v1/launchpad/resume'),
  saveResume: (r: Omit<ResumeData, 'id'>) =>
    api<ResumeData>('/api/v1/launchpad/resume', {
      method: 'PUT',
      body: JSON.stringify(r),
    }),
  matchJd: (jd_text: string) =>
    api<JDMatchResult>('/api/v1/launchpad/jd-match', {
      method: 'POST',
      body: JSON.stringify({ jd_text }),
    }),
};

export interface Certificate {
  id: string;
  kind: string;
  title: string;
  ref_id: string;
  verification_code: string;
  issued_at: string;
  detail: string;
}

export const certificatesApi = {
  list: () => api<Certificate[]>('/api/v1/launchpad/certificates'),
  issue: (kind: string, ref_id: string) =>
    api<Certificate>('/api/v1/launchpad/certificates/issue', {
      method: 'POST',
      body: JSON.stringify({ kind, ref_id }),
    }),
  verify: (code: string) =>
    api<{ valid: boolean; title?: string; kind?: string; issued_to?: string; issued_at?: string; detail?: string }>(
      `/api/v1/launchpad/certificates/verify/${code}`,
    ),
};

export interface Portfolio {
  name: string;
  summary: string;
  skills: string[];
  experience: { title: string; company: string; bullets: string[] }[];
  projects: { name: string; description: string; tech: string[] }[];
  education: { degree: string; school: string; year: string }[];
  links: Record<string, string>;
  certificates: { title: string; issued_at: string; detail: string; verification_code: string }[];
  roadmap_title: string;
  roadmap_done: number;
  roadmap_total: number;
  evidence_count: number;
}

export const portfolioApi = {
  get: () => api<Portfolio>('/api/v1/launchpad/portfolio'),
  download: async () => {
    const t = getAccessToken();
    const res = await fetch('/api/v1/launchpad/portfolio/download', {
      headers: t ? { Authorization: `Bearer ${t}` } : {},
    });
    if (!res.ok) throw new ApiError(res.status, 'Download failed');
    const blob = await res.blob();
    const cd = res.headers.get('content-disposition') || '';
    const m = cd.match(/filename="([^"]+)"/);
    return { blob, filename: m ? m[1] : 'portfolio.html' };
  },
};

export interface PrepQuestion {
  id: string;
  topic: string;
  level: string;
  question: string;
  guidance: string[];
  tags: string[];
}

export const prepApi = {
  topics: () => api<{ topics: { topic: string; count: number }[] }>('/api/v1/prep/topics'),
  questions: (topic: string, count = 10) =>
    api<{ questions: PrepQuestion[] }>(
      `/api/v1/prep/questions?topic=${encodeURIComponent(topic)}&count=${count}`,
    ),
};

export interface EnglishQuestion {
  id: string;
  kind: string;
  level: string;
  prompt: string;
  choices: string[];
  passage: string;
}

export const englishApi = {
  daily: () => api<{ date: string; questions: EnglishQuestion[] }>('/api/v1/english/daily'),
  submit: (answers: Record<string, number>) =>
    api<{ date: string; correct: number; total: number }>('/api/v1/english/daily/submit', {
      method: 'POST',
      body: JSON.stringify({ answers }),
    }),
};
