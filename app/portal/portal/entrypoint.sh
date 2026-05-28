#!/bin/sh

# Exit on errors
set -e

# If a SQL_HOST is provided, wait for Postgres to become available before running
# migrations. This prevents race conditions when using docker-compose where the
# web container starts before the DB is ready.
if [ -n "$SQL_HOST" ]; then
	echo "Waiting for database at ${SQL_HOST}:${SQL_PORT:-5432}..."
	# pg_isready is available after installing postgresql-client in the image
	until pg_isready -h "$SQL_HOST" -p "${SQL_PORT:-5432}" >/dev/null 2>&1; do
		echo "Postgres is unavailable - sleeping"
		sleep 1
	done
	echo "Postgres is up"
fi

echo "Applying database migrations..."
python manage.py migrate --noinput
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Checking for existing providers..."
if [ "$(python manage.py shell -c 'from providers.models import PoliticalRegion; print(PoliticalRegion.objects.count())' 2>/dev/null | tail -1)" = "0" ]; then
    echo "No providers found, loading default providers fixture..."
	python manage.py loaddata fixtures/providers_20210524.json
else
	echo "number of political regions: $(python manage.py shell -c 'from providers.models import PoliticalRegion; print(PoliticalRegion.objects.count())' 2>/dev/null | tail -1)"
	echo "Providers content already exist, skipping fixture load."
fi

echo "Starting python development server on :8000"
python manage.py runserver 0.0.0.0:8000
