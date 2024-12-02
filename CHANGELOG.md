# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-10-18
### Added
- Initial release of the `msl-odt` PyPi module.
- Basic functionality for reading and writing to ODT files.

### Changed
- [2020] Very first version 2020 by Adam D
- [2024 August] Added equation mathHeight by Cheng Y
- [2024 September] by Adam D 
  - Added tables, minor formatting, and table creation utility
  - Added warnings for problematic parameters
  - Used PEP8 case convention (lowercase or snake_case) as opposed to CamelCase which previous functions have used. (Eventually other functions should be re-written to conform with PEP8 and also annotations (PEP484))

### Fixed
- Initial implementation had issues with hyperlink detection in `addtext`, which was fixed to properly format detected URLs as clickable links
- Appending to existing document needed an additional utility function to pick up styles for previous tables so that new table styles didn't overwrite them

### Deprecated
- None at this time.

### Removed
- None at this time.

## [Unreleased]

### Added 
- Enhancements to allow richer text formatting, including bold, italic, and other styles for paragraphs

### Changed
- Improvements for the `addtext` method to support different link formats, like email addresses
- Refactoring code for better modularity and test coverage

