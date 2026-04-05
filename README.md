# Fixed-ratio Satiation Schedule

![Maturity: draft](https://img.shields.io/badge/Maturity-draft-64748b?style=flat-square&labelColor=111827)

| Field | Value |
|---|---|
| Name | Fixed-ratio Satiation Schedule |
| Version | v0.1.0-dev |
| URL / Repository | E:/Taskbeacon/T000041-fixed-ratio-satiation-schedule |
| Short Description | Chinese fixed-ratio pressing task with three effort requirements (FR5, FR10, FR20) and an accumulating satiety meter. |
| Created By | TaskBeacon |
| Date Updated | 2026-04-05 |
| PsyFlow Version | 0.1.12 |
| PsychoPy Version | 2025.2.4 |
| Modality | Behavior |
| Language | Chinese |
| Voice Name | zh-CN-YunyangNeural |

## 1. Task Overview

This task measures effort-based responding under a fixed-ratio operant schedule. On each trial, participants press the space bar repeatedly until they satisfy the condition-specific ratio requirement. The three trial conditions are `fr5`, `fr10`, and `fr20`, which require 5, 10, and 20 presses respectively.

Each successful completion delivers one token and increases the running satiety signal. Satiety is displayed as a percentage of a 12-token limit, so the participant sees the reward accumulation curve grow across the session. The human schedule contains 3 blocks of 18 trials each for a total of 54 trials.

The task is designed to capture motivation, persistence, and reward accumulation as the effort requirement increases. The implementation uses Chinese participant-facing text and PsychoPy primitive stimuli only.

## 2. Task Flow

![Task Flow](task_flow.png)

### Block-Level Flow

| Step | Description |
|---|---|
| 1. Load mode and config | `main.py` loads `human`, `qa`, or `sim` mode and resolves the matching YAML config. |
| 2. Initialize runtime | Subject info, window, triggers, and the stimulus bank are initialized. |
| 3. Show instructions | The participant reads the Chinese instruction screen and starts with the space key. |
| 4. Run blocks | Human mode runs 3 blocks with 18 trials per block; QA and simulation modes use shorter smoke-test schedules. |
| 5. Show block break | A summary screen appears between blocks and reports completion rate, mean completion time, and total tokens. |
| 6. Finish | The goodbye screen appears and all trial data are saved. |

### Trial-Level Flow

| Step | Description |
|---|---|
| Work preview | A brief preview screen shows the required press count, current counter, satiety, and fixation before responding starts. |
| Work press window | Repeated press windows show the prompt, press counter, satiety, and fixation. Each valid space press advances the counter by one. |
| Reward delivery | After the required number of presses is completed, a reward screen shows the token, reward text, and updated satiety. |
| Satiation pause | A short pause screen keeps satiety visible before the next trial begins. |
| Timeout feedback | If a press window expires before the ratio is met, a timeout screen appears instead of reward delivery. |
| Inter-trial interval | Every trial ends with a fixation-only ITI screen before the next condition begins. |

### Controller Logic

| Component | Description |
|---|---|
| Condition generation | `BlockUnit.generate_conditions()` produces `fr5`, `fr10`, and `fr20` with equal weights. |
| Ratio mapping | The ratio requirements are 5, 10, and 20 presses for `fr5`, `fr10`, and `fr20`. |
| Reward accounting | Each successful completion gives 1 token and increments `token_total`. |
| Satiety model | Satiety is computed as `total_tokens / 12` and clamped to the range `[0, 1]`. |
| Block seeds | The three human blocks use deterministic seeds `41041`, `41042`, and `41043`. |
| Summary outputs | Block and overall summaries report completion rate, mean completion time, timeout count, total tokens, and trial count. |

### Other Logic

| Component | Description |
|---|---|
| Response key | The only task response key is the space bar. |
| Human pacing | Human mode uses a 3-second countdown before each block. |
| QA/sim scope | QA and simulation modes reuse the same state machine with shortened schedules so the same logic can be validated quickly. |
| Data capture | Trial records include press traces, response RTs, reward flags, token totals, and satiety before/after each trial. |

## 3. Configuration Summary

All human settings are defined in `config/config.yaml`. QA and smoke-test overrides live in `config/config_qa.yaml`, `config/config_scripted_sim.yaml`, and `config/config_sampler_sim.yaml`.

### a. Subject Info

| Field | Meaning |
|---|---|
| `subject_id` | 3-digit participant identifier used to seed the run. |

### b. Window Settings

| Parameter | Value |
|---|---|
| `size` | `[1280, 720]` |
| `units` | `pix` |
| `screen` | `0` |
| `bg_color` | `black` |
| `fullscreen` | `false` |
| `monitor_width_cm` | `35.5` |
| `monitor_distance_cm` | `60` |

### c. Stimuli

| Name | Type | Description |
|---|---|---|
| `instruction_text` | text | Chinese instructions that explain the fixed-ratio pressing rule and the space-key response. |
| `block_ready` | text | Block-start text kept in config; human mode currently uses a 3-second countdown helper before each block. |
| `work_prompt` | text | Shows the required number of presses for the current trial. |
| `work_counter` | text | Shows the current press count out of the requirement. |
| `satiety_text` | text | Shows the current satiety percentage. |
| `fixation` | text | Centered plus sign used during work, feedback, and ITI screens. |
| `reward_token` | circle | Gold token drawn on the reward screen. |
| `reward_text` | text | Reward confirmation that indicates a token has been delivered. |
| `timeout_text` | text | Timeout feedback shown when a press window closes before completion. |
| `block_break` | text | Block summary with completion rate, mean completion time, and total tokens. |
| `good_bye` | text | Session-end summary and exit prompt. |

### d. Timing

| Phase | Duration |
|---|---|
| Instruction pause | `0.0 s` |
| Ready / countdown | `3.0 s` |
| Press timeout | `1.2 s` |
| Reward display | `0.9 s` |
| Satiation pause | `1.2 s` |
| Inter-trial interval | `0.8 s` |
| Block break | `3.0 s` |

### e. Triggers

| Event | Code |
|---|---:|
| Experiment onset | `1` |
| Experiment end | `2` |
| Block onset | `10` |
| Block end | `11` |
| Trial onset | `20` |
| Press onset | `21` |
| Press response | `22` |
| Press timeout | `23` |
| Reward onset | `30` |
| Satiation onset | `31` |
| ITI onset | `40` |

### f. Adaptive Controller

| Parameter | Value |
|---|---|
| `phase_order` | `instruction -> work -> reward -> satiation -> iti` |
| `conditions` | `fr5`, `fr10`, `fr20` |
| `condition_weights` | `1, 1, 1` |
| `ratio_requirements` | `fr5=5`, `fr10=10`, `fr20=20` |
| `total_blocks` | `3` in human mode, `1` in QA and simulation modes |
| `trial_per_block` | `18` in human mode, `3` in QA and simulation modes |
| `total_trials` | `54` in human mode, `3` in QA and simulation modes |
| `satiation_limit` | `12` tokens |
| `reward_tokens_per_completion` | `1` |
| `response_key` | `space` |
| `seed_mode` | `same_across_sub` |
| `block_seed` | `41041`, `41042`, `41043` |
| `delta` | `1` token per successful completion |
| `QA acceptance` | `condition`, `ratio_requirement`, and `presses_completed` must be present in the QA trace |

## 4. Methods (for academic publication)

Fixed-ratio satiation schedules are used to study effort allocation, persistence, and reward accumulation under increasing response requirements. In this implementation, each trial requires repeated space-bar presses to satisfy one of three fixed-ratio contingencies: FR5, FR10, or FR20. Successful completion delivers one token, and the cumulative token count is converted into a satiety signal that grows across the session.

The task is organized into three balanced blocks in human mode, with shortened QA and simulation profiles that preserve the same state machine for validation. The trial sequence is a work preview, repeated work windows, reward delivery or timeout feedback, satiation pause, and ITI. Performance is summarized using completion rate, completion time, timeout count, and total token accumulation, making the paradigm suitable for behavioral studies of motivation and effort-based responding.
