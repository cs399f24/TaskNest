python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

./scripts/create_get_tasks_lambda.sh
./scripts/create_add_task_lambda.sh
./scripts/create_delete_task_lambda.sh

python scripts/create_api_gateway.py