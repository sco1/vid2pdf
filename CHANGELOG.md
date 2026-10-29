# Changelog
Versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html) (`<major>`.`<minor>`.`<patch>`)

## [v1.3.0]
### Added
* `FFMPEG_PATH` may now point directly to the FFmpeg executable, in addition to a directory containing it
* FFmpeg executable is now searched on the system's `PATH` if it is not found at `FFMPEG_PATH` or the default `/utils/ffmpeg` location

### Fixed
* Fix default `/utils/ffmpeg` location resolving relative to the package directory rather than the project root
* Intermediate frames are now written to a uniquely named temporary directory, rather than `<dest>/frames`
* Intermediate frames are now cleaned up if conversion fails

## [v1.2.0]
### Added
* Add support for locating FFMPEG installation via an `FFMPEG_PATH` environment variable

### Changed
* #12 Updated CLI flow to be more consistent; step-by-step prompts have been removed

## [v1.1.0]
### Changed
* PDF filename now defaults to same filename as the input video
* Intermediate `frames` directory is no longer preserved

## [v1.0.0]
Initial Release - Yay! 🎉
