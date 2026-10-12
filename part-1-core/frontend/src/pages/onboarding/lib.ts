/* Shared types + localStorage contracts for the UX v2 onboarding pages.
   Backend shapes verified against the live API (Oct 13, 2026) — never guess. */

export interface Question {
  id: string;
  topic: string;
  level: string;
  prompt: string;
  choices: string[];
}

export interface PlacementStart {
  placement_id: string;
  topic: string;
  claimed_level: string;
  status: string;
  verification_skipped: boolean;
  verified_level: string | null;
  levels: string[];
  question_count: number;
  questions: Question[];
}

/** Router-state contract for /verification (set by MakePlan via navigate). */
export interface VerificationState {
  placement_id: string;
  topic: string;
  claimed_level: string;
  questions: Question[];
}

export interface LevelResult {
  correct: number;
  total: number;
  ratio: number;
}

export interface PlacementAnalysis {
  claimed_level: string;
  verified_level: string;
  correct: number;
  total: number;
  summary: string;
  levels: Record<string, LevelResult>;
}

export interface PlacementSubmitResult {
  placement_id: string;
  status: string;
  correct: number;
  total: number;
  claimed_level: string;
  verified_level: string;
  analysis: PlacementAnalysis;
}

export interface ExperienceItem {
  title: string;
  company: string;
  start: string;
  end: string;
  bullets: string[];
}

export interface ProjectItem {
  name: string;
  description: string;
  tech: string[];
  link: string;
}

export interface EducationItem {
  degree: string;
  school: string;
  year: string;
}

export interface Resume {
  id: string;
  title: string;
  summary: string;
  skills: string[];
  experience: ExperienceItem[];
  projects: ProjectItem[];
  education: EducationItem[];
  links: Record<string, string>;
}

export interface KeywordHit {
  keyword: string;
  jd_count: number;
}

export interface JDMatch {
  score: number;
  jd_keyword_count: number;
  matched: KeywordHit[];
  missing: KeywordHit[];
  suggestions: string[];
}

export interface TierInfo {
  name: string;
  price_inr: number;
  features: string[];
}

export interface SubscriptionInfo {
  tier: string;
  name: string;
  price_inr: number;
  max_roadmaps: number;
  features: string[];
}

/* ------------------------------------------------------------------ */
/* localStorage contracts (documented in INTEGRATION.md)               */
/* ------------------------------------------------------------------ */

/** Welcome nudge shown once: set when the user clicks "Skip for now". */
const WELCOME_SEEN_KEY = 'sf_welcome_seen';
export function welcomeSeen(): boolean {
  return localStorage.getItem(WELCOME_SEEN_KEY) === '1';
}
export function markWelcomeSeen(): void {
  localStorage.setItem(WELCOME_SEEN_KEY, '1');
}

/**
 * DEMO SCAFFOLDING — remove when real checkout lands.
 * The shell's "Go Pro" popup + plan badge read this key:
 *   'pro' | 'expert' → popup hidden, PRO/EXPERT badge shown.
 *   absent           → shell falls back to the backend subscription tier.
 */
const DEMO_PLAN_KEY = 'sf_plan';
export type DemoPlan = 'pro' | 'expert';
export function getDemoPlan(): DemoPlan | null {
  const v = localStorage.getItem(DEMO_PLAN_KEY);
  return v === 'pro' || v === 'expert' ? v : null;
}
export function setDemoPlan(p: DemoPlan): void {
  localStorage.setItem(DEMO_PLAN_KEY, p);
}
export function clearDemoPlan(): void {
  localStorage.removeItem(DEMO_PLAN_KEY);
}

export function fmtINR(n: number): string {
  return `₹${n.toLocaleString('en-IN')}`;
}
