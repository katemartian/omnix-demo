name: CI

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: Cache pip
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/pyproject.toml') }}
          restore-keys: |
            ${{ runner.os }}-pip-

      - name: Install
        run: |
          python -m pip install --upgrade pip
          pip install -e .[dev]

      - name: Lint (ruff)
        run: |
          ruff check .

      - name: Run tests
        env:
          # HuggingFace models sometimes show progress bars; disable to keep logs clean
          TRANSFORMERS_NO_ADVISORY_WARNINGS: 1
          TOKENIZERS_PARALLELISM: false
        run: |
          pytest -q
