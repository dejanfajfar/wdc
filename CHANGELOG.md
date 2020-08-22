# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [unreleased]
### Add
- ```export``` command

### Fixed
- Tasks with no history do not cause error on ```info``` command

### Changed
- Moved documentation to the wiki

## [0.3.9]
### Add
- ```amend``` command

### Changed
- Work item tags are now sorted alphabetically

## [0.2.7]
### Fix
- ```list``` command does not throw error if no tasks have been recorder yet
- ```list``` command now shows the last state of the task and not the oldest one

### Changed
- The error and warning output is now colored and texts changed

## [0.2.4]
### Add
- ```info``` command

## [0.1.3]
### Add
- ```calc``` command
- ```start``` command
- ```list``` command
