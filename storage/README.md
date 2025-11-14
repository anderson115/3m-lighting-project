# Shared Storage Map

This folder centralises pointers to persistent storage used across clients.

- `db/` – configuration files and migration scripts for PostgreSQL instances hosted on `/Volumes/DATA/STORAGE/postgresql/`.
- `media/` – lightweight index files that reference large raw assets stored under `/Volumes/DATA/media/`.

> Large binary assets and live databases remain on `/Volumes/DATA`; do not check them into git.
