/* M1 demo plan state.
   Subscribed = the user has a Pro/Expert plan. Sources, in order:
   1. localStorage 'sf_plan' ('pro' | 'expert') — set by the M1 demo
      subscription flow after a successful upgrade.
   2. The real backend tier from GET /api/v1/account/subscription.
   The checkout endpoint itself is 501 until payments KYC — never faked. */

import { api } from './api';

export const PLAN_KEY = 'sf_plan';
export const PLAN_EVENT = 'sf:plan-change';

export type Plan = 'free' | 'pro' | 'expert';

export function readLocalPlan(): Plan | null {
  const v = localStorage.getItem(PLAN_KEY);
  return v === 'pro' || v === 'expert' ? v : null;
}

/** Persist a demo purchase (M1 only; real checkout is 501). */
export function setLocalPlan(plan: 'pro' | 'expert'): void {
  localStorage.setItem(PLAN_KEY, plan);
  window.dispatchEvent(new CustomEvent(PLAN_EVENT, { detail: plan }));
}

export function clearLocalPlan(): void {
  localStorage.removeItem(PLAN_KEY);
  window.dispatchEvent(new CustomEvent(PLAN_EVENT, { detail: null }));
}

/** Real backend tier. Returns null when the call fails (loading states
    should not hide the Go Pro button on a network error). */
export async function fetchBackendTier(): Promise<Plan | null> {
  try {
    const data = await api<{ subscription?: { tier?: string } }>(
      '/api/v1/account/subscription',
    );
    const t = data.subscription?.tier;
    return t === 'pro' || t === 'expert' ? t : t === 'free' ? 'free' : null;
  } catch {
    return null;
  }
}

/** Effective subscribed plan: localStorage demo purchase wins, then backend. */
export async function resolvePlan(): Promise<{ plan: Plan; source: 'local' | 'backend' | 'none' }> {
  const local = readLocalPlan();
  if (local) return { plan: local, source: 'local' };
  const backend = await fetchBackendTier();
  if (backend === 'pro' || backend === 'expert') return { plan: backend, source: 'backend' };
  return { plan: 'free', source: 'none' };
}
