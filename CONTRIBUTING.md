# Contributing
## Python Version Support
A best attempt is made to support Python versions until they reach EOL, after which support will be formally dropped by the next minor or major release of this package, whichever arrives first. The status of Python versions can be found [here](https://devguide.python.org/versions/).

## Development Environment
Development of this project is done using the supported Python version most recently released.

This project uses [uv](https://docs.astral.sh/uv) to manage dependencies. With your fork cloned to your local machine, you can install the project and its dependencies to create a development environment using:

```bash
$ uv venv
$ uv sync --all-extras --dev
```

A [`pre-commit`](https://pre-commit.com) configuration is also provided to create a pre-commit hook so linting errors aren't committed:

```bash
$ pre-commit install
```

[`mypy`](https://mypy-lang.org/) is also used by this project to provide static type checking. It can be invoked using:

```bash
$ mypy .
```

Note that `mypy` is not included as a pre-commit hook.
