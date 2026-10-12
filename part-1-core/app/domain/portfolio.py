"""Domain: portfolio generation. PURE.

Aggregates the user's SkillForge footprint (resume, roadmap progress,
certificates, evidence count) into a portfolio model, then renders a
single-file HTML portfolio (Aurora Dark, no external assets — works on
GitHub Pages as-is).

Auto-publish to the user's GitHub is a separate, explicit step that needs
their GitHub token (P3f / account linking). This slice is honest: build +
download now, one-click publish when they connect GitHub.
"""
from __future__ import annotations

import html
from dataclasses import dataclass, field

from app.domain.user import DomainError


@dataclass(frozen=True)
class PortfolioData:
    name: str  # resume title doubles as headline
    summary: str
    skills: tuple[str, ...] = ()
    experience: tuple[dict, ...] = ()
    projects: tuple[dict, ...] = ()
    education: tuple[dict, ...] = ()
    links: dict = field(default_factory=dict)
    certificates: tuple[dict, ...] = ()
    roadmap_title: str = ""
    roadmap_done: int = 0
    roadmap_total: int = 0
    evidence_count: int = 0

    def validate(self) -> None:
        if not self.name.strip():
            raise DomainError("portfolio needs a name/headline — save your resume first")


def _e(s: str) -> str:
    return html.escape(s or "", quote=True)


def render_html(p: PortfolioData) -> str:
    """Single-file portfolio HTML. All user content escaped."""
    p.validate()
    skills = "".join(f"<span class='skill'>{_e(s)}</span>" for s in p.skills)
    exp = "".join(
        "<div class='item'><h3>" + _e(e.get("title", "")) + " <span>· " + _e(e.get("company", "")) + "</span></h3>"
        + "".join(f"<li>{_e(b)}</li>" for b in e.get("bullets", []))
        + "</div>"
        for e in p.experience)
    projs = "".join(
        "<div class='item'><h3>" + _e(pr.get("name", "")) + "</h3><p>" + _e(pr.get("description", "")) + "</p>"
        + "<div class='tags'>" + "".join(f"<span class='tag'>{_e(t)}</span>" for t in pr.get("tech", [])) + "</div></div>"
        for pr in p.projects)
    edu = "".join(
        "<div class='item'><h3>" + _e(e.get("degree", "")) + " <span>· " + _e(e.get("school", "")) + "</span></h3>"
        + f"<p class='muted'>{_e(e.get('year', ''))}</p></div>"
        for e in p.education)
    certs = "".join(
        "<div class='item cert'><h3>🏆 " + _e(c.get("title", "")) + "</h3>"
        + f"<p class='muted'>{_e(c.get('issued_at', '')[:10])} · {_e(c.get('detail', ''))}</p>"
        + f"<code>{_e(c.get('verification_code', ''))}</code></div>"
        for c in p.certificates)
    links = "".join(
        f"<a href='{_e(url)}' target='_blank' rel='noopener'>{_e(name)}</a>"
        for name, url in p.links.items() if url)
    journey = ""
    if p.roadmap_total:
        pct = int(100 * p.roadmap_done / p.roadmap_total)
        journey = (f"<section><h2>Learning journey</h2><p>{_e(p.roadmap_title)} — "
                   f"{p.roadmap_done}/{p.roadmap_total} tasks · {p.evidence_count} evidence submissions</p>"
                   f"<div class='pbar'><div class='pfill' style='width:{pct}%'></div></div></section>")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_e(p.name)} — Portfolio</title>
<style>
:root {{ color-scheme: dark; }}
body {{ font-family: system-ui, sans-serif; background: #0b0e14; color: #e6e9f0;
       max-width: 760px; margin: 0 auto; padding: 40px 20px; line-height: 1.6; }}
header {{ border-bottom: 1px solid #232838; padding-bottom: 24px; margin-bottom: 24px; }}
h1 {{ font-size: 34px; margin: 0 0 8px; }}
h2 {{ font-size: 20px; color: #7dd3fc; margin-top: 32px; }}
h3 {{ font-size: 16px; margin: 0 0 4px; }}
h3 span {{ color: #8b93a7; font-weight: 400; }}
.muted {{ color: #8b93a7; }}
.skill, .tag {{ display: inline-block; background: #141821; border: 1px solid #232838;
  border-radius: 16px; padding: 4px 12px; margin: 3px; font-size: 13px; }}
.item {{ background: #10141d; border: 1px solid #232838; border-radius: 12px;
  padding: 16px; margin: 10px 0; }}
.item ul, .item li {{ margin: 4px 0; }}
.pbar {{ height: 8px; background: #141821; border-radius: 4px; overflow: hidden; }}
.pfill {{ height: 100%; background: linear-gradient(90deg, #7dd3fc, #4ade80); }}
code {{ background: #141821; border: 1px dashed #7dd3fc; color: #7dd3fc;
  border-radius: 8px; padding: 3px 10px; font-size: 13px; }}
.links a {{ margin-right: 14px; color: #7dd3fc; }}
footer {{ margin-top: 40px; color: #8b93a7; font-size: 13px;
  border-top: 1px solid #232838; padding-top: 16px; }}
</style>
</head>
<body>
<header>
<h1>{_e(p.name)}</h1>
<p class="muted">{_e(p.summary)}</p>
<div class="links">{links}</div>
</header>
<section><h2>Skills</h2><div>{skills or "<p class='muted'>—</p>"}</div></section>
{f"<section><h2>Experience</h2>{exp}</section>" if exp else ""}
{f"<section><h2>Projects</h2>{projs}</section>" if projs else ""}
{f"<section><h2>Education</h2>{edu}</section>" if edu else ""}
{f"<section><h2>Certificates</h2>{certs}</section>" if certs else ""}
{journey}
<footer>Built with SkillForge Career Launchpad · evidence-backed, verifiable.</footer>
</body>
</html>
"""
