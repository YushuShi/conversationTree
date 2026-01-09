#!/bin/sh
set -eu

PORT_VALUE="${PORT:-${RAILWAY_PORT:-8080}}"
echo "Starting reflex on port ${PORT_VALUE}"

exec reflex run --env prod --single-port --backend-host 0.0.0.0 --frontend-port "$PORT_VALUE"
