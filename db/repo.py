from __future__ import annotations

from typing import Any, Dict, List, Optional
from sqlalchemy import select, desc
from db.session import SessionLocal
from db.models import DriftRun

def save_run(host: str, captured_at: str, risk_level: str, risk_score: int, snapshot_path: str, result: Dict[str, Any]) -> int:
    row = DriftRun(
        host=host,
        captured_at=captured_at,
        risk_level=risk_level,
        risk_score=int(risk_score),
        snapshot_path=snapshot_path,
        result=result,
    )
    with SessionLocal() as db:
        db.add(row)
        db.commit()
        db.refresh(row)
        return row.id

def list_runs(limit: int = 20) -> List[Dict[str, Any]]:
    with SessionLocal() as db:
        rows = (
            db.execute(select(DriftRun).order_by(desc(DriftRun.created_at)).limit(limit))
            .scalars()
            .all()
        )
        return [
            {
                "id": r.id,
                "created_at": r.created_at.isoformat(),
                "host": r.host,
                "captured_at": r.captured_at,
                "risk_level": r.risk_level,
                "risk_score": r.risk_score,
                "snapshot_path": r.snapshot_path,
            }
            for r in rows
        ]

def get_run(run_id: int) -> Optional[Dict[str, Any]]:
    with SessionLocal() as db:
        r = db.get(DriftRun, run_id)
        if not r:
            return None
        return {
            "id": r.id,
            "created_at": r.created_at.isoformat(),
            "host": r.host,
            "captured_at": r.captured_at,
            "risk_level": r.risk_level,
            "risk_score": r.risk_score,
            "snapshot_path": r.snapshot_path,
            "result": r.result,
        }
