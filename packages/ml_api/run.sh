#!/usr/bin/env bash

export IS_DUBUG=${DEBUG:-false}
exec gunicorn --bind 0.0.0.0:5000 --access-logfile - --error-logfile - run:application