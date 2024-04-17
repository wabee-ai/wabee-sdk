# Contributing Guide

## Project Setup

First of all, clone this repository from git using the following command:

```sh
git clone <TODO: ADD REPO URL>
```

Then, install `poetry` and `pre-commit` with the following commands:

```sh
pip install poetry==1.8.0 pre-commit==3.7.0
```

Next step is to initialize `pre-commit-hooks` with:

```sh
pre-commit install --hook-type pre-commit --hook-type pre-push --hook-type commit-msg
pre-commit run --all-files
```

Finally, run the command below to install the project dependencies

```sh
poetry install
```

Now we are good to go

## Functionality Testing

To run the project tests use:

```sh
poetry run pytest -vv
```

Add the flag `--cov` to the command above if you also want to include test coverage

## Project Structure

The project folder/file structure is given down below for reference:

```sh
.
├── CHANGES.txt
├── CONTRIBUTING.md
├── examples
│   ├── division_tool.py
│   ├── food_ordering_tool.py
│   ├── __init__.py
│   └── power_tool.py
├── LICENSE
├── poetry.lock
├── pyproject.toml
├── README.md
├── semantix_agent_tools
│   ├── handlers
│   │   ├── dates
│   │   │   └── date_handler.py
│   │   ├── exec
│   │   │   └── python_execution_handler.py
│   │   └── files
│   │       └── file_handler.py
│   ├── __init__.py
│   ├── semantix_agent_tool_config.py
│   ├── semantix_agent_tool_field_validator.py
│   ├── semantix_agent_tool_input.py
│   └── semantix_agent_tool.py
└── tests
    ├── handlers
    │   ├── dates
    │   │   └── test_date_handler.py
    │   ├── exec
    │   │   └── test_python_execution_handler.py
    │   └── files
    │       └── test_file_handler.py
    ├── __init__.py
    ├── test_semantix_agent_tool_config.py
    ├── test_semantix_agent_tool_field_validator.py
    ├── test_semantix_agent_tool_input.py
    └── test_semantix_agent_tool.py
```

## How to Contribute

To add new features to this project, first of all, create a feature branch from the main branch using:

```sh
git checkout -b feat/feature-name-here main
```

Make sure the main branch is up to date with the remote, if you are not sure, run:

```sh
git fetch
git switch main
git pull
```

Then, commit your changes to the feature branch using conventional commit messages, like the example below:

```sh
git commit -m 'feat: ensure semantix agent tool does not allow its children class to not implement the create method'
```

We also encourage you to create short purpose commits to enhance version control management. Moreover, note that your commit might be blocked by the hooks if it does not follow the linting/security guidelines, if it happens to you, then make the necessary changes to make your changes compliant and commit again.

Once all the changes were made, push the changes to the remote using:

```sh
git push origin/feat/feature-name-here
```

Finally, create a merge request to the main branch and assign one of the project maintainers listed at the [pyproject.toml](./pyproject.toml) file as reviewer and wait for the feedback!
