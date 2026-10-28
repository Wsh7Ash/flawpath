"""flawpath corpus: pack metadata plus 50 authored backend implementation skills.

Skills are authored as plain dicts in ``part1``..``part3`` and loaded once
into the validated :class:`~flawpath.model.Skill` shape.
"""

from __future__ import annotations

from typing import Any

from ..model import skill_from_dict
from .part1 import SKILLS as PART1
from .part2 import SKILLS as PART2
from .part3 import SKILLS as PART3

PACK: dict[str, Any] = {
    "name": "flawpath",
    "version": "1.0.0",
    "category": "backend-api",
    "license": "MIT",
    "runtime": "Claude Code, opencode, or any agent runtime that loads SKILL.md files",
    "description": (
        "50 validated backend implementation skills: route and parameter mapping, "
        "mass assignment, coercion, filtering, error and debug surfaces, "
        "concurrency and idempotency, confirmation and framework-level fixes, "
        "with a handler-inventory-to-assessment-plan CLI."
    ),
    "expected_skills": 50,
    "meta_keys": ("phase",),
    "requires_verification": False,
}

PHASE_ORDER = (
    "scope",
    "map",
    "probe",
    "confirm",
    "harden",
    "document",
)

SKILLS: list[Any] = [skill_from_dict(raw) for raw in (*PART1, *PART2, *PART3)]