#!/usr/bin/env bash

/scripts/wait-for-it.sh postgres:5432 -- echo "PostgreSQL is up"
/scripts/wait-for-it.sh redis:6379 -- echo "Redis is up"

alembic upgrade head
gunicorn -c gunicorn.conf.py src.main:app
