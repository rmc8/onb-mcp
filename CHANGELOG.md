# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.1] - 2026-07-12

### Fixed
- **Episode Profiles**: Fixed `speaker_config` parameter type from `dict` to `str` in `create_episode_profile` and `update_episode_profile` tools to match the backend API schema requirement.

## [0.4.0] - 2026-07-12

### Added
- **Speaker Profile CRUD**: Added `list_speaker_profiles`, `get_speaker_profile`, `create_speaker_profile`, `update_speaker_profile`, `delete_speaker_profile` tools for managing podcast speaker configurations (voice model, speakers, TTS provider/model).
- **Episode Profile CRUD**: Added `list_episode_profiles`, `get_episode_profile`, `create_episode_profile`, `update_episode_profile`, `delete_episode_profile` tools for managing podcast episode format configurations (segments, tokens, language, LLM providers/models).
- Full create/read/update/delete support for both profile types via the Open Notebook REST API.

## [0.3.0] - 2026-07-11

### Added
- Added instruction on how to run via `uvx` (PyPI package manager toolrunner) which downloads and runs the server instantly.
- Added explicit configurations and setup templates for Claude Desktop using `uvx`.

### Changed
- Promoted `uvx` as the primary installation and running mechanism in `README.md`.
- Updated PyPI package version configuration to `0.3.0` in `pyproject.toml`.
- Improved error descriptions and configuration hints.

## [0.2.0] - 2026-06-26

### Added
- Initial release of Open Notebook MCP Server.
- Implemented 44 distinct tools covering Notebooks, Sources, Notes, Chat sessions, Models, Credentials, and Podcasts.
- Progressive disclosure pattern via `search_capabilities` tool.
- Supports both STDIO (for local dev) and Streamable HTTP (for remote setups) transports.
