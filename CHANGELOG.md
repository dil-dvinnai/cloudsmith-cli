# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

**Note:** Until 1.0 any MAJOR or MINOR release may have backwards-incompatible changes.

## [Unreleased]

Phase 3 release.

## [0.2.0] - 2017-12-03

Phase 2 release.

### Added

- Configuration profiles, to support multiple environments.
- Options for `api_host`, `api_proxy` and `api_user_agent` in config file.
- The `help` command for those who need more than `-h` and `--help`.
- Support for uploading multiple package files at once.
- Tox-based testing for Python2.x and Python3.x.
- Pre-flight checks to push/upload command.
- The `list` command with support for listing distros, packages and repos.

### Changed

- Environment variables to use a `CLOUDSMITH_` prefix (not backwards compatible).

### Fixed

- Validation for `push` commands that require a distribution.
- Token endpoint failing because API key overrides login/password.
- Python3 compatibility so that it now runs with Py3. :-)

## [0.1.0] - 2017-11-23

Phase 1 release (initial release).