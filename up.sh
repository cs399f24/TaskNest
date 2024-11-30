#!/bin/bash
cd scripts
./create_lambdas.sh
python3 -m venv .venv
./.venv/bin/pip install boto3 awscli
./.venv/bin/python create_add_task_lambda.py