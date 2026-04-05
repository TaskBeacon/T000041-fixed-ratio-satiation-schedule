# Stimulus Mapping

## Mapping Table

| Condition | Stage/Phase | Stimulus IDs | Participant-Facing Content | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Asset References | Notes |
|---|---|---|---|---|---|---|---|---|
| `shared` | `instruction` | `instruction_text` | `你将进行一个固定比率按键任务。每一轮都需要连续按空格若干次，达到要求后才能获得 1 个代币。代币越多，屏幕上的饱腹指数越高。` | `W1964652787` | Title and fixed-ratio pausing framing; schedule-related reinforcement-effect literature | `psychopy_builtin` | `text` | Shared instruction screen for all conditions. |
| `fr5` | `work_press` | `work_prompt`, `work_counter`, `satiety_text`, `fixation` | `本轮固定比率要求：连续按空格 5 次；已按 {current_press}/5 次；饱腹指数 ...` | `W1964652787` | Fixed-ratio pausing and schedule type evidence | `psychopy_builtin` | `text` | Ratio-specific work prompt. |
| `fr10` | `work_press` | `work_prompt`, `work_counter`, `satiety_text`, `fixation` | `本轮固定比率要求：连续按空格 10 次；已按 {current_press}/10 次；饱腹指数 ...` | `W2037578646` | Response rate and schedule type evidence | `psychopy_builtin` | `text` | Ratio-specific work prompt. |
| `fr20` | `work_press` | `work_prompt`, `work_counter`, `satiety_text`, `fixation` | `本轮固定比率要求：连续按空格 20 次；已按 {current_press}/20 次；饱腹指数 ...` | `W2167077741` | Establishing operations and reinforcement effects; schedule sensitivity | `psychopy_builtin` | `text` | Ratio-specific work prompt. |
| `shared` | `reward_delivery` | `reward_token`, `reward_text`, `satiety_text` | `奖励已发放：+1 个代币；饱腹指数随累计代币上升` | `W2029549266` | Effort-based responding for food and reward value under motivational state | `psychopy_builtin` | `circle`, `text` | Reward token is a built-in circle primitive. |
| `shared` | `satiation_pause` | `satiety_text` | `饱腹指数：{satiety_pct:.0%}` | `W2077496630` | Food-reward value decreases as motivational state changes | `psychopy_builtin` | `text` | Satiation is operationalized as cumulative reward progress. |
| `shared` | `timeout_feedback` | `timeout_text` | `本轮超时，未获得代币` | `W2168128112` | Food-reinforced behavior and reward interruption framing | `psychopy_builtin` | `text` | Displayed only when the ratio window expires early. |
| `shared` | `block_break` | `block_break` | `完成率、平均完成用时、累计代币` | `W2164961539` | Reward-related vigor and motivation summary framing | `psychopy_builtin` | `text` | Block summary screen. |
| `shared` | `good_bye` | `good_bye` | `任务结束；总完成率；累计代币；平均完成用时` | `W1980196077` | Effort-based responding and motivational cost framing | `psychopy_builtin` | `text` | Final summary screen. |

Allowed implementation modes:

- `psychopy_builtin`
- `generated_reference_asset`
- `licensed_external_asset`

