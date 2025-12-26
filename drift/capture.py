from __future__ import annotations

import socket
from datetime import datetime, UTC
from typing import Dict, List, Any

DEFAULT_PORTS = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 3389, 1433, 3306]


def _probe_port(host: str, port: int, timeout: float = 0.35) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def capture_snapshot(host: str, ports: List[int] | None = None) -> Dict[str, Any]:
    ports = ports or DEFAULT_PORTS
    open_ports: List[int] = []

    for p in ports:
        if _probe_port(host, p):
            open_ports.append(p)

    return {
        "meta": {
            "captured_at": datetime.now(UTC).isoformat(),
            "host": host,
            "port_list": ports,
        },
        "observed": {
            "open_ports": sorted(open_ports),
        },
    }
