"""Inbound adapter (HTTP): account router — subscription + links (P3f)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.api.v1.auth import _domain_error, current_user_id, require_admin
from app.domain.billing import TIERS, AccountLinks, check_tier, tier_info
from app.domain.user import DomainError

router = APIRouter(prefix="", tags=["account"])


class CheckoutRequest(BaseModel):
    tier: str


class LinksRequest(BaseModel):
    github: str = ""
    linkedin: str = ""
    leetcode: str = ""


class SetTierRequest(BaseModel):
    user_id: str
    tier: str


def _users(request: Request):
    return request.app.state.user_repo


def _links_repo(request: Request):
    return request.app.state.links_repo


@router.get("/account/subscription")
def get_subscription(request: Request, user_id: str = Depends(current_user_id)):
    user = _users(request).get(user_id)
    if not user:
        return JSONResponse(status_code=404, content={"error": "user not found"})
    info = tier_info(user.tier)
    return {"subscription": info,
            "tiers": {k: {"name": v["name"], "price_inr": v["price_inr"],
                           "features": v["features"]} for k, v in TIERS.items()}}


@router.post("/account/subscription/checkout")
def checkout(body: CheckoutRequest, request: Request,
             user_id: str = Depends(current_user_id)):
    try:
        check_tier(body.tier)
    except DomainError as exc:
        raise _domain_error(exc)
    # HONEST: no fake payments. Razorpay/Stripe need business KYC first.
    return JSONResponse(status_code=501, content={
        "error": "payments_not_connected",
        "message": ("Online payments are not connected yet — they need business "
                    "KYC (Razorpay/Stripe). Tier upgrades are currently done "
                    "manually by the team."),
        "requested_tier": body.tier,
    })


@router.post("/account/subscription/set-tier")
def admin_set_tier(body: SetTierRequest, request: Request,
                   _admin: str = Depends(require_admin)):
    try:
        check_tier(body.tier)
    except DomainError as exc:
        raise _domain_error(exc)
    user = _users(request).set_tier(body.user_id, body.tier)
    if not user:
        return JSONResponse(status_code=404, content={"error": "user not found"})
    return {"user_id": user.id, "tier": user.tier}


@router.get("/account/links")
def get_links(request: Request, user_id: str = Depends(current_user_id)):
    links = _links_repo(request).get_by_user(user_id)
    if not links:
        return {"github": "", "linkedin": "", "leetcode": ""}
    return {"github": links.github, "linkedin": links.linkedin,
            "leetcode": links.leetcode}


@router.put("/account/links")
def save_links(body: LinksRequest, request: Request,
               user_id: str = Depends(current_user_id)):
    try:
        links = AccountLinks(user_id=user_id, github=body.github.strip(),
                             linkedin=body.linkedin.strip(),
                             leetcode=body.leetcode.strip())
        links.validate()
    except DomainError as exc:
        raise _domain_error(exc)
    _links_repo(request).upsert(links)
    return {"github": links.github, "linkedin": links.linkedin,
            "leetcode": links.leetcode}
