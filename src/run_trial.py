from __future__ import annotations

import json
from functools import partial
from statistics import mean
from typing import Any

from psyflow import StimUnit, next_trial_id, set_trial_context

from .utils import (
    parse_condition,
    ratio_requirement_for_condition,
    reward_tokens_per_completion,
    satiety_fraction,
)


def _get_setting(settings: Any, *names: str, default: Any = None) -> Any:
    for name in names:
        if hasattr(settings, name):
            value = getattr(settings, name)
            if value is not None:
                return value
    return default


def _condition_dict(condition: Any, settings: Any) -> dict[str, Any]:
    if isinstance(condition, dict):
        data = dict(condition)
    else:
        data = {"condition": condition}

    condition_id = parse_condition(data)
    ratio_requirement = data.get("ratio_requirement")
    if ratio_requirement is None:
        ratio_requirement = ratio_requirement_for_condition(condition_id, settings)

    try:
        ratio_requirement = int(ratio_requirement)
    except Exception as exc:
        raise ValueError(f"Invalid ratio requirement for condition {condition!r}") from exc

    return {
        "condition": condition_id,
        "condition_id": condition_id,
        "ratio_requirement": ratio_requirement,
    }


def _stim_ids(ids: list[str]) -> str:
    return "+".join(ids)


def _make_text_unit(
    *,
    win,
    kb,
    trigger_runtime,
    unit_label: str,
    stim_bank,
    stim_ids: list[str],
    phase: str,
    trial_id: int,
    block_id: str,
    condition_id: str,
    deadline_s: float | None,
    valid_keys: list[str],
    task_factors: dict[str, Any],
):
    unit = StimUnit(unit_label, win, kb, runtime=trigger_runtime)
    set_trial_context(
        unit,
        trial_id=trial_id,
        phase=phase,
        deadline_s=deadline_s,
        valid_keys=valid_keys,
        block_id=block_id,
        condition_id=condition_id,
        task_factors=task_factors,
        stim_id=_stim_ids(stim_ids),
    )
    return unit


def _resolve_block_id(block_id: Any, block_num: int, block_kind: str = "block") -> str:
    if block_id is not None:
        return str(block_id)
    return f"{block_kind}_{block_num:02d}"


def run_trial(
    win,
    kb,
    settings,
    condition,
    stim_bank,
    trigger_runtime,
    block_id=None,
    block_idx=None,
    block_seed=None,
):
    """Run one fixed-ratio satiation trial."""

    trial_id = int(next_trial_id())
    trial_spec = _condition_dict(condition, settings)
    condition_id = str(trial_spec["condition_id"])
    ratio_requirement = int(trial_spec["ratio_requirement"])

    block_idx_value = int(block_idx if block_idx is not None else 0)
    block_num_value = block_idx_value + 1
    block_id_value = _resolve_block_id(block_id, block_num_value, "block")

    press_timeout = float(_get_setting(settings, "press_timeout", default=1.2))
    reward_duration = float(_get_setting(settings, "reward_duration", default=0.9))
    satiation_duration = float(_get_setting(settings, "satiation_duration", default=1.2))
    iti_duration = float(_get_setting(settings, "iti_duration", default=0.8))
    satiety_limit = int(_get_setting(settings, "satiation_limit", default=12) or 12)
    reward_tokens = reward_tokens_per_completion(settings)
    total_tokens_before = int(getattr(settings, "token_total", 0) or 0)
    satiety_before = satiety_fraction(total_tokens_before, satiety_limit)
    response_key = str(_get_setting(settings, "response_key", default="space")).strip().lower()

    trial_data: dict[str, Any] = {
        "trial_id": trial_id,
        "block_id": block_id_value,
        "block_idx": block_idx_value,
        "block_num": block_num_value,
        "condition": condition_id,
        "condition_id": condition_id,
        "ratio_requirement": ratio_requirement,
        "presses_required": ratio_requirement,
        "presses_completed": 0,
        "work_timeout": False,
        "reward_delivered": False,
        "reward_tokens": 0,
        "reward_tokens_before": total_tokens_before,
        "total_tokens_before": total_tokens_before,
        "total_tokens_after": total_tokens_before,
        "satiety_fraction_before": satiety_before,
        "satiety_fraction_after": satiety_before,
        "work_completion_s": None,
        "first_press_rt_s": None,
        "last_press_rt_s": None,
        "mean_press_rt_s": None,
        "press_trace_json": "[]",
        "response_key": response_key,
    }

    press_events: list[dict[str, Any]] = []
    press_rts: list[float] = []
    first_onset_global: float | None = None
    last_response_global: float | None = None
    work_timeout = False

    work_preview_duration = min(0.6, press_timeout)
    work_preview = StimUnit("work_preview", win, kb, runtime=trigger_runtime)
    work_preview.add_stim(
        stim_bank.get_and_format(
            "work_prompt",
            required_presses=ratio_requirement,
        )
    )
    work_preview.add_stim(
        stim_bank.get_and_format(
            "work_counter",
            current_press=0,
            required_presses=ratio_requirement,
        )
    )
    work_preview.add_stim(
        stim_bank.get_and_format(
            "satiety_text",
            satiety_pct=satiety_before,
        )
    )
    work_preview.add_stim(stim_bank.get("fixation"))
    set_trial_context(
        work_preview,
        trial_id=trial_id,
        phase="work_preview",
        deadline_s=work_preview_duration,
        valid_keys=[],
        block_id=block_id_value,
        condition_id=condition_id,
        task_factors={
            "stage": "work_preview",
            "condition": condition_id,
            "ratio_requirement": ratio_requirement,
            "token_total_before": total_tokens_before,
            "satiety_fraction_before": satiety_before,
            "block_idx": block_idx_value,
            "block_num": block_num_value,
        },
        stim_id="work_prompt+work_counter+satiety_text+fixation",
    )
    work_preview.show(duration=work_preview_duration, onset_trigger=settings.triggers.get("trial_onset"))

    for press_index in range(1, ratio_requirement + 1):
        completed_before = press_index - 1
        press_phase = "work_press"
        press_unit_label = f"work_press_{press_index:02d}"
        press_unit = _make_text_unit(
            win=win,
            kb=kb,
            trigger_runtime=trigger_runtime,
            unit_label=press_unit_label,
            stim_bank=stim_bank,
            stim_ids=["work_prompt", "work_counter", "satiety_text", "fixation"],
            phase=press_phase,
            trial_id=trial_id,
            block_id=block_id_value,
            condition_id=condition_id,
            deadline_s=press_timeout,
            valid_keys=[response_key],
            task_factors={
                "stage": press_phase,
                "condition": condition_id,
                "ratio_requirement": ratio_requirement,
                "press_index": press_index,
                "presses_completed_before": completed_before,
                "presses_remaining": ratio_requirement - completed_before,
                "token_total_before": total_tokens_before,
                "satiety_fraction_before": satiety_before,
                "block_idx": block_idx_value,
                "block_num": block_num_value,
            },
        )
        press_unit.add_stim(
            stim_bank.get_and_format(
                "work_prompt",
                required_presses=ratio_requirement,
            )
        )
        press_unit.add_stim(
            stim_bank.get_and_format(
                "work_counter",
                current_press=completed_before,
                required_presses=ratio_requirement,
            )
        )
        press_unit.add_stim(
            stim_bank.get_and_format(
                "satiety_text",
                satiety_pct=satiety_before,
            )
        )
        press_unit.add_stim(stim_bank.get("fixation"))

        press_unit.capture_response(
            keys=[response_key],
            duration=press_timeout,
            onset_trigger=settings.triggers.get("press_onset"),
            response_trigger=settings.triggers.get("press_response"),
            timeout_trigger=settings.triggers.get("press_timeout"),
            correct_keys=[response_key],
            terminate_on_response=True,
        )

        onset_global = press_unit.get_state("onset_time_global", None)
        if first_onset_global is None and isinstance(onset_global, (int, float)):
            first_onset_global = float(onset_global)

        response_key_pressed = press_unit.get_state("response", None)
        response_rt = press_unit.get_state("rt", None)
        response_time_global = press_unit.get_state("response_time_global", None)
        response_hit = bool(press_unit.get_state("hit", False))

        if response_hit:
            try:
                press_rts.append(float(response_rt))
            except Exception:
                pass
            if isinstance(response_time_global, (int, float)):
                last_response_global = float(response_time_global)
            press_events.append(
                {
                    "press_index": press_index,
                    "response": str(response_key_pressed or ""),
                    "rt_s": float(response_rt) if isinstance(response_rt, (int, float)) else None,
                    "hit": True,
                    "timed_out": False,
                }
            )
            trial_data["presses_completed"] = press_index
            continue

        work_timeout = True
        press_events.append(
            {
                "press_index": press_index,
                "response": str(response_key_pressed or ""),
                "rt_s": float(response_rt) if isinstance(response_rt, (int, float)) else None,
                "hit": False,
                "timed_out": True,
            }
        )
        break

    reward_delivered = False
    total_tokens_after = total_tokens_before
    satiety_after = satiety_before

    if not work_timeout and trial_data["presses_completed"] >= ratio_requirement:
        reward_delivered = True
        total_tokens_after = total_tokens_before + reward_tokens
        satiety_after = satiety_fraction(total_tokens_after, satiety_limit)
        settings.token_total = total_tokens_after

        work_completion_s = None
        if first_onset_global is not None and last_response_global is not None:
            work_completion_s = max(0.0, float(last_response_global) - float(first_onset_global))

        trial_data.update(
            {
                "work_completion_s": work_completion_s,
                "reward_delivered": True,
                "reward_tokens": reward_tokens,
                "total_tokens_after": total_tokens_after,
                "satiety_fraction_after": satiety_after,
                "first_press_rt_s": press_rts[0] if press_rts else None,
                "last_press_rt_s": press_rts[-1] if press_rts else None,
                "mean_press_rt_s": mean(press_rts) if press_rts else None,
            }
        )

        reward_unit = _make_text_unit(
            win=win,
            kb=kb,
            trigger_runtime=trigger_runtime,
            unit_label="reward_delivery",
            stim_bank=stim_bank,
            stim_ids=["reward_text", "reward_token", "satiety_text"],
            phase="reward_delivery",
            trial_id=trial_id,
            block_id=block_id_value,
            condition_id=condition_id,
            deadline_s=reward_duration,
            valid_keys=[],
            task_factors={
                "stage": "reward_delivery",
                "condition": condition_id,
                "ratio_requirement": ratio_requirement,
                "reward_tokens": reward_tokens,
                "token_total_before": total_tokens_before,
                "token_total_after": total_tokens_after,
                "satiety_fraction_after": satiety_after,
            },
        )
        reward_unit.add_stim(
            stim_bank.get_and_format(
                "reward_text",
                reward_tokens=reward_tokens,
            )
        )
        reward_unit.add_stim(stim_bank.get("reward_token"))
        reward_unit.add_stim(
            stim_bank.get_and_format(
                "satiety_text",
                satiety_pct=satiety_after,
            )
        )
        reward_unit.show(duration=reward_duration, onset_trigger=settings.triggers.get("reward_onset"))

        satiation_unit = _make_text_unit(
            win=win,
            kb=kb,
            trigger_runtime=trigger_runtime,
            unit_label="satiation_pause",
            stim_bank=stim_bank,
            stim_ids=["satiety_text", "fixation"],
            phase="satiation_pause",
            trial_id=trial_id,
            block_id=block_id_value,
            condition_id=condition_id,
            deadline_s=satiation_duration,
            valid_keys=[],
            task_factors={
                "stage": "satiation_pause",
                "condition": condition_id,
                "ratio_requirement": ratio_requirement,
                "token_total_after": total_tokens_after,
                "satiety_fraction_after": satiety_after,
            },
        )
        satiation_unit.add_stim(
            stim_bank.get_and_format(
                "satiety_text",
                satiety_pct=satiety_after,
            )
        )
        satiation_unit.add_stim(stim_bank.get("fixation"))
        satiation_unit.show(duration=satiation_duration, onset_trigger=settings.triggers.get("satiation_onset"))
    else:
        trial_data.update(
            {
                "work_timeout": True,
                "reward_delivered": False,
                "reward_tokens": 0,
                "total_tokens_after": total_tokens_after,
                "satiety_fraction_after": satiety_after,
                "first_press_rt_s": press_rts[0] if press_rts else None,
                "last_press_rt_s": press_rts[-1] if press_rts else None,
                "mean_press_rt_s": mean(press_rts) if press_rts else None,
            }
        )
        timeout_unit = _make_text_unit(
            win=win,
            kb=kb,
            trigger_runtime=trigger_runtime,
            unit_label="timeout_feedback",
            stim_bank=stim_bank,
            stim_ids=["timeout_text", "fixation"],
            phase="timeout_feedback",
            trial_id=trial_id,
            block_id=block_id_value,
            condition_id=condition_id,
            deadline_s=reward_duration,
            valid_keys=[],
            task_factors={
                "stage": "timeout_feedback",
                "condition": condition_id,
                "ratio_requirement": ratio_requirement,
                "presses_completed": trial_data["presses_completed"],
                "token_total_after": total_tokens_after,
            },
        )
        timeout_unit.add_stim(stim_bank.get("timeout_text"))
        timeout_unit.add_stim(stim_bank.get("fixation"))
        timeout_unit.show(duration=reward_duration)

    iti_unit = _make_text_unit(
        win=win,
        kb=kb,
        trigger_runtime=trigger_runtime,
        unit_label="iti",
        stim_bank=stim_bank,
        stim_ids=["fixation"],
        phase="iti",
        trial_id=trial_id,
        block_id=block_id_value,
        condition_id=condition_id,
        deadline_s=iti_duration,
        valid_keys=[],
        task_factors={
            "stage": "iti",
            "condition": condition_id,
            "ratio_requirement": ratio_requirement,
            "presses_completed": trial_data["presses_completed"],
            "token_total_after": total_tokens_after,
        },
    )
    iti_unit.add_stim(stim_bank.get("fixation"))
    iti_unit.show(duration=iti_duration, onset_trigger=settings.triggers.get("iti_onset"))

    trial_data.update(
        {
            "press_trace_json": json.dumps(press_events, ensure_ascii=False),
            "work_timeout": work_timeout,
            "reward_delivered": reward_delivered,
            "reward_tokens": reward_tokens if reward_delivered else 0,
            "total_tokens_before": total_tokens_before,
            "total_tokens_after": total_tokens_after,
            "satiety_fraction_before": satiety_before,
            "satiety_fraction_after": satiety_after,
            "work_completion_s": trial_data.get("work_completion_s"),
            "presses_completed": int(trial_data.get("presses_completed", 0)),
        }
    )

    return trial_data


__all__ = ["run_trial"]
