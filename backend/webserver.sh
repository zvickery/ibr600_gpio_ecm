#!/usr/bin/env bash

gunicorn lights:app -D --error-logfile log/lights.error.log --access-logfile log/lights.access.log
