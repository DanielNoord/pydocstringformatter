Usage
=====

Current usage of ``pydocstringformatter``:

.. code-block:: shell

    usage: pydocstringformatter [-h] [-w] [--quiet] [-v] [--exclude EXCLUDE]
                                [--split-summary-body] [--no-split-summary-body]
                                [--strip-whitespaces] [--no-strip-whitespaces]
                                [--beginning-quotes] [--no-beginning-quotes]
                                [--closing-quotes] [--no-closing-quotes]
                                [--capitalize-first-letter]
                                [--no-capitalize-first-letter] [--final-period]
                                [--no-final-period] [--quotes-type]
                                [--no-quotes-type]
                                [files ...]

    positional arguments:
      files                 The directory or files to format.

    options:
      -h, --help            show this help message and exit
      -w, --write           Write the changes to file instead of printing the
                            diffs to stdout.
      --quiet               Do not print any logging or status messages to stdout.
      -v, --version         Show version number and exit.

    configuration:
      --exclude EXCLUDE     A comma separated list of glob patterns of file path
                            names not to be formatted.

    default formatters:
      these formatters are turned on by default

      --strip-whitespaces   Activate the strip-whitespaces formatter : Strip 1)
                            docstring start, 2) docstring end and 3) end of line.
      --no-strip-whitespaces
                            Deactivate the strip-whitespaces formatter.
      --beginning-quotes    Activate the beginning-quotes formatter : Fix the
                            position of the opening quotes.
      --no-beginning-quotes
                            Deactivate the beginning-quotes formatter.
      --closing-quotes      Activate the closing-quotes formatter : Fix the
                            position of the closing quotes.
      --no-closing-quotes   Deactivate the closing-quotes formatter.
      --capitalize-first-letter
                            Activate the capitalize-first-letter formatter :
                            Capitalize the first letter of the docstring if
                            appropriate.
      --no-capitalize-first-letter
                            Deactivate the capitalize-first-letter formatter.
      --final-period        Activate the final-period formatter : Add a period to
                            the end of single line docstrings and summaries.
      --no-final-period     Deactivate the final-period formatter.
      --quotes-type         Activate the quotes-type formatter : Change all
                            opening and closing quotes to be triple quotes.
      --no-quotes-type      Deactivate the quotes-type formatter.

    optional formatters:
      these formatters are turned off by default

      --split-summary-body  Activate the split-summary-body formatter : Split the
                            summary and body of a docstring based on a period in
                            between them. This formatter is currently optional as
                            its considered somwehat opinionated and might require
                            major refactoring for existing projects.
      --no-split-summary-body
                            Deactivate the split-summary-body formatter.
