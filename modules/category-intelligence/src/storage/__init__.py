"""Storage adapters for Category Intelligence."""

from .filesystem import FilesystemWriter
from .postgres import PostgresWriter  # noqa: F401
from .duckdb_writer import DuckDBWriter  # noqa: F401

__all__ = ["FilesystemWriter", "PostgresWriter", "DuckDBWriter"]
