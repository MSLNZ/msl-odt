# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0] - 2024-12-18

### Added
- Initial release of the `msl-odt` PyPi module.
- Basic functionality for reading and writing to `.odt` files.

### Changed
- [2020] Initial stand-alone development in 2020
- [2024 August] Add mathHeight parameter to addequation()
- [2024 September]
  - Add tables, minor formatting, and table creation utility
  - Add warnings for problematic parameters
  - Modify to use PEP8 case convention (lowercase or snake_case).
- [2024 November]
  - Develop tests and example files
  - Configure for PyPi and Github

### Fixed
- Initial stand-alone version had issues with hyperlink detection in `addtext()`. This was fixed to properly format detected URLs as clickable links in the `.odt` document
- Appending to existing document required an additional utility function to read existing styles for previous tables so new table styles didn't overwrite or conflict with them.

### Deprecated
- None at this time.

### Removed
- None at this time.

## [Unreleased]

### Added 
- Enhancements for richer text formatting, e.g. bold, italic, etc. in paragraphs

### Changed
- Improve `addtext()` to support different link formats, e.g. email addresses
- Refactor code to improve modularity
- Extend test coverage