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

/* ---------- code runner (P2 via Core) ---------- */

export interface EngineLanguage {
  id: string;
  name: string;
  available?: boolean;
  version?: string;
}

export interface CodeRunResult {
  run_id: string;
  verdict: string; // "ok" | "compile_error" | "runtime_error" | "time_limit" | ...
  stdout: string;
  stderr: string;
  truncated: boolean;
  exit_code: number | null;
  cpu_ms: number | null;
  peak_ram_mb: number | null;
  timed_out: boolean;
  server_ms?: number;
}

export interface EngineErrorBody {
  error: string;
  message: string;
}

export const codeApi = {
  run: (language: string, code: string, stdin: string) =>
    api<CodeRunResult>('/api/v1/code/run', {
      method: 'POST',
      body: JSON.stringify({ language, code, stdin }),
    }),
  languages: () => api<{ languages: EngineLanguage[] }>('/api/v1/code/languages'),
};

/* ---------- daily DSA (F6b) ---------- */

export interface DSAExample {
  stdin: string;
  stdout: string;
  explanation: string;
}

export interface DailyDSAQuestion {
  id: string;
  title: string;
  difficulty: string; // easy | medium | hard
  description: string;
  examples: DSAExample[];
  starter_code: string;
  hidden_test_count: number;
  topic_tags: string[];
  hints: string[];
  date: string; // YYYY-MM-DD
}

export interface DSASubmitResult {
  date: string;
  question_id: string;
  passed: number;
  total: number;
  verdict: string;
  accepted: boolean;
  failed_case: string | null;
}

export const dsaApi = {
  daily: (date?: string) =>
    api<DailyDSAQuestion>(`/api/v1/practice/dsa-daily${date ? `?date=${encodeURIComponent(date)}` : ''}`),
  submit: (date: string, language: string, code: string) =>
    api<DSASubmitResult>('/api/v1/dsa/daily/submit', {
      method: 'POST',
      body: JSON.stringify({ date, language, code }),
    }),
};
