# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.1] - 2025-11-23

### Added
- Templates directory README linking to official jgraph/drawio-diagrams repository for comprehensive examples and reference implementations

## [1.1.0] - 2025-11-22

### Added
- **Zero-Error Quick Start section** in instruction file with mandatory first-line XML declaration, infinite canvas rule, and clear DO/DON'T list to prevent common generation errors
- **FINAL OUTPUT CHECKLIST** consolidating all pre-output validation requirements in one authoritative location
- **Enhanced validator detection** for literal `\n` sequences, multi-line value attributes, and improved `<br/>` validation requiring `html=1` in style
- Support for command-line file/directory arguments in `validate.py` for flexible testing
- `tmp/` directory with `.gitignore` entry for test outputs (excluded from version control)

### Changed
- **Clarified newline handling policy**: XML entities (`&#xa;`, `&#xA;`, `&#10;`) are now explicitly permitted as valid multi-line label format; only literal `\n` (backslash-n) is forbidden
- **Merged duplicate checklists**: Consolidated "PRE-OUTPUT CHECKLIST" and "Validation Checklist" into single "FINAL OUTPUT CHECKLIST (must all be true)" to eliminate redundancy and confusion
- **Rule 9 WRONG example**: Improved comment clarity to precisely explain how quoted hex values break XML parsing (premature style attribute closure)
- Updated DO/DON'T guidance to distinguish between valid XML entities and invalid literal escape sequences

### Fixed
- Validator previously rejected valid `&#xa;` entities that draw.io renders correctly; now only flags literal `\n` sequences
- Removed overly restrictive newline entity detection that caused false positives on structurally valid diagrams
- Simplified final output gate phrase for better model comprehension (removed blockquote formatting)

### Rationale
These changes address structural failures observed during real-world multi-model testing (Claude Sonnet 4.5, Gemini 3, ChatGPT 4+). Initial experimentation revealed:
- Models occasionally omitted XML declaration despite instructions
- Literal `\n` sequences appeared in value attributes (breaking rendering)
- Duplicate checklists created confusion about authoritative requirements
- Overly strict validation rejected working diagrams using valid XML entities

The hardened instructions prioritize:
1. **Prominent placement** of critical requirements (Zero-Error Quick Start before detailed rules)
2. **Unambiguous validation** (single authoritative checklist)
3. **Correct technical distinctions** (XML entities vs literal escape sequences)
4. **Empirical validation** (tested against generated diagrams, verified with draw.io rendering)

## [1.0.0] - 2024-11-17

### Added
- Initial draw.io instruction framework with progressive template structure
- Validation script (`validate.py`) checking structural requirements
- Example diagrams demonstrating common patterns (flowcharts, architectures, networks)
- Comprehensive rule set for mxGraph XML generation
- Style and color palette reference guides

[Unreleased]: https://github.com/simonpo/drawio-ninja/compare/v1.1.1...HEAD
[1.1.1]: https://github.com/simonpo/drawio-ninja/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/simonpo/drawio-ninja/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/simonpo/drawio-ninja/releases/tag/v1.0.0
