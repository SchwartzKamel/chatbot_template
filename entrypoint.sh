#!/bin/sh
set -e

# Run application with security-conscious settings
exec python -m app.root_agent "$@"