#!/bin/bash

# Installs the dependencies with poetry and then runs the application with uvicorn
# This script is used in the Dockerfile as the entrypoint

poetry install --no-root
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
