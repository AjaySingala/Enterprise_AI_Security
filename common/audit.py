"""
===============================================================================
Enterprise AI Gateway (EAIG)

Audit Service

Version:
    1.0.0

Python:
    3.13.11
===============================================================================
"""

from __future__ import annotations

import json

from dataclasses import asdict
from dataclasses import dataclass

from datetime import datetime
from pathlib import Path
from threading import Lock

###############################################################################
# Record
###############################################################################
@dataclass(slots=True)
class AuditRecord:
    timestamp: str
    request_id: str
    client_ip: str
    decision: str
    pii_count: int
    secret_count: int
    confidential_count: int
    processing_time_ms: float

###############################################################################
# Service
###############################################################################
class AuditService:
    def __init__(self):
        self.audit_folder = Path("audit")
        self.audit_folder.mkdir(
            exist_ok=True,
        )
        self._lock = Lock()

    ###########################################################################
    def write(
        self,
        record: AuditRecord,
    ) -> None:
        filename = (
            datetime.now()
            .strftime("%Y-%m-%d")
            + ".jsonl"
        )

        path = self.audit_folder / filename

        with self._lock:
            with open(
                path,
                "a",
                encoding="utf-8",
            ) as fp:
                fp.write(
                    json.dumps(
                        asdict(record),
                    )
                )

                fp.write("\n")
