#!/bin/bash
sudo yum install -y git
git clone https://github.com/cs399f24/TaskNest.git
cd TaskNest/backend
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
./.venv/bin/python app.py