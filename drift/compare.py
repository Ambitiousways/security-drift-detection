from __future__ import annotations

from typing import Any, Dict, List
from pathlib import Path
import yaml


def load_policy(path: str) -> Dict[str, Any]:
    """Load baseline policy YAML."""
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def _severity_for(code: str, policy: Dict[str, Any]) -> str:
    sev = policy.get("rules", {}).get("severity", {})
    return sev.get(code, "LOW")


def evaluate_snapshot_against_policy(snapshot: Dict[str, Any], policy: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compare observed open ports to baseline policy.
    Returns findings and a simple risk score/level.
    """
    observed_ports = set(snapshot.get("observed", {}).get("open_ports", []))
    baseline = policy.get("baseline", {})
    allowed = set(baseline.get("allowed_ports_common", []))
    flagged = set(baseline.get("flagged_ports", []))

    findings: List[Dict[str, Any]] = []
    score = 0

    # Flagged ports open
    for p in sorted(observed_ports & flagged):
        sev = _severity_for("flagged_port_open", policy)
        findings.append(
            {"code": "flagged_port_open", "severity": sev, "detail": f"Flagged port open: {p}"}
        )
        score += 60 if sev == "HIGH" else 35

    # Unexpected ports open (not allowed and not flagged)
    unexpected = sorted([p for p in observed_ports if p not in allowed and p not in flagged])
    for p in unexpected:
        sev = _severity_for("unexpected_port_open", policy)
        findings.append(
            {"code": "unexpected_port_open", "severity": sev, "detail": f"Unexpected port open: {p}"}
        )
        score += 25 if sev == "MEDIUM" else 10

    risk_level = "LOW"
    if score >= 80:
        risk_level = "HIGH"
    elif score >= 35:
        risk_level = "MEDIUM"

    return {
        "risk_score": score,
        "risk_level": risk_level,
        "findings": findings,
        "observed_open_ports": sorted(observed_ports),
        "baseline_allowed_ports": sorted(allowed),
        "baseline_flagged_ports": sorted(flagged),
    }


def compare_snapshots(before: Dict[str, Any], after: Dict[str, Any]) -> Dict[str, Any]:
    """Compare two snapshots and report opened/closed ports."""
    b_ports = set(before.get("observed", {}).get("open_ports", []))
    a_ports = set(after.get("observed", {}).get("open_ports", []))

    opened = sorted(a_ports - b_ports)
    closed = sorted(b_ports - a_ports)

    changes: List[str] = []
    for p in opened:
        changes.append(f"OPENED port {p}")
    for p in closed:
        changes.append(f"CLOSED port {p}")

    return {"opened": opened, "closed": closed, "changes": changes}
