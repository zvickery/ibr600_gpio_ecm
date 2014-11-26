#!/usr/bin/env bash

gunicorn lights:app -D --error-logfile log/lights.error.log --access-logfile log/lights.access.log --access-logformat '%({X-Forwarded-For}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
