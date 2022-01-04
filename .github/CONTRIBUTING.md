## Development

### Linting

Use `pre-commit install` to install the pre-commit hook for the repository.

### Creating a new formatter

- Implement a Formatter by inheriting from `pydocstringformatter.formatting.Formatter`
- Add your new formatter to `pydocstringformatter.formatting.FORMATTERS`
- Write a clear docstring because this will be user-facing: it's what will be seen in
  the help message for the formatters command line option.
- Choose a proper name because this will be user-facing: the name will be used to turn
  the checker on and off via the command line or config files.

### Testing

To run all the tests:

```shell
pytest
```

To create test for a specific formatting option use the `tests/data/format` directory.
For each `.py` file create a `.py.out` file with the expected output after formatting.
The test suite will automatically pickup the new tests.

To only run a specific test from that directory, for example
`tests/data/format/multi_line/class_docstring.py`, use:

```shell
pytest -k multi_line-class_docstring
```
