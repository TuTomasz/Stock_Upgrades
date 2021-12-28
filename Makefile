.PHONY: setup build install-build uninstall-build publish clean test lint

# Setup Constants
POETRY_VERSION = 1.1.11
 

# Set up environment and install dependencies
setup:
	make clean
	@echo Install Poetry Version $(POETRY_VERSION)
	[ -f ./poetry.lock ] && rm -r poetry.lock || echo lock file not found
	pip install --upgrade --force-reinstall 'poetry==$(POETRY_VERSION)'
	@echo 🧰 Installing  Dependencies 
	poetry install

 
clean:
	@echo 🧹 cleanup
	rm -r ./Data/Rating/*.json || echo dir file not found

# run unit tests
test:
	@echo 🧪 Running Tests
	poetry run pytest tests/
	@echo 🧪 Type Checks with MyPy
	poetry run mypy python_datastructures/

# format code
lint:
	@echo ♻️ Reformatting Code
	poetry run black .
