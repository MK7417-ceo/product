"""Inbound adapter (HTTP): placement essentials router.

Public (no auth):
- GET /placement/gd-topics?category=&difficulty=
- GET /placement/interview-qa?category=&subcategory=&company=
- GET /placement/quant?section=&type_id=
- GET /placement/companies
- GET /placement/summary
"""
from __future__ import annotations

from fastapi import APIRouter, Query

from app.adapters.outbound import gd_topics
from app.adapters.outbound import interview_qa
from app.adapters.outbound import quant_bank

router = APIRouter(prefix="/placement", tags=["placement"])


@router.get("/interview-qa/random")
def random_interview_qa(
    count: int = Query(default=5, ge=1, le=10),
    category: str = Query(default=""),
):
    """4-6 (or up to 10) RANDOM interview questions — no repeats in one draw."""
    picked = interview_qa.get_random(count=count, category=category)
    return {"items": picked, "count": len(picked)}


@router.get("/gd-topics")
def list_gd_topics(
    category: str = Query(default=""),
    difficulty: int = Query(default=0, ge=0, le=5),
):
    """50 group-discussion topics with for/against points."""
    return {
        "topics": gd_topics.get_gd_topics(category=category, difficulty=difficulty),
        "count": len(gd_topics.get_gd_topics(category=category, difficulty=difficulty)),
    }


@router.get("/interview-qa")
def list_interview_qa(
    category: str = Query(default=""),
    subcategory: str = Query(default=""),
    company: str = Query(default=""),
):
    """100 interview Q&A — filter by hr/technical, subcategory, or company."""
    if company:
        items = interview_qa.get_by_company(company.lower())
        if category:
            items = [q for q in items if q["category"] == category]
    else:
        items = interview_qa.get_interview_qa(category=category, subcategory=subcategory)
    return {"items": items, "count": len(items)}


@router.get("/quant")
def list_quant(
    section: str = Query(default=""),
    type_id: str = Query(default=""),
):
    """Aptitude questions with tricks. type_id e.g. 'percentages'."""
    questions = quant_bank.get_questions(type_id=type_id, section=section)
    trick = quant_bank.get_trick(type_id) if type_id else None
    return {"questions": questions, "count": len(questions), "trick": trick}


@router.get("/quant/types")
def list_quant_types(section: str = Query(default="")):
    """All 22 aptitude types with their tricks."""
    return {"types": quant_bank.get_types(section=section)}


@router.get("/companies")
def list_companies():
    """Companies covered across interview Q&A."""
    return {"companies": interview_qa.get_companies()}


@router.get("/summary")
def placement_summary():
    """Counts across all placement essentials."""
    return {
        "gd_topics": gd_topics.summary()["total"],
        "interview_qa": interview_qa.summary(),
        "quant": quant_bank.summary(),
    }
