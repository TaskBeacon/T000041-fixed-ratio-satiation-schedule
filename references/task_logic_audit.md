# Task Logic Audit

## 1. Paradigm Intent

- Task: Fixed-ratio Satiation Schedule
- Primary construct: effort allocation under a fixed-ratio reinforcement schedule while cumulative reward value is indexed by satiation
- Manipulated factors:
  - fixed-ratio requirement per trial (`fr5`, `fr10`, `fr20`)
  - cumulative satiety state across the session
- Dependent measures:
  - press completion rate
  - completion latency per ratio trial
  - timeout rate
  - reward-token accumulation
  - satiety fraction at reward delivery
- Key citations:
  - `W1964652787` Fixed-ratio pausing: joint effects of past reinforcer magnitude and stimuli correlated with upcoming magnitude
  - `W2037578646` Response rate viewed as engagement bouts: effects of relative reinforcement and schedule type
  - `W2167077741` Establishing operations and reinforcement effects
  - `W2029549266` Hippocampal GLP-1 Receptors Influence Food Intake, Meal Size, and Effort-Based Responding for Food through Volume Transmission
  - `W2168128112` The Novel Cannabinoid CB1 Receptor Neutral Antagonist AM4113 Suppresses Food Intake and Food-Reinforced Behavior but Does not Induce Signs of Nausea in Rats
  - `W2077496630` The Glucagon-Like Peptide 1 (GLP-1) Analogue, Exendin-4, Decreases the Rewarding Value of Food: A New Role for Mesolimbic GLP-1 Receptors
  - `W2164961539` Dopamine Modulates Reward-Related Vigor
  - `W1980196077` Dopamine Antagonism Decreases Willingness to Expend Physical, But Not Cognitive, Effort: A Comparison of Two Rodent Cost/Benefit Decision-Making Tasks

## 2. Block/Trial Workflow

### Block Structure

- Total blocks: 3 in the human config; QA/sim configs use shortened one-block probes
- Trials per block: 18 in the human config; 3 in QA/sim
- Randomization/counterbalancing:
  - `BlockUnit.generate_conditions(...)` is used
  - trial labels are balanced across the three fixed-ratio conditions
- Condition weight policy:
  - No custom weighting is required
  - `task.condition_weights` is defined as an even mapping in config
  - runtime can rely on `TaskSettings.resolve_condition_weights()` if needed
- Condition generation method:
  - built-in `BlockUnit.generate_conditions(...)`
  - the label passed into `run_trial.py` is a simple condition token (`fr5`, `fr10`, `fr20`)
- Runtime-generated trial values:
  - `run_trial.py` resolves `ratio_requirement` from the condition token
  - `run_trial.py` accumulates per-press reaction times and satiety fraction
  - generation is deterministic because values are derived from the condition label and the running satiety counter, not from hidden state

### Trial State Machine

1. `work_press`
   - Onset trigger: `trial_onset` on the first press window of the trial; `press_onset` on each press window
   - Stimuli shown: work prompt, press counter, satiety text, and a neutral center fixation
   - Valid keys: `space`
   - Timeout behavior: if any press window times out before the required count is met, the trial ends without reward
   - Next state: `reward_delivery` when the required count is reached, otherwise `timeout_feedback` or direct ITI

2. `reward_delivery`
   - Onset trigger: `reward_onset`
   - Stimuli shown: gold reward token and reward text
   - Valid keys: none
   - Timeout behavior: fixed-duration display
   - Next state: `satiation_pause`

3. `satiation_pause`
   - Onset trigger: `satiation_onset`
   - Stimuli shown: satiety text only
   - Valid keys: none
   - Timeout behavior: fixed-duration display
   - Next state: `iti`

4. `iti`
   - Onset trigger: `iti_onset`
   - Stimuli shown: fixation only
   - Valid keys: none
   - Timeout behavior: fixed-duration display
   - Next state: next trial

## 3. Condition Semantics

For each condition token in `task.conditions`:

- Condition ID: `fr5`
  - Participant-facing meaning: press the space bar 5 times to earn the token
  - Concrete stimulus realization (visual/audio): text prompt with `5` in the requirement line; cumulative satiety text updates after reward delivery
  - Outcome rules: reward is delivered only when 5 space presses are completed before the per-press timeout expires

- Condition ID: `fr10`
  - Participant-facing meaning: press the space bar 10 times to earn the token
  - Concrete stimulus realization (visual/audio): text prompt with `10` in the requirement line; cumulative satiety text updates after reward delivery
  - Outcome rules: reward is delivered only when 10 space presses are completed before timeout

- Condition ID: `fr20`
  - Participant-facing meaning: press the space bar 20 times to earn the token
  - Concrete stimulus realization (visual/audio): text prompt with `20` in the requirement line; cumulative satiety text updates after reward delivery
  - Outcome rules: reward is delivered only when 20 space presses are completed before timeout

Also document where participant-facing condition text/stimuli are defined:

- Participant-facing text source (config stimuli / code formatting / generated assets): `config/config.yaml` `stimuli.*` entries, formatted at runtime with `StimBank.get_and_format(...)`
- Why this source is appropriate for auditability: all participant wording and condition-specific counts remain in config, so localization or wording edits do not require code changes
- Localization strategy (how language variants are swapped via config without code edits): swap `config/*.yaml` files and keep `run_trial.py` text-agnostic except for key/value formatting placeholders

## 4. Response and Scoring Rules

- Response mapping: `space` is the only work-phase response key
- Response key source (config field vs code constant): config-defined via `task.key_list` / `task.response_key`
- If code-defined, why config-driven mapping is not sufficient: not applicable
- Missing-response policy: if a press window times out before quota completion, the trial ends without reward
- Correctness logic:
  - a trial is successful when the required number of space presses is completed within the allowed press windows
  - individual press windows are counted as hits when `space` is pressed before timeout
- Reward/penalty updates:
  - successful trials add `reward_tokens_per_completion` to the cumulative total
  - failed trials add no reward
  - no negative penalty is used
- Running metrics:
  - cumulative tokens
  - completion rate
  - mean completion latency
  - timeout count
  - satiety fraction

## 5. Stimulus Layout Plan

For every screen with multiple simultaneous options/stimuli:

- Screen name: instruction screen
  - Stimulus IDs shown together: `instruction_text`
  - Layout anchors (`pos`): centered
  - Size/spacing (`height`, width, wrap): 28 px, wrap width 1000 px
  - Readability/overlap checks: single text block, no overlap risk
  - Rationale: a centered instruction block is easiest to read before the timing task starts

- Screen name: work screen
  - Stimulus IDs shown together: `work_prompt`, `work_counter`, `satiety_text`, `fixation`
  - Layout anchors (`pos`): prompt near `y=120`, counter near `y=18`, satiety text near `y=-84`, fixation near center/lower center
  - Size/spacing (`height`, width, wrap): prompt 30 px, counter 32 px, satiety 26 px, wrap width 800 to 1000 px
  - Readability/overlap checks: text blocks are vertically separated; no debug labels are shown to participants
  - Rationale: the participant needs a stable count of presses plus a visible satiety indicator

- Screen name: reward screen
  - Stimulus IDs shown together: `reward_token`, `reward_text`, `satiety_text`
  - Layout anchors (`pos`): reward token centered at `y≈22`, reward text below at `y≈-118`, satiety text below that
  - Size/spacing (`height`, width, wrap): token radius 42 px, text 30 px, wrap width 900 px
  - Readability/overlap checks: token is visually distinct from the text block; text lines are stacked
  - Rationale: reinforce the moment of reward delivery and show cumulative satiety

- Screen name: block break / goodbye
  - Stimulus IDs shown together: `block_break`, `good_bye`
  - Layout anchors (`pos`): centered
  - Size/spacing (`height`, width, wrap): 26 to 28 px, wrap width 980 px
  - Readability/overlap checks: one block of text per screen
  - Rationale: summary screens are informational and should remain uncluttered

## 6. Trigger Plan

- `exp_onset`: experiment start
- `exp_end`: experiment end
- `block_onset`: each block start
- `block_end`: each block end
- `trial_onset`: first work-window onset in each trial
- `press_onset`: each press window onset
- `press_response`: every successful space press
- `press_timeout`: press-window timeout
- `reward_onset`: reward token screen onset
- `satiation_onset`: satiety screen onset
- `iti_onset`: ITI onset

## 7. Architecture Decisions (Auditability)

- `main.py` runtime flow style (simple single flow / helper-heavy / why): simple block loop with a single task-specific helper for the repeated press windows
- `utils.py` used? yes
- If yes, exact purpose (adaptive controller / sequence generation / asset pool / other): fixed-ratio parsing, satiety math, and block summary helpers
- Custom controller used? no
- If yes, why PsyFlow-native path is insufficient: not applicable
- Legacy/backward-compatibility fallback logic required? no
- If yes, scope and removal plan: not applicable

## 8. Inference Log

List any inferred decisions not directly specified by references:

- Decision: map the task into three fixed-ratio conditions (`fr5`, `fr10`, `fr20`)
  - Why inference was required: the queue title does not specify exact ratio values
  - Citation-supported rationale: fixed-ratio pausing and reinforcement-schedule papers support the general structure, while effort-based food-reward papers support the satiety/motivation framing

- Decision: use cumulative token accumulation as the satiety index
  - Why inference was required: the exact satiety metric is not specified in the queue title
  - Citation-supported rationale: food-reward and establishment-operation papers link reward value to motivational state, so a cumulative token index is a defensible operationalization

- Decision: implement each required press as a separate press window inside the work phase
  - Why inference was required: PsyFlow’s standard response capture is single-response oriented
  - Citation-supported rationale: per-press windows preserve auditable RTs, QA/sim compatibility, and fixed-ratio completion timing

## Contract Note

- Participant-facing labels/instructions/options should be config-defined whenever possible.
- `src/run_trial.py` should not hardcode participant-facing text that would require code edits for localization.
