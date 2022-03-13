Usage
=====

Current usage of ``pydocstringformatter``:

.. code-block:: shell

    usage: pydocstringformatter [-h] [-w] [--quiet] [-v] [--exclude EXCLUDE]
                                [--max-summary-lines MAX_SUMMARY_LINES]
                                [--summary-quotes-same-line]
                                [--split-summary-body  --no-split-summary-body]
                                [--strip-whitespaces  --no-strip-whitespaces]
                                [--beginning-quotes  --no-beginning-quotes]
                                [--closing-quotes  --no-closing-quotes]
                                [--capitalize-first-letter  --no-capitalize-first-letter]
                                [--final-period  --no-final-period]
                                [--quotes-type  --no-quotes-type]
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
      --max-summary-lines MAX_SUMMARY_LINES
                            The maximum numbers of lines a summary can span. The
                            default value is 1.
      --summary-quotes-same-line
                            Force the start of a multi-line docstring to be on the
                            same line as the opening quotes. Similar to how this
                            is enforced for single line docstrings.

    default formatters:
      these formatters are turned on by default

      --strip-whitespaces, --no-strip-whitespaces
                            Activate or deactivate strip-whitespaces: Strip 1)
                            docstring start, 2) docstring end and 3) end of line.
                            (default: True)
      --beginning-quotes, --no-beginning-quotes
                            Activate or deactivate beginning-quotes: Fix the
                            position of the opening quotes. (default: True)
      --closing-quotes, --no-closing-quotes
                            Activate or deactivate closing-quotes: Fix the
                            position of the closing quotes. (default: True)
      --capitalize-first-letter, --no-capitalize-first-letter
                            Activate or deactivate capitalize-first-letter:
                            Capitalize the first letter of the docstring if
                            appropriate. (default: True)
      --final-period, --no-final-period
                            Activate or deactivate final-period: Add a period to
                            the end of single line docstrings and summaries.
                            (default: True)
      --quotes-type, --no-quotes-type
                            Activate or deactivate quotes-type: Change all opening
                            and closing quotes to be triple quotes. (default:
                            True)

    optional formatters:
      these formatters are turned off by default

      --split-summary-body, --no-split-summary-body
                            Activate or deactivate split-summary-body: Split the
                            summary and body of a docstring based on a period and
                            max length. The maximum length of a summary can be set
                            with the --max-summary-lines option. This formatter is
                            currently optional as its considered somwehat
                            opinionated and might require major refactoring for
                            existing projects. (default: False)
