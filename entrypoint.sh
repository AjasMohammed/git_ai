#!/bin/bash
set -e

# Assuming repos are mounted under /repos directory
echo "Setting Git safe.directory for repos under /repos..."

for repo_path in /repos/*; do
  if [ -d "$repo_path/.git" ]; then
    echo "Adding safe.directory: $repo_path"
    git config --global --add safe.directory "$repo_path"
  fi
done

# Now start your FastAPI app (adjust to your command)
exec .venv/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8888
