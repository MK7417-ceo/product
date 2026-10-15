import { useEffect, useRef, useState } from 'react';
import { api, ApiError } from '../../lib/api';
import type {
  EducationItem, ExperienceItem, JDMatch, ProjectItem, Resume,
} from './lib';
import './onboarding.css';

/**
 * Route: /resume — JD matcher + guided resume builder (Flow 2).
 * Also mounted as the sidebar LAUNCH → Resume page (same component).
 *
 * ATS score IS the JD-match score (deterministic backend `match_jd`).
 * Score < 70 → missing keywords + suggestions → edit → re-check.
 */
const emptyExp = (): ExperienceItem => ({ title: '', company: '', start: '', end: '', bullets: [] });
const emptyProj = (): ProjectItem => ({ name: '', description: '', tech: [], link: '' });
const emptyEdu = (): EducationItem => ({ degree: '', school: '', year: '' });

function ScoreRing({ score }: { score: number }) {
  const r = 56;
  const c = 2 * Math.PI * r;
  const frac = Math.max(0, Math.min(100, score)) / 100;
  return (
    <div className="ob-ring">
      <svg width="132" height="132" viewBox="0 0 132 132">
        <defs>
          <linearGradient id="ob-ring-grad" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="#8B5CF6" />
            <stop offset="100%" stopColor="#36C5F0" />
          </linearGradient>
        </defs>
        <circle cx="66" cy="66" r={r} fill="none" stroke="rgba(255,255,255,.08)" strokeWidth="11" />
        <circle
          cx="66" cy="66" r={r} fill="none"
          stroke="url(#ob-ring-grad)" strokeWidth="11" strokeLinecap="round"
          strokeDasharray={c} strokeDashoffset={c * (1 - frac)}
          style={{ transition: 'stroke-dashoffset .6s ease' }}
        />
      </svg>
      <div className="num">
        <b className="mono">{Math.round(score)}</b>
        <small>ATS SCORE</small>
      </div>
    </div>
  );
}

export default function Resume() {
  // ---- resume form state ----
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState('');
  const [hasResume, setHasResume] = useState(false);
  const [title, setTitle] = useState('');
  const [summary, setSummary] = useState('');
  const [skillsText, setSkillsText] = useState('');
  const [experience, setExperience] = useState<ExperienceItem[]>([]);
  const [projects, setProjects] = useState<ProjectItem[]>([]);
  const [education, setEducation] = useState<EducationItem[]>([]);
  const [links, setLinks] = useState({ github: '', linkedin: '', website: '' });
  const [saving, setSaving] = useState(false);
  const [saveMsg, setSaveMsg] = useState('');

  // ---- JD matcher state ----
  const [jdText, setJdText] = useState('');
  const [matching, setMatching] = useState(false);
  const [matchError, setMatchError] = useState('');
  const [match, setMatch] = useState<JDMatch | null>(null);

  const fieldRefs = useRef<Record<string, HTMLElement | null>>({});
  const setRef = (k: string) => (el: HTMLElement | null) => { fieldRefs.current[k] = el; };

  useEffect(() => {
    api<Resume>('/api/v1/launchpad/resume')
      .then((r) => {
        setHasResume(true);
        setTitle(r.title ?? '');
        setSummary(r.summary ?? '');
        setSkillsText((r.skills ?? []).join(', '));
        setExperience(r.experience ?? []);
        setProjects(r.projects ?? []);
        setEducation(r.education ?? []);
        setLinks({
          github: r.links?.github ?? '',
          linkedin: r.links?.linkedin ?? '',
          website: r.links?.website ?? '',
        });
      })
      .catch((e) => {
        if (e instanceof ApiError && e.status === 404) {
          setHasResume(false); // no resume yet — start blank, that's fine
        } else {
          setLoadError(e instanceof Error ? e.message : 'Could not load resume');
        }
      })
      .finally(() => setLoading(false));
  }, []);

  // ---- inline prompts for missing required details (Flow 2, step H) ----
  const skills = skillsText.split(',').map((s) => s.trim()).filter(Boolean);
  const prompts: { key: string; text: string; target: string }[] = [];
  if (!title.trim()) prompts.push({ key: 'title', text: 'Add a professional title (e.g. AI/ML Engineer)', target: 'title' });
  if (!summary.trim()) prompts.push({ key: 'summary', text: 'Add a 2-line summary of what you do', target: 'summary' });
  if (skills.length < 3) prompts.push({ key: 'skills', text: `Add at least 3 skills (${skills.length}/3 so far)`, target: 'skills' });
  if (experience.length === 0) prompts.push({ key: 'exp', text: 'Add your most recent role', target: 'experience' });
  if (education.length === 0) prompts.push({ key: 'edu', text: 'Add your education', target: 'education' });
  if (projects.length === 0) prompts.push({ key: 'proj', text: 'Add a project (optional, but recruiters look for it)', target: 'projects' });

  const scrollTo = (target: string) => {
    fieldRefs.current[target]?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  };

  const runMatch = async () => {
    setMatchError('');
    setMatch(null);
    const text = jdText.trim();
    if (!text) { setMatchError('Paste a job description first.'); return; }
    setMatching(true);
    try {
      const res = await api<JDMatch>('/api/v1/launchpad/jd-match', {
        method: 'POST',
        body: JSON.stringify({ jd_text: text }),
      });
      setMatch(res);
    } catch (e) {
      if (e instanceof ApiError && e.status === 404) {
        setMatchError('No resume on file yet — complete the builder below, save, then re-check.');
      } else {
        setMatchError(e instanceof Error ? e.message : 'JD match failed');
      }
    } finally {
      setMatching(false);
    }
  };

  const save = async () => {
    setSaving(true);
    setSaveMsg('');
    try {
      await api('/api/v1/launchpad/resume', {
        method: 'PUT',
        body: JSON.stringify({
          title: title.trim(),
          summary: summary.trim(),
          skills,
          experience: experience.map((e) => ({
            title: e.title.trim(), company: e.company.trim(),
            start: e.start.trim(), end: e.end.trim(),
            bullets: e.bullets.map((b) => b.trim()).filter(Boolean),
          })),
          projects: projects.map((p) => ({
            name: p.name.trim(), description: p.description.trim(),
            tech: p.tech, link: p.link.trim(),
          })),
          education: education.map((e) => ({
            degree: e.degree.trim(), school: e.school.trim(), year: e.year.trim(),
          })),
          links: {
            github: links.github.trim(), linkedin: links.linkedin.trim(),
            website: links.website.trim(),
          },
        }),
      });
      setHasResume(true);
      setSaveMsg('Resume saved.');
      if (jdText.trim()) await runMatch(); // Flow 2: save → re-run JD match
    } catch (e) {
      setSaveMsg(e instanceof Error ? `Save failed: ${e.message}` : 'Save failed');
    } finally {
      setSaving(false);
    }
  };

  const updExp = (i: number, patch: Partial<ExperienceItem>) =>
    setExperience((xs) => xs.map((x, j) => (j === i ? { ...x, ...patch } : x)));
  const updProj = (i: number, patch: Partial<ProjectItem>) =>
    setProjects((xs) => xs.map((x, j) => (j === i ? { ...x, ...patch } : x)));
  const updEdu = (i: number, patch: Partial<EducationItem>) =>
    setEducation((xs) => xs.map((x, j) => (j === i ? { ...x, ...patch } : x)));

  if (loading) {
    return <div className="ob"><div className="ob-load">Loading your resume…</div></div>;
  }
  if (loadError) {
    return (
      <div className="ob">
        <h1 className="ob-title">Resume</h1>
        <div className="ob-alert err">{loadError}</div>
      </div>
    );
  }

  return (
    <div className="ob">
      <h1 className="ob-title">Resume</h1>
      <p className="ob-sub">
        Paste a job description to get your ATS score, then close the gaps with the
        guided builder. {hasResume ? 'Resume on file.' : 'No resume on file yet — build one below.'}
      </p>

      {/* ============ JD matcher ============ */}
      <div className="ob-section-t">JOB DESCRIPTION MATCH</div>
      <div className="ob-card glow">
        <h3>Check ATS score</h3>
        <p className="ob-hint">Paste the full job description — we extract its keywords and score your resume 0–100.</p>
        <div className="ob-field">
          <textarea
            value={jdText}
            onChange={(e) => setJdText(e.target.value)}
            placeholder="Paste the job description here…"
            aria-label="Job description"
          />
        </div>
        <div className="ob-cta-row" style={{ marginTop: 0 }}>
          <button className="ob-btn-sm" onClick={runMatch} disabled={matching}>
            {matching ? 'Scoring…' : 'Check ATS score'}
          </button>
        </div>
        {matchError && <div className="ob-alert err" style={{ marginTop: 14 }}>{matchError}</div>}

        {match && (
          <div style={{ marginTop: 18 }}>
            <div className="ob-ring-wrap">
              <ScoreRing score={match.score} />
              <div>
                <b style={{ fontSize: 15 }}>
                  {match.matched.length} of {match.jd_keyword_count} JD keywords matched
                </b>
                <p className="ob-hint" style={{ margin: '6px 0 0' }}>
                  {match.score >= 70
                    ? 'Above the 70 bar — this resume is competitive for this JD.'
                    : 'Below the 70 bar — add the missing keywords below, then re-check.'}
                </p>
              </div>
            </div>

            {match.matched.length > 0 && (
              <>
                <div className="ob-section-t" style={{ marginTop: 18 }}>MATCHED KEYWORDS</div>
                <div className="ob-chips">
                  {match.matched.map((m) => (
                    <span key={m.keyword} className="ob-chip matched">
                      {m.keyword}<span className="n">×{m.jd_count}</span>
                    </span>
                  ))}
                </div>
              </>
            )}

            {match.missing.length > 0 && (
              <>
                <div className="ob-section-t" style={{ marginTop: 18 }}>MISSING KEYWORDS</div>
                <div className="ob-chips">
                  {match.missing.map((m) => (
                    <span key={m.keyword} className="ob-chip missing">
                      {m.keyword}<span className="n">×{m.jd_count}</span>
                    </span>
                  ))}
                </div>
                <div className="ob-section-t" style={{ marginTop: 18 }}>SUGGESTIONS</div>
                <ul className="ob-sug">
                  {match.suggestions.map((s, i) => <li key={i}>{s}</li>)}
                </ul>
              </>
            )}
          </div>
        )}
      </div>

      {/* ============ guided builder ============ */}
      <div className="ob-section-t">RESUME BUILDER</div>

      {prompts.length > 0 && (
        <div style={{ marginBottom: 18 }}>
          {prompts.map((p) => (
            <div className="ob-prompt" key={p.key}>
              <span className="dot">●</span>
              <span>{p.text}</span>
              <button onClick={() => scrollTo(p.target)}>Fill it →</button>
            </div>
          ))}
        </div>
      )}

      <div className="ob-card" ref={setRef('title')}>
        <h3>Basics</h3>
        <div className="ob-field" style={{ marginTop: 12 }}>
          <label>Professional title</label>
          <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} placeholder="AI/ML Engineer" />
        </div>
        <div className="ob-field" ref={setRef('summary')}>
          <label>Summary</label>
          <textarea value={summary} onChange={(e) => setSummary(e.target.value)} placeholder="2 lines on what you build and what you're great at…" style={{ minHeight: 80 }} />
        </div>
        <div className="ob-field" ref={setRef('skills')}>
          <label>Skills (comma-separated)</label>
          <input type="text" value={skillsText} onChange={(e) => setSkillsText(e.target.value)} placeholder="python, machine learning, django, react" />
        </div>
        <div className="ob-grid2">
          {(['github', 'linkedin', 'website'] as const).map((k) => (
            <div className="ob-field" key={k}>
              <label style={{ textTransform: 'capitalize' }}>{k}</label>
              <input
                type="text" value={links[k]}
                onChange={(e) => setLinks((l) => ({ ...l, [k]: e.target.value }))}
                placeholder={k === 'website' ? 'https://…' : 'your handle / url'}
              />
            </div>
          ))}
        </div>
      </div>

      <div className="ob-card" ref={setRef('experience')}>
        <div className="ob-list-head">
          <h3>Experience</h3>
          <button className="ob-btn-sm" onClick={() => setExperience((xs) => [...xs, emptyExp()])}>+ Add role</button>
        </div>
        {experience.length === 0 && <p className="ob-empty">No roles yet.</p>}
        {experience.map((e, i) => (
          <div className="ob-list-item" key={i}>
            <div className="ob-list-head">
              <b>Role {i + 1}</b>
              <button className="ob-del" onClick={() => setExperience((xs) => xs.filter((_, j) => j !== i))}>Remove</button>
            </div>
            <div className="ob-grid2">
              <div className="ob-field"><label>Title</label>
                <input type="text" value={e.title} onChange={(ev) => updExp(i, { title: ev.target.value })} placeholder="ML Intern" /></div>
              <div className="ob-field"><label>Company</label>
                <input type="text" value={e.company} onChange={(ev) => updExp(i, { company: ev.target.value })} placeholder="Acme AI" /></div>
              <div className="ob-field"><label>Start</label>
                <input type="text" value={e.start} onChange={(ev) => updExp(i, { start: ev.target.value })} placeholder="2024-06" /></div>
              <div className="ob-field"><label>End</label>
                <input type="text" value={e.end} onChange={(ev) => updExp(i, { end: ev.target.value })} placeholder="2024-12 / present" /></div>
            </div>
            <div className="ob-field"><label>Achievements (one per line)</label>
              <textarea value={e.bullets.join('\n')} onChange={(ev) => updExp(i, { bullets: ev.target.value.split('\n') })} placeholder={'Shipped X, improving Y by Z%\n…'} style={{ minHeight: 70 }} /></div>
          </div>
        ))}
      </div>

      <div className="ob-card" ref={setRef('projects')}>
        <div className="ob-list-head">
          <h3>Projects</h3>
          <button className="ob-btn-sm" onClick={() => setProjects((xs) => [...xs, emptyProj()])}>+ Add project</button>
        </div>
        {projects.length === 0 && <p className="ob-empty">No projects yet.</p>}
        {projects.map((p, i) => (
          <div className="ob-list-item" key={i}>
            <div className="ob-list-head">
              <b>Project {i + 1}</b>
              <button className="ob-del" onClick={() => setProjects((xs) => xs.filter((_, j) => j !== i))}>Remove</button>
            </div>
            <div className="ob-grid2">
              <div className="ob-field"><label>Name</label>
                <input type="text" value={p.name} onChange={(ev) => updProj(i, { name: ev.target.value })} placeholder="Skill-gap analyzer" /></div>
              <div className="ob-field"><label>Link</label>
                <input type="text" value={p.link} onChange={(ev) => updProj(i, { link: ev.target.value })} placeholder="https://github.com/…" /></div>
            </div>
            <div className="ob-field"><label>Description</label>
              <textarea value={p.description} onChange={(ev) => updProj(i, { description: ev.target.value })} placeholder="What it does and what you learned…" style={{ minHeight: 70 }} /></div>
            <div className="ob-field"><label>Tech (comma-separated)</label>
              <input type="text" value={p.tech.join(', ')} onChange={(ev) => updProj(i, { tech: ev.target.value.split(',').map((s) => s.trim()).filter(Boolean) })} placeholder="python, fastapi, react" /></div>
          </div>
        ))}
      </div>

      <div className="ob-card" ref={setRef('education')}>
        <div className="ob-list-head">
          <h3>Education</h3>
          <button className="ob-btn-sm" onClick={() => setEducation((xs) => [...xs, emptyEdu()])}>+ Add education</button>
        </div>
        {education.length === 0 && <p className="ob-empty">No education yet.</p>}
        {education.map((e, i) => (
          <div className="ob-list-item" key={i}>
            <div className="ob-list-head">
              <b>Education {i + 1}</b>
              <button className="ob-del" onClick={() => setEducation((xs) => xs.filter((_, j) => j !== i))}>Remove</button>
            </div>
            <div className="ob-grid2">
              <div className="ob-field"><label>Degree</label>
                <input type="text" value={e.degree} onChange={(ev) => updEdu(i, { degree: ev.target.value })} placeholder="B.Tech, Computer Science" /></div>
              <div className="ob-field"><label>School</label>
                <input type="text" value={e.school} onChange={(ev) => updEdu(i, { school: ev.target.value })} placeholder="IIT Delhi" /></div>
              <div className="ob-field"><label>Year</label>
                <input type="text" value={e.year} onChange={(ev) => updEdu(i, { year: ev.target.value })} placeholder="2026" /></div>
            </div>
          </div>
        ))}
      </div>

      {saveMsg && (
        <div className={`ob-alert ${saveMsg.startsWith('Save failed') ? 'err' : 'ok'}`}>{saveMsg}</div>
      )}
      <div className="ob-cta-row">
        <button className="ob-btn" onClick={save} disabled={saving}>
          {saving ? 'Saving…' : 'Save resume'}
        </button>
        {jdText.trim() && <span className="ob-empty">Saving re-runs the JD match automatically.</span>}
      </div>
    </div>
  );
}
