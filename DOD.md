# Definition of Done for Integration

## Overview

This document outlines the necessary criteria that must be met for an integration to be considered complete.

An integration in this context refers to a route under `app/routes/integration_name` which includes at least an `integration_name_router.py` and `README.md`.

## Files

- [ ] `integration_name_router.py` included
- [ ] `README.md` included

## Coding Standards

- [ ] Uses prompt templates in Jinja.
- [ ] Uses Pydantic v2 to validate input.
- [ ] Uses Pydantic v2 to validate output.
- [ ] All functions include type hints for input and returns.
- [ ] Returns a `uuid4` in the response.
- [ ] Uses a common logging format with `log.info` and `log.debug`.
- [ ] Uses a standard environment variables format, with a prefix of `ICA_INTEGRATION_NAME_`.
- [ ] Passes `pylint` with a score of 9.8 or higher.
- [ ] All static typing checks (e.g., `mypy`, `pyright`) pass, including bandit and all other security scans.
- [ ] 100% docstring coverage (using Google dostring format), with doctest and all documented Args, Returns, Raises, Example -  including the module itself, and passes `pydocstyle`.
- [ ] Includes dependencies in a group under `pyproject.toml`
- [ ] Can be installed and tested indepdendently, or removed from the container without affecting other integrations.


## Testing

- [ ] Unit testing is included.
- [ ] At least 80% test coverage.
- [ ] Included in `test/jmeter` test.

## UI Prototype

- [ ] Included in `tools/streaming-ui/integrations.json` and tested.
