#!/bin/bash

set -euo pipefail
export PYTHONPATH=/opt/app-root/
exec python3 webserver/server.py
