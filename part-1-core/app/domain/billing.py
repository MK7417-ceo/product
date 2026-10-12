"""Domain: subscriptions + account linking. PURE.

Tiers are real: the matrix defines what each tier unlocks. Payments are
NOT faked — checkout returns 'not connected' until the operator completes
Razorpay/Stripe business KYC. Admins can set tiers directly (testing,
gifting, manual upgrades).
"""
from __future__ import annotations

from dataclasses import dataclass

from app.domain.user import DomainError

TIERS: dict[str, dict] = {
    "free": {
        "name": "Free",
        "price_inr": 0,
        "max_roadmaps": 10,
        "features": [
            "Assessment + skill gaps",
            "Roadmap (up to 10)",
            "Daily practice questions",
            "Code runner",
            "Resume builder + JD matcher",
        ],
    },
    "pro": {
        "name": "Pro",
        "price_inr": 299,
        "max_roadmaps": 10_000,
        "features": [
            "Everything in Free",
            "Unlimited roadmaps",
            "Certificates + verification",
            "Portfolio builder + download",
            "Interview prep + PI mock",
            "English track",
        ],
    },
    "expert": {
        "name": "Expert",
        "price_inr": 799,
        "max_roadmaps": 10_000,
        "features": [
            "Everything in Pro",
            "Priority code-engine queue",
            "Early access to new tracks",
            "Founder's badge on portfolio",
        ],
    },
}


def tier_info(tier: str) -> dict:
    if tier not in TIERS:
        raise DomainError(f"unknown tier: {tier}")
    return {"tier": tier, **TIERS[tier]}


def check_tier(tier: str) -> str:
    if tier not in TIERS:
        raise DomainError(f"unknown tier: {tier}")
    return tier


@dataclass(frozen=True)
class AccountLinks:
    user_id: str
    github: str = ""
    linkedin: str = ""
    leetcode: str = ""

    def validate(self) -> None:
        for field in ("github", "linkedin", "leetcode"):
            v = getattr(self, field)
            if v and len(v) > 80:
                raise DomainError(f"{field} handle too long")
            if v and not all(c.isalnum() or c in "-_." for c in v):
                raise DomainError(f"{field} handle has invalid characters")
