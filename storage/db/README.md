# Database Storage

Each client project receives a dedicated schema namespace inside the shared PostgreSQL instance on `/Volumes/DATA/STORAGE/postgresql/`.

Recommended naming: `<client>_<project>__<module>` (e.g., `3m_lighting2025__jtbd`). Maintain migration scripts or DDL snapshots in this folder to document schema changes.

## Category Intelligence Schema

- **Database:** `offbrain` (local Postgres on `localhost`)
- **Schema:** `category_intel`
- **DDL:** `storage/db/category_intel_schema.sql`
- **Tables:**
  - `category_intel.category_projects` – project lookup (`project_key`, client, project name, description).
  - `category_intel.category_brands` – brand rows with `project_key` foreign key.
  - `category_intel.category_products` – SKU rows with `project_key` foreign key.

Use `project_key` (for example `251106-3m-accent-lighting`) whenever inserting new data so multiple projects can share the same tables without collisions.
