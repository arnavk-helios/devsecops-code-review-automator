#!/bin/bash

# Target path passed as an argument (defaults to current directory if not provided)
TARGET=${1:-"."}

# Run Bandit SAST scan on target and output in JSON format
bandit -r "$TARGET" -f json --quiet 2>/dev/null