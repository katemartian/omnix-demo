from __future__ import annotations
from typing import Tuple
import re

def redact_pii(text: str, pii_regexes: list[str]) -> Tuple[str, int]:
    redacted = text
    count = 0
    for pat in pii_regexes:
        rx = re.compile(pat)
        redacted, n = rx.subn("[REDACTED]", redacted)
        count += n
    return redacted, count
