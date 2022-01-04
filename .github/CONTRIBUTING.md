## Development

Use `pre-commit install` to install the pre-commit hook for the repository.

### Testing

To run all the tests:

```shell
pytest
```

To create test for a specific formatting option use the `tests/data/format` directory. For each `.py` file create a `.py.out` file with the expected output after formatting. The test suite will automatically pickup the new tests.

To only run a specific test from that directory, for example `tests/data/format/multi_line/class_docstring.py`, use:

```shell
pytest -k multi_line-class_docstring
```
