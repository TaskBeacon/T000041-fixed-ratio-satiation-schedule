# CHANGELOG

All notable development changes for `T000041-fixed-ratio-satiation-schedule` are documented here.

## [Unreleased] - 2026-04-05

### Added
- Added a fixed-ratio satiation schedule with three ratio conditions (`fr5`, `fr10`, `fr20`) and cumulative token-based satiety tracking.
- Added reference-curated literature files covering fixed-ratio pausing, engagement bouts, effort-based responding for food, and reward-vigor literature.
- Added repeated press-window handling, reward delivery, satiety feedback, and timeout feedback within the PsyFlow/TAPS runtime.

### Changed
- Replaced the copied probabilistic stimulus selection scaffold with a fixed-ratio response-counting paradigm.
- Reworked human, QA, scripted-sim, and sampler-sim configs to use the new ratio requirements and Chinese participant-facing text.
- Updated the launcher, task metadata, and block summary reporting for the new effort-based schedule.

### Fixed
- Added explicit layout anchors for the multi-line work, reward, and summary screens.
- Kept participant-facing text in config-defined stimuli to preserve localization portability.

