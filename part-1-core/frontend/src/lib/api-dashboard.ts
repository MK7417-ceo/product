/* Typed API helpers for the Dashboard page (Milestone 1).
   Uses the shared fetch client from ./api — do NOT duplicate token logic here.
   Shapes verified against part-1-core/app/api/v1/{roadmaps,practice,onboarding,assessments}.py
   (live backend http://127.0.0.1:8001). Missing resources surface as null;
   the UI renders actionable empty states for those — never mock data. */

import { api, ApiError } from './api';

/* ---------- roadmaps ---------- */

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

export interface TaskCounts {
  total: number;
  pending: number;
  in_progress: number;
  completed: number;
}

export interface RoadmapOut {
  id: string;
  version: number;
  title: string;
  source: string;
  tasks: RoadmapTask[];
  task_counts: TaskCounts;
}

/* ---------- practice ---------- */

export interface TodayQuestion {
  id: string;
  topic: string;
  level: string;
  prompt: string;
  choices: string[];
}

export interface TodayTask {
  id: string;
  title: string;
  status: string;
  effort_minutes: number;
  priority: string;
}

export interface TodayOut {
  date: string;
  questions: TodayQuestion[];
  tasks: TodayTask[];
  has_roadmap: boolean;
}

/* ---------- assessments ---------- */

export interface AssessmentSummary {
  assessment_id: string;
  topic: string;
  level: string;
  status: string;
  correct: number;
  total: number;
}

/* ---------- onboarding ---------- */

export interface ProfileOut {
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

export interface PlacementTopicsOut {
  topics: string[];
}

/* Missing-resource errors from the backend are DomainError → 400/404.
   Treat those as "not present yet" (null); anything else rethrows. */
function missing(e: unknown): boolean {
  return e instanceof ApiError && (e.status === 400 || e.status === 404);
}

export const dashboardApi = {
  /** null when the user has not generated a roadmap yet. */
  getRoadmap: async (): Promise<RoadmapOut | null> => {
    try {
      return await api<RoadmapOut>('/api/v1/roadmaps/current');
    } catch (e) {
      if (missing(e)) return null;
      throw e;
    }
  },

  getToday: () => api<TodayOut>('/api/v1/practice/today'),

  getAssessments: async (): Promise<AssessmentSummary[]> => {
    const res = await api<{ assessments: AssessmentSummary[] }>('/api/v1/assessments');
    return res.assessments ?? [];
  },

  /** null when the user has not created a profile yet. */
  getProfile: async (): Promise<ProfileOut | null> => {
    try {
      return await api<ProfileOut>('/api/v1/profiles/me');
    } catch (e) {
      if (missing(e)) return null;
      throw e;
    }
  },

  getPlacementTopics: () => api<PlacementTopicsOut>('/api/v1/placement/topics'),
};

export { ApiError };
