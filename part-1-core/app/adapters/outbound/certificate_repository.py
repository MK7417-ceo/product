"""Outbound adapter: CertificateRepository backed by SQLAlchemy."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Callable

from sqlalchemy.orm import Session

from app.adapters.outbound.models import CertificateModel
from app.domain.certificate import Certificate


def _to_domain(m: CertificateModel) -> Certificate:
    return Certificate(id=m.id, user_id=m.user_id, kind=m.kind,
                       title=m.title, ref_id=m.ref_id,
                       verification_code=m.verification_code,
                       issued_at=m.issued_at.isoformat(), detail=m.detail or "")


class SqlAlchemyCertificateRepository:
    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self._sessions = session_factory

    def save(self, cert: Certificate) -> None:
        with self._sessions() as s:
            s.add(CertificateModel(
                id=cert.id, user_id=cert.user_id, kind=cert.kind,
                title=cert.title, ref_id=cert.ref_id,
                verification_code=cert.verification_code,
                issued_at=datetime.fromisoformat(cert.issued_at),
                detail=cert.detail))
            s.commit()

    def list_for_user(self, user_id: str) -> list[Certificate]:
        with self._sessions() as s:
            rows = (s.query(CertificateModel).filter_by(user_id=user_id)
                    .order_by(CertificateModel.issued_at.desc()).all())
            return [_to_domain(r) for r in rows]

    def find_by_code(self, code: str) -> Certificate | None:
        with self._sessions() as s:
            row = (s.query(CertificateModel)
                   .filter_by(verification_code=code).one_or_none())
            return _to_domain(row) if row else None

    def exists(self, user_id: str, kind: str, ref_id: str) -> bool:
        with self._sessions() as s:
            return (s.query(CertificateModel)
                    .filter_by(user_id=user_id, kind=kind, ref_id=ref_id)
                    .one_or_none() is not None)
