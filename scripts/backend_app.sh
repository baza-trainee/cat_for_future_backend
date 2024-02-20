#!/usr/bin/env bash

alembic upgrade head
gunicorn -c gunicorn.conf.py src.main:app
