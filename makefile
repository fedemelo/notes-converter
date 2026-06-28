run:
	set -a && source .env && set +a && venv/bin/uvicorn src.main:app --reload --host 0.0.0.0 --port 8005

format:
	venv/bin/isort . && venv/bin/black .

lint:
	venv/bin/flake8

test:
	venv/bin/pytest