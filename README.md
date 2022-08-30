# Enopios

## Installation

Install poetry, tested with poetry version `1.2.0rc2`.

```bash
curl -sSL https://install.python-poetry.org | python - --preview
```

Install dependencies:

```bash
poetry install
```

If you want to include extra dependencies edit the `pyproject.toml` file.

If you have changed any dependencies run the following:

```bash
poetry update
poetry export -f requirements.txt --output requirements.txt
```

Update `enopios/app.py` if you want to have a different streamlit script than
the bare-bones hello world.

Build the executable:

```bash
poetry run pyoxidizer build
```

Run the newly created executable:

```bash
./build/dist/enopios
```
