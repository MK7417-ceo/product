"""Inbound adapter (HTTP): tech taxonomy API — every major tech tool/skill.

Public (no auth):
  GET /taxonomy/tools[?importance=critical|high|medium|low][?domain=slug]
  GET /taxonomy/tools/{slug}
  GET /taxonomy/categories
  GET /taxonomy/critical
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app.adapters.outbound.tech_taxonomy import (
    VALID_IMPORTANCE,
    get_important_tools,
    get_tool,
    list_categories,
    list_tools,
)

router = APIRouter(tags=["taxonomy"])


@router.get("/taxonomy/tools")
def tools(
    importance: str | None = Query(default=None, description="critical|high|medium|low"),
    domain: str | None = Query(default=None, description="curriculum domain slug"),
):
    if importance is not None and importance not in VALID_IMPORTANCE:
        raise HTTPException(status_code=422, detail=f"unknown importance: {importance}")
    result = list_tools(importance)
    if domain is not None:
        result = [t for t in result if t["related_domain"] == domain]
    return {"tools": result, "count": len(result)}


@router.get("/taxonomy/tools/{slug}")
def tool_detail(slug: str):
    tool = get_tool(slug)
    if tool is None:
        raise HTTPException(status_code=404, detail="tool not found")
    return tool


@router.get("/taxonomy/categories")
def categories():
    cats = list_categories()
    return {"categories": cats, "count": len(cats)}


@router.get("/taxonomy/critical")
def critical_tools():
    tools = list_tools("critical")
    return {"tools": tools, "count": len(tools)}


@router.get("/taxonomy/domains/{domain_slug}/tools")
def domain_tools(domain_slug: str):
    """Important tools for a curriculum domain, sorted by importance."""
    return {"tools": get_important_tools(domain_slug), "domain": domain_slug}
