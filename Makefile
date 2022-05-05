clean:
	find . -name \*.pyc -delete
	find . -name __pycache__ -delete
	rm -rf dist/

unit:
	pytest

lint:
	flake8 src/

isort:
	isort --diff --check src/

black:
	black --diff --check src/

test: unit lint isort black
