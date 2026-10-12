/* Typed API helpers for the P1 pages (Milestone 1 UX rebuild).
   Reuses api()/ApiError/getAccessToken from the shared ./api — nothing here
   touches auth plumbing. Response shapes verified against the live backend
   (part-1-core/app/api/v1/*.py). */

import { api, ApiError, getAccessToken } from './api';

export { ApiError };

/* ---------- assessments (F3) ---------- */

export interface AssessmentSession {
  assessment_id: string;
  topic: string;
  level: string;
  status: string;
  correct: number;
  total: number;
}

export const assessmentApi = {
  list: () => api<{ assessments: AssessmentSession[] }>('/api/v1/assessments'),
};

/* ---------- onboarding profile (F2) — claimed skills ---------- */

export interface ProfileData {
  id: string;
  user_id: string;
  education: string;
  experience_years: number;
  current_skills: string[];
  target_role: string;
  target_domain: string;
  target_level: string;
  tech_focus: string[];
  created_at: string;
}

export const profileApi = {
  me: () => api<ProfileData>('/api/v1/profiles/me'),
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

/* ---------- practice (F6) ---------- */

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
  today: () => api<TodayPlan>('/api/v1/practice/today'),
  submitDaily: (answers: Record<string, number>) =>
    api<{ date: string; correct: number; total: number }>('/api/v1/practice/daily/submit', {
      method: 'POST',
      body: JSON.stringify({ answers }),
    }),
};

/* ---------- certificates (P3b) ---------- */

export interface Certificate {
  id: string;
  kind: string;
  title: string;
  ref_id: string;
  verification_code: string;
  issued_at: string;
  detail: string;
}

export interface CertificateVerifyResult {
  valid: boolean;
  title?: string;
  kind?: string;
  issued_to?: string;
  issued_at?: string;
  detail?: string;
}

export const certificatesApi = {
  list: () => api<Certificate[]>('/api/v1/launchpad/certificates'),
  issue: (kind: string, ref_id: string) =>
    api<Certificate>('/api/v1/launchpad/certificates/issue', {
      method: 'POST',
      body: JSON.stringify({ kind, ref_id }),
    }),
  verify: (code: string) =>
    api<CertificateVerifyResult>(`/api/v1/launchpad/certificates/verify/${code}`),
};

/* ---------- portfolio (P3c) ---------- */

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

/* ---------- interview prep bank (P3g) ---------- */

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

/* ---------- english (P3i) ---------- */

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

/* ---------- account: subscription + links (P3f) ---------- */

export interface TierInfo {
  tier: string;
  name: string;
  price_inr: number;
  max_roadmaps: number;
  features: string[];
}

export interface AccountLinks {
  github: string;
  linkedin: string;
  leetcode: string;
}

export const accountApi = {
  subscription: () =>
    api<{
      subscription: TierInfo;
      tiers: Record<string, { name: string; price_inr: number; features: string[] }>;
    }>('/api/v1/account/subscription'),
  checkout: (tier: string) =>
    api<{ error: string; message: string }>('/api/v1/account/subscription/checkout', {
      method: 'POST',
      body: JSON.stringify({ tier }),
    }),
  getLinks: () => api<AccountLinks>('/api/v1/account/links'),
  saveLinks: (links: AccountLinks) =>
    api<AccountLinks>('/api/v1/account/links', {
      method: 'PUT',
      body: JSON.stringify(links),
    }),
};
