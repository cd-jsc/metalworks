#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# Setup the Inventory app database (apply migrations) and generate dummy data.
# This script is intended for local development environments that rely on the
# provided docker-compose configuration.  It can be safely re-run multiple times.
# -----------------------------------------------------------------------------
set -euo pipefail

# Always execute from repository root regardless of where the script was called
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd "${SCRIPT_DIR}/.."

# Ensure backend & database containers are up in detached mode
# (frontend is optional for seeding so we omit it for speed)

docker compose up -d db backend

# Apply Django migrations (no-input avoids interactive prompts)
docker compose exec backend python manage.py migrate --noinput

# Seed dummy data (pass through any extra CLI args)
# Example: ./scripts/setup_and_seed.sh --items 100 --with-superuser
docker compose exec backend python manage.py seed_dummy_data "$@"

printf "\n✅  Database is ready and populated with dummy data.\n"