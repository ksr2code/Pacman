export UV_SKIP_WHEEL_FILENAME_CHECK=1
.PHONY: install run debug clean lint lint-strict test re push skip

ifneq (,$(wildcard ./.env))
    include .env
    export
endif

PY_FILES := pac-man.py $(shell find src -name '*.py' -type f)

GREEN := \033[0;32mOK\033[0m
RED := \033[0;31mKO\033[0m

install:
	uv sync --python 3.12 --all-extras
	uv tool install pygbag

build:
	unzip packages/mazegenerator-00001-py3-none-any.whl -x mazegenerator-2.0.1.dist-info/{METADATA,WHEEL,top_level.txt,RECORD} -d src
	pygbag --build src/main.py
	rm -rf src/mazegenerator
	@read -p "Launch HTTP server on port 8000? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		python3 -m http.server -b 127.0.0.1 8000 -d src/build/web; \
	fi

run:
	uv run -v pac-man.py $(ARGS)

debug:
	uv run python3 -m pdb pac-man.py $(ARGS)

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
	find . -type d -name .venv -exec rm -rf {} +
	find . -type d -name .pygbag -exec rm -rf {} +
	find . -type d -name build -exec rm -rf {} +
	find . -type d -name dist -exec rm -rf {} +
	find . -name .pytest_cache -exec rm -rf {} +
	find . -name .ruff_cache -exec rm -rf {} +
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete

# use this target to run the unit tests
test:
	pytest test -vv
	@echo "WHEN PROJECT IF FINISHED REMOVE THE TEST FOLDER"

lint:
	uv run flake8 $(PY_FILES)
	uv run mypy $(PY_FILES) \
		--explicit-package-bases \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs \
		--exclude '(^\.venv/)'

lint-strict:
	uv run flake8 $(PY_FILES)
	uv run mypy $(PY_FILES)\
		--explicit-package-bases \
		--strict \
		--exclude '(^\.venv/)'

re: clean install

# push the build to itch.io
push:
	BUTLER_API_KEY=$(BUTLER_API_KEY) butler/butler push ./src/build/web 42-HN-DreamTeam/pac-man:web
