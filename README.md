# Interlink Insights Repository

Organises shared analytics modules alongside client projects. Designed so non-technical teammates can find deliverables, configs, and run history without digging through code.

## Top-Level Map

| Folder | What lives here |
|--------|-----------------|
| `modules/` | Reusable analytics/code modules (category intelligence, consumer video, etc.). No client data is stored here. |
| `clients/` | Engagement-specific workspaces organised by client → project. Contains configs, docs, runs, and admin files. |
| `storage/` | Pointers and documentation for shared PostgreSQL schemas and large media stored on `/Volumes/DATA`. |
| `docs/` | Cross-project reference materials, R&D notes, and module design papers. |
| `scripts/`, `core/`, `data/` | Shared utilities and assets (see sub-README files). |

## Working With a Client Project

1. Navigate to `clients/<client>/projects/<project>/`.
2. Review the project `README.md` for quick links to configs, deliverables, and storage paths.
3. Use the module run logs (`runs/<module>/run-log.md`) to understand prior executions.
4. Any new runs should create a timestamped folder under `runs/<module>/` and update the log table.

## Storage Conventions

- **Large media** lives on `/Volumes/DATA/media/<client>/<project>/`.
- **Databases** live on `/Volumes/DATA/STORAGE/postgresql/` with schema names documented in `storage/db/`.
- **Git repository** remains lightweight and audit-friendly—no bulky assets or secrets.

## Documentation Expectations

- Module documentation stays inside `modules/<module>/docs/` and explains how to integrate.
- Client/project documentation stays inside `clients/<client>/projects/<project>/docs/`.
- Admin/finance materials belong in `clients/<client>/projects/<project>/admin/`.

Questions? Start with the project README, then check the relevant module docs.
