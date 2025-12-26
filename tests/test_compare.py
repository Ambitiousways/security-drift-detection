from drift.compare import evaluate_snapshot_against_policy, compare_snapshots

def test_evaluate_snapshot_flags_flagged_ports_high():
    policy = {
        "baseline": {
            "allowed_ports_common": [22, 80, 443],
            "flagged_ports": [21, 23],
        },
        "rules": {
            "severity": {
                "flagged_port_open": "HIGH",
                "unexpected_port_open": "MEDIUM",
            }
        }
    }

    snapshot = {
        "meta": {"host": "demo-host", "captured_at": "2025-12-26T12:00:00Z"},
        "observed": {"open_ports": [21, 22, 23, 443]},
    }

    result = evaluate_snapshot_against_policy(snapshot, policy)

    assert result["risk_level"] == "HIGH"
    assert result["risk_score"] >= 80
    assert any("Flagged port open: 21" in f["detail"] for f in result["findings"])
    assert any("Flagged port open: 23" in f["detail"] for f in result["findings"])


def test_compare_snapshots_detects_opened_and_closed_ports():
    before = {"observed": {"open_ports": [22, 443, 3389]}}
    after = {"observed": {"open_ports": [22, 443]}}

    diff = compare_snapshots(before, after)

    assert diff["opened"] == []
    assert diff["closed"] == [3389]
    assert "CLOSED port 3389" in diff["changes"]
