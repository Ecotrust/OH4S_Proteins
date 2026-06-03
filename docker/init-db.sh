#!/bin/sh
set -e

# This script runs automatically when the PostgreSQL container is first initialized
# It will only run if the database is empty (first time setup)

 DB_DUMP_FILE="/tmp/db_dump.sql"
 if [ -d "$DB_DUMP_FILE" ]; then
   echo "Error: expected SQL file at $DB_DUMP_FILE but found a directory. This usually means the host bind-mount source path does not exist as a file." >&2
   exit 1
 fi
 if [ ! -f "$DB_DUMP_FILE" ]; then
   echo "Error: database dump file not found at $DB_DUMP_FILE. Mount or copy the SQL dump before initializing the database." >&2
   exit 1
 fi
 if [ ! -r "$DB_DUMP_FILE" ]; then
   echo "Error: database dump file is not readable at $DB_DUMP_FILE. Check file permissions before initializing the database." >&2
   exit 1
 fi

echo "Importing database dump..."

# Import the SQL dump, ignoring meta-command errors
PGPASSWORD="$POSTGRES_PASSWORD" psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -v ON_ERROR_STOP=0 < "$DB_DUMP_FILE"

echo "Database import completed!"