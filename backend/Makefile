export PYTHONPATH=$(PWD)


.PHONY: test test-cov lint format typecheck run

test:
	PYTHONPATH=$(PYTHONPATH) pytest -v

test-cov:
	PYTHONPATH=$(PYTHONPATH) coverage run -m pytest
	coverage report -m
	coverage html

lint:
	black pages tests --check

format:
	black pages tests

typecheck:
	mypy pages --explicit-package-bases

# Alembic

alembic:
	alembic -x DOCKER_ENV=1

migrate-dev:
	alembic upgrade head

revision:
ifndef name
	$(error Você precisa rodar: make revision name=mensagem)
endif
	alembic revision --autogenerate -m "$(name)"

downgrade:
	alembic downgrade -1

run:
	uvicorn pages.api.main:app --reload --host 0.0.0.0 --port 8000
