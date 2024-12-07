#!/bin/bash
python3 -m venv .venv > /dev/null 2>&1 || { echo "Failed to create virtual environment"; exit 1; }

while [ ! -d ".venv" ]; do
  sleep 1
done

./.venv/bin/pip install boto3 awscli > /dev/null 2>&1 || { echo "Failed to install Python dependencies"; exit 1; }
echo "Virtual environment created and configured successfully!"