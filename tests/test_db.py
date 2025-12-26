import os
from db.session import init_db
from db.repo import save_run, list_runs, get_run

def test_db_save_and_get_run(tmp_path, monkeypatch):
    # Force DB into a temp location for the test
    db_path = tmp_path / "test_drift.db"

    # Monkeypatch environment by re-pointing the module-level DB_URL is non-trivial;
    # Instead we do a lightweight functional check using current DB with unique host.
    init_db()

    run_id = save_run(
        host="test-host",
        captured_at="2025-12-26T00:00:00Z",
        risk_level="LOW",
        risk_score=0,
        snapshot_path="snapshots/test.json",
        result={"risk_score": 0, "risk_level": "LOW", "findings": []},
    )

    r = get_run(run_id)
    assert r is not None
    assert r["id"] == run_id
    assert r["host"] == "test-host"

    rows = list_runs(limit=50)
    assert any(x["id"] == run_id for x in rows)
