# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
