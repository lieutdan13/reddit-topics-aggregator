# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## TODO

- add support for json output
- add support for markdown output
- add count of articles if duplicate
- remove pinned topics
- default to 0 topics
- add --all which will set the number of submissions for every other option

## [Unreleased]

### Added

### Fixed

### Changed

### Removed

## [0.2.1]

### Fixed

- unit test coverage now reports correctly in GitHub

## [0.2.0]

### Added

- environment variable defaults are now documented and used
- command `topics` - CLI sub-command to retrieve and display topic submissions for the specified Subreddits

### Fixed

- coverage in Github was failing with "import file mismatch"

## [0.1.0]

### Added

- command `connect` - CLI sub-command to connect and show basic information about the authenticated user
- unit tests now run on Python 3.10, 3.11, and 3.12 in GitHub
- `tox` configuration added to run locally
- completely switches to `ruff` for file formatting
- pip-audit vulnerability scanning added locally
- gh-action-pip-audit added to GitHub

## [0.0.1] - 2024-10-01

Initial Release

[unreleased]: https://github.com/lieutdan13/reddit-topics-aggregator/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/lieutdan13/reddit-topics-aggregator/releases/tag/v0.2.0
[0.1.0]: https://github.com/lieutdan13/reddit-topics-aggregator/releases/tag/v0.1.0
[0.0.1]: https://github.com/lieutdan13/reddit-topics-aggregator/releases/tag/v0.0.1
