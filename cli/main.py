from __future__ import annotations

import json
from pathlib import Path
import typer
from rich import print

from drift.capture import capture_snapshot
from drift.compare import load_policy, evaluate_snapshot_against_policy, compare_snapshots

from db.session import init_db
from db.repo import save_run, list_runs, get_run

app = typer.Typer(help="Security Drift Detection CLI")


@app.command()
def capture(
    target: str = typer.Option(..., help="Target host or IP (authorized only)."),
    out: str = typer.Option("snapshots", help="Output directory for snapshots."),
):
    """Capture a snapshot of observed open ports."""
    snap = capture_snapshot(target)

    Path(out).mkdir(parents=True, exist_ok=True)
    ts = snap["meta"]["captured_at"].replace(":", "").replace("-", "")
    out_path = Path(out) / f"snapshot_{target}_{ts}.json"

    out_path.write_text(json.dumps(snap, indent=2), encoding="utf-8")

    print(f"[green]Snapshot saved:[/green] {out_path}")
    print(json.dumps(snap["observed"], indent=2))


@app.command(name="check-drift")
def check_drift(
    snapshot: str = typer.Option(..., help="Path to snapshot JSON."),
    policy: str = typer.Option("baselines/baseline_policy.yml", help="Baseline policy YAML."),
):
    """Evaluate snapshot against baseline, report drift, and store a history record."""
    pol = load_policy(policy)
    snap = json.loads(Path(snapshot).read_text(encoding="utf-8"))
    result = evaluate_snapshot_against_policy(snap, pol)

    # Persist the run (history)
    init_db()
    run_id = save_run(
        host=snap["meta"]["host"],
        captured_at=snap["meta"]["captured_at"],
        risk_level=result["risk_level"],
        risk_score=result["risk_score"],
        snapshot_path=snapshot,
        result=result,
    )

    print(f"[bold]Target:[/bold] {snap['meta']['host']}")
    print(f"[bold]Captured:[/bold] {snap['meta']['captured_at']}")
    print(f"[bold]Risk:[/bold] {result['risk_level']} (score={result['risk_score']})")
    print(f"[green]Saved drift run[/green] id={run_id}")

    if not result["findings"]:
        print("[green]No drift detected[/green]")
    else:
        print("[bold]Findings:[/bold]")
        for f in result["findings"]:
            print(f"- [{f['severity']}] {f['detail']}")


@app.command(name="diff-snapshots")
def diff_snapshots(
    before: str = typer.Option(..., help="BEFORE snapshot JSON."),
    after: str = typer.Option(..., help="AFTER snapshot JSON."),
):
    """Compare two snapshots over time."""
    b = json.loads(Path(before).read_text(encoding="utf-8"))
    a = json.loads(Path(after).read_text(encoding="utf-8"))
    diff = compare_snapshots(b, a)

    if not diff["changes"]:
        print("No changes detected")
    else:
        print("[bold]Changes:[/bold]")
        for c in diff["changes"]:
            print(f"- {c}")


@app.command()
def history(limit: int = typer.Option(20, help="Number of recent drift runs to show.")):
    """List recent drift check runs."""
    init_db()
    rows = list_runs(limit=limit)
    if not rows:
        print("No drift runs found.")
        raise typer.Exit(0)

    for r in rows:
        print(
            f"- id={r['id']} host={r['host']} risk={r['risk_level']}({r['risk_score']}) "
            f"captured={r['captured_at']} created={r['created_at']}"
        )


@app.command()
def show(run_id: int = typer.Option(..., help="Run ID from history.")):
    """Show details for a single drift run."""
    init_db()
    r = get_run(run_id)
    if not r:
        print("Run not found.")
        raise typer.Exit(1)

    print(json.dumps(r["result"], indent=2))


def main():
    app()


if __name__ == "__main__":
    main()
