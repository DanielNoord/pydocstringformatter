Development
===========

Linting and checks
------------------

Use ``pip`` to install ``pre-commit`` and then use ``pre-commit install`` to
install the pre-commit hook for the repository.

Creating a new formatter
------------------------

- Implement a Formatter by inheriting from ``pydocstringformatter.formatting.Formatter``.
- Add your new formatter to ``pydocstringformatter.formatting.FORMATTERS``.
- Write a clear docstring because this will be user-facing: it's what will be seen in
  the help message for the formatter's command line option.
- Choose a proper name because this will be user-facing: the name will be used to turn
  the formatter on and off via the command line or config files.
- Rebuild the documentation by running:

.. code-block:: shell

  cd docs
  make html


Testing
-------

To run all the tests:

.. code-block:: shell

  pytest

To create test for a specific formatting option use the ``tests/data/format`` directory.
For each ``.py`` file create a ``.py.out`` file with the expected output after formatting.
The test suite will automatically pickup the new tests.

To only run a specific test from that directory, for example
``tests/data/format/multi_line/class_docstring.py``, use:

.. code-block:: shell

  pytest -k multi_line-class_docstring


Primer
-------

To check if any changes create any unforeseen regressions all pull requests are tested
with our primer. This process is heavily inspired on other open source projects and our
own primer is based on the one used by `mypy <http://mypy-lang.org>`_.

You can also run the primer locally with minimal set-up. First you will need to make
a duplicate of your ``pydocstringformatter`` directory in a new ``./program_to_test``
directory. This is required so that the primer can check out multiple versions of the
program and compare the difference.

The next step is to follow the bash script in the ``Run primer`` step in the ``primer``
workflow file, found at ``.github/workflows/primer.yaml``. This should allow you to run
all necessary steps locally.

The final output of the primer run can be found in ``.pydocstringformatter_primer_tests/fulldiff.txt``

New projects to run the primer over can be added to the ``pydocstringformatter/testutils/primer/packages.py``
file.
