from __future__ import annotations

import math
import re
from typing import Any

DEFAULT_CONDITIONS = ("fr5", "fr10", "fr20")
DEFAULT_RATIO_REQUIREMENTS = {
    "fr5": 5,
    "fr10": 10,
    "fr20": 20,
}


def _normalize_token(value: Any) -> str:
    token = str(value if value is not None else "").strip().lower()
    return re.sub(r"[^a-z0-9]+", "", token)


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    token = str(value if value is not None else "").strip().lower()
    return token in {"1", "true", "yes", "y"}


def _as_float(value: Any) -> float | None:
    try:
        parsed = float(value)
    except Exception:
        return None
    return parsed if math.isfinite(parsed) else None


def parse_condition(condition: Any) -> str:
    if isinstance(condition, dict):
        raw = condition.get("condition") or condition.get("condition_id") or condition.get("label")
    else:
        raw = condition
    token = _normalize_token(raw)
    if not token:
        raise ValueError("trial condition is missing a condition token")
    return token


def ratio_requirement_for_condition(condition: Any, settings: Any = None) -> int:
    token = parse_condition(condition)
    mapping = dict(getattr(settings, "ratio_requirements", {}) or {})
    for key, value in mapping.items():
        if _normalize_token(key) == token:
            try:
                return int(value)
            except Exception:
                break
    if token in DEFAULT_RATIO_REQUIREMENTS:
        return int(DEFAULT_RATIO_REQUIREMENTS[token])
    match = re.search(r"(\d+)", token)
    if match:
        return int(match.group(1))
    raise ValueError(f"Unable to infer ratio requirement from condition {condition!r}")


def reward_tokens_per_completion(settings: Any = None) -> int:
    try:
        return int(getattr(settings, "reward_tokens_per_completion", 1) or 1)
    except Exception:
        return 1


def satiety_fraction(total_tokens: int, limit: int) -> float:
    if limit <= 0:
        return 0.0
    return max(0.0, min(float(total_tokens) / float(limit), 1.0))


def _trial_completion_s(row: dict[str, Any]) -> float | None:
    for key in ("work_completion_s", "completion_s", "trial_completion_s"):
        value = _as_float(row.get(key))
        if value is not None:
            return value
    return None


def _summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {
            "completion_rate": 0.0,
            "mean_completion_ms": 0.0,
            "timeout_count": 0,
            "total_tokens": 0,
            "total_trials": 0,
        }

    timeout_count = 0
    completion_count = 0
    total_tokens = 0
    completion_time_sum = 0.0
    completion_time_count = 0

    for row in rows:
        if _as_bool(row.get("work_timeout", row.get("timed_out", False))):
            timeout_count += 1
        if _as_bool(row.get("reward_delivered", False)):
            completion_count += 1
            completion_s = _trial_completion_s(row)
            if completion_s is not None:
                completion_time_sum += completion_s
                completion_time_count += 1
        total_tokens = max(total_tokens, int(row.get("total_tokens_after", row.get("score_total", total_tokens)) or total_tokens))

    completion_rate = completion_count / len(rows)
    mean_completion_ms = (completion_time_sum / completion_time_count) * 1000.0 if completion_time_count else 0.0
    return {
        "completion_rate": completion_rate,
        "mean_completion_ms": mean_completion_ms,
        "timeout_count": timeout_count,
        "total_tokens": total_tokens,
        "total_trials": len(rows),
    }


def summarizeBlock(reducedRows: list[dict[str, Any]], blockId: str) -> dict[str, Any]:
    rows = [row for row in reducedRows if str(row.get("block_id", "")) == str(blockId)]
    return _summarize(rows)


def summarizeOverall(reducedRows: list[dict[str, Any]]) -> dict[str, Any]:
    return _summarize(list(reducedRows))


__all__ = [
    "DEFAULT_CONDITIONS",
    "DEFAULT_RATIO_REQUIREMENTS",
    "parse_condition",
    "ratio_requirement_for_condition",
    "reward_tokens_per_completion",
    "satiety_fraction",
    "summarizeBlock",
    "summarizeOverall",
]
