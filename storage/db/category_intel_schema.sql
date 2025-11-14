-- Category Intelligence shared schema
CREATE SCHEMA IF NOT EXISTS category_intel;

CREATE TABLE IF NOT EXISTS category_intel.category_projects (
    project_key TEXT PRIMARY KEY,
    client TEXT,
    project_name TEXT,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS category_intel.category_brands (
    project_key TEXT REFERENCES category_intel.category_projects(project_key) ON DELETE SET NULL,
    category TEXT NOT NULL,
    name TEXT NOT NULL,
    tier TEXT,
    source_url TEXT,
    inserted_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS category_intel.category_products (
    project_key TEXT REFERENCES category_intel.category_projects(project_key) ON DELETE SET NULL,
    category TEXT NOT NULL,
    retailer TEXT,
    sku TEXT,
    name TEXT,
    url TEXT,
    price NUMERIC,
    rating NUMERIC,
    taxonomy_path JSONB,
    attributes JSONB,
    inserted_at TIMESTAMPTZ DEFAULT NOW()
);
