# Task Plot Audit

- generated_at: 2026-04-05T13:55:16
- mode: existing
- task_path: E:\Taskbeacon\T000041-fixed-ratio-satiation-schedule

## 1. Inputs and provenance

- E:\Taskbeacon\T000041-fixed-ratio-satiation-schedule\README.md
- E:\Taskbeacon\T000041-fixed-ratio-satiation-schedule\config\config.yaml
- E:\Taskbeacon\T000041-fixed-ratio-satiation-schedule\src\run_trial.py

## 2. Evidence extracted from README

- | Step | Description |
- |---|---|
- | Block ready | A centered ready screen appears for `3.0 s` before each block. |
- | Choice screen | Two kana symbols appear left and right; the participant responds with the left or right key within `4.0 s`. |
- | Feedback, learning only | A probabilistic `正确` or `错误` screen appears for `1.0 s` based on the chosen role's reward probability. |
- | No-feedback transfer | Transfer trials skip feedback and go straight to the inter-trial interval. |
- | Inter-trial interval | A fixation `+` appears for `1.0 s` before the next trial. |

## 3. Evidence extracted from config/source

- fr5: phase=work preview, deadline_expr=work_preview_duration, response_expr=n/a, stim_expr='work_prompt+work_counter+satiety_text+fixation'
- fr5: visible_show_without_context phase=reward_text, unit_label_expr=(none), duration_expr=reward_duration, stim_exprs=["stim_bank.get_and_format('reward_text', reward_tokens=reward_tokens)", "stim_bank.get('reward_token')", "stim_bank.get_and_format('satiety_text', satiety_pct=satiety_after)"]
- fr5: visible_show_without_context phase=satiety_text, unit_label_expr=(none), duration_expr=satiation_duration, stim_exprs=["stim_bank.get_and_format('satiety_text', satiety_pct=satiety_after)", "stim_bank.get('fixation')"]
- fr5: visible_show_without_context phase=timeout_text, unit_label_expr=(none), duration_expr=reward_duration, stim_exprs=["stim_bank.get('timeout_text')", "stim_bank.get('fixation')"]
- fr5: visible_show_without_context phase=fixation, unit_label_expr=(none), duration_expr=iti_duration, stim_exprs=["stim_bank.get('fixation')"]
- fr10: phase=work preview, deadline_expr=work_preview_duration, response_expr=n/a, stim_expr='work_prompt+work_counter+satiety_text+fixation'
- fr10: visible_show_without_context phase=reward_text, unit_label_expr=(none), duration_expr=reward_duration, stim_exprs=["stim_bank.get_and_format('reward_text', reward_tokens=reward_tokens)", "stim_bank.get('reward_token')", "stim_bank.get_and_format('satiety_text', satiety_pct=satiety_after)"]
- fr10: visible_show_without_context phase=satiety_text, unit_label_expr=(none), duration_expr=satiation_duration, stim_exprs=["stim_bank.get_and_format('satiety_text', satiety_pct=satiety_after)", "stim_bank.get('fixation')"]
- fr10: visible_show_without_context phase=timeout_text, unit_label_expr=(none), duration_expr=reward_duration, stim_exprs=["stim_bank.get('timeout_text')", "stim_bank.get('fixation')"]
- fr10: visible_show_without_context phase=fixation, unit_label_expr=(none), duration_expr=iti_duration, stim_exprs=["stim_bank.get('fixation')"]
- fr20: phase=work preview, deadline_expr=work_preview_duration, response_expr=n/a, stim_expr='work_prompt+work_counter+satiety_text+fixation'
- fr20: visible_show_without_context phase=reward_text, unit_label_expr=(none), duration_expr=reward_duration, stim_exprs=["stim_bank.get_and_format('reward_text', reward_tokens=reward_tokens)", "stim_bank.get('reward_token')", "stim_bank.get_and_format('satiety_text', satiety_pct=satiety_after)"]
- fr20: visible_show_without_context phase=satiety_text, unit_label_expr=(none), duration_expr=satiation_duration, stim_exprs=["stim_bank.get_and_format('satiety_text', satiety_pct=satiety_after)", "stim_bank.get('fixation')"]
- fr20: visible_show_without_context phase=timeout_text, unit_label_expr=(none), duration_expr=reward_duration, stim_exprs=["stim_bank.get('timeout_text')", "stim_bank.get('fixation')"]
- fr20: visible_show_without_context phase=fixation, unit_label_expr=(none), duration_expr=iti_duration, stim_exprs=["stim_bank.get('fixation')"]

## 3b. Warnings

- fr5:reward_text: participant-visible phase inferred from show() because set_trial_context(...) is missing
- fr5:satiety_text: participant-visible phase inferred from show() because set_trial_context(...) is missing
- fr5:timeout_text: participant-visible phase inferred from show() because set_trial_context(...) is missing
- fr5:fixation: participant-visible phase inferred from show() because set_trial_context(...) is missing
- fr10:reward_text: participant-visible phase inferred from show() because set_trial_context(...) is missing
- fr10:satiety_text: participant-visible phase inferred from show() because set_trial_context(...) is missing
- fr10:timeout_text: participant-visible phase inferred from show() because set_trial_context(...) is missing
- fr10:fixation: participant-visible phase inferred from show() because set_trial_context(...) is missing
- fr20:reward_text: participant-visible phase inferred from show() because set_trial_context(...) is missing
- fr20:satiety_text: participant-visible phase inferred from show() because set_trial_context(...) is missing
- fr20:timeout_text: participant-visible phase inferred from show() because set_trial_context(...) is missing
- fr20:fixation: participant-visible phase inferred from show() because set_trial_context(...) is missing

## 4. Mapping to task_plot_spec

- timeline collection: one representative timeline per unique trial logic
- phase flow inferred from run_trial set_trial_context order and branch predicates
- participant-visible show() phases without set_trial_context are inferred where possible and warned
- duration/response inferred from deadline/capture expressions
- stimulus examples inferred from stim_id + config stimuli
- conditions with equivalent phase/timing logic collapsed and annotated as variants
- root_key: task_plot_spec
- spec_version: 0.2

## 5. Style decision and rationale

- Single timeline-collection view selected by policy: one representative condition per unique timeline logic.

## 6. Rendering parameters and constraints

- output_file: task_flow.png
- dpi: 300
- max_conditions: 3
- screens_per_timeline: 5
- screen_overlap_ratio: 0.1
- screen_slope: 0.08
- screen_slope_deg: 25.0
- screen_aspect_ratio: 1.4545454545454546
- qa_mode: local
- auto_layout_feedback:
  - layout pass 1: crop-only; left=0.031, right=0.033, blank=0.119
- auto_layout_feedback_records:
  - pass: 1
    metrics: {'left_ratio': 0.0308, 'right_ratio': 0.0331, 'blank_ratio': 0.1192}

## 7. Output files and checksums

- E:\Taskbeacon\T000041-fixed-ratio-satiation-schedule\references\task_plot_spec.yaml: sha256=f55fb647f688837e73cfdd7666a65b311e1ee44c1b74f9d1a3b6986c56c1bf87
- E:\Taskbeacon\T000041-fixed-ratio-satiation-schedule\references\task_plot_spec.json: sha256=9cbdd855175303521f8fe88f95f508b7cbcb62a04c87c6ed8ae78872b51886a5
- E:\Taskbeacon\T000041-fixed-ratio-satiation-schedule\references\task_plot_source_excerpt.md: sha256=7710f42378e719e583f4204046d23270dbbf9a17e29204cb8d277b19be0a1a40
- E:\Taskbeacon\T000041-fixed-ratio-satiation-schedule\task_flow.png: sha256=b10231eccdef69fc45a7713e15a42a1071a3dd433c05afb9c2277d438181fdf2

## 8. Inferred/uncertain items

- fr5:work preview:heuristic numeric parse from 'min(0.6, press_timeout)'
- fr5:reward_text:heuristic numeric parse from 'float(_get_setting(settings, 'reward_duration', default=0.9))'
- fr5:satiety_text:heuristic numeric parse from 'float(_get_setting(settings, 'satiation_duration', default=1.2))'
- fr5:timeout_text:heuristic numeric parse from 'float(_get_setting(settings, 'reward_duration', default=0.9))'
- fr5:fixation:heuristic numeric parse from 'float(_get_setting(settings, 'iti_duration', default=0.8))'
- fr10:work preview:heuristic numeric parse from 'min(0.6, press_timeout)'
- fr10:reward_text:heuristic numeric parse from 'float(_get_setting(settings, 'reward_duration', default=0.9))'
- fr10:satiety_text:heuristic numeric parse from 'float(_get_setting(settings, 'satiation_duration', default=1.2))'
- fr10:timeout_text:heuristic numeric parse from 'float(_get_setting(settings, 'reward_duration', default=0.9))'
- fr10:fixation:heuristic numeric parse from 'float(_get_setting(settings, 'iti_duration', default=0.8))'
- fr20:work preview:heuristic numeric parse from 'min(0.6, press_timeout)'
- fr20:reward_text:heuristic numeric parse from 'float(_get_setting(settings, 'reward_duration', default=0.9))'
- fr20:satiety_text:heuristic numeric parse from 'float(_get_setting(settings, 'satiation_duration', default=1.2))'
- fr20:timeout_text:heuristic numeric parse from 'float(_get_setting(settings, 'reward_duration', default=0.9))'
- fr20:fixation:heuristic numeric parse from 'float(_get_setting(settings, 'iti_duration', default=0.8))'
- collapsed equivalent condition logic into representative timeline: fr5, fr10, fr20
- unparsed if-tests defaulted to condition-agnostic applicability: first_onset_global is None; isinstance(onset_global, (int, float)); first_onset_global is not None; last_response_global is not None; isinstance(response_time_global, (int, float)); not work_timeout; trial_data['presses_completed'] >= ratio_requirement; response_hit
