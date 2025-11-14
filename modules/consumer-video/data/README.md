# Data Directory Template

Run-specific artifacts (raw transcripts, processed segments, logs, model outputs) should not live inside the shared module. When executing this module for a client, direct all data writes to the project space under `clients/<client>/projects/<project>/runs/consumer-video/` and keep `/Volumes/DATA/media/<client>/<project>/` for large video/audio source files.

This placeholder maintains the expected folder structure for tests and packaging while keeping the repository lightweight.
