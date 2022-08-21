Usage
=====

Current usage of ``pydocstringformatter``:

.. code-block:: shell

    usage: pydocstringformatter [-h] [-w] [--quiet] [-v] [--exclude EXCLUDE]
                                [--exit-code] [--max-summary-lines int]
                                [--summary-quotes-same-line]
                                [--max-line-length int]
                                [--style {pep257,numpydoc} [{pep257,numpydoc} ...]]
                                [--strip-whitespaces  --no-strip-whitespaces]
                                [--split-summary-body  --no-split-summary-body]
                                [--linewrap-full-docstring  --no-linewrap-full-docstring]
                                [--beginning-quotes  --no-beginning-quotes]
                                [--closing-quotes  --no-closing-quotes]
                                [--capitalize-first-letter  --no-capitalize-first-letter]
                                [--final-period  --no-final-period]
                                [--quotes-type  --no-quotes-type]
                                [--numpydoc-section-order  --no-numpydoc-section-order]
                                [--numpydoc-name-type-spacing  --no-numpydoc-name-type-spacing]
                                [--numpydoc-section-spacing  --no-numpydoc-section-spacing]
                                [--numpydoc-section-hyphen-length  --no-numpydoc-section-hyphen-length]
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
      --exit-code           Turn on if the program should exit with bitwise exit
                            codes. 0 = No changes, 32 = Changed files or printed
                            diff.
      --max-summary-lines int
                            The maximum numbers of lines a summary can span. The
                            default value is 1.
      --summary-quotes-same-line
                            Force the start of a multi-line docstring to be on the
                            same line as the opening quotes. Similar to how this
                            is enforced for single line docstrings.
      --max-line-length int
                            Maximum line length of docstrings.
      --style {pep257,numpydoc} [{pep257,numpydoc} ...]
                            Docstring styles that are used in the project. Can be
                            more than one.

    default formatters:
      these formatters are turned on by default

      --strip-whitespaces, --no-strip-whitespaces
                            Activate or deactivate strip-whitespaces: Strip 1)
                            docstring start, 2) docstring end and 3) end of line.
                            Styles: default. (default: True)
      --split-summary-body, --no-split-summary-body
                            Activate or deactivate split-summary-body: Split the
                            summary and body of a docstring based on a period and
                            max length. The maximum length of a summary can be set
                            with the --max-summary-lines option. Styles: pep257.
                            (default: True)
      --beginning-quotes, --no-beginning-quotes
                            Activate or deactivate beginning-quotes: Fix the
                            position of the opening quotes. Styles: default.
                            (default: True)
      --closing-quotes, --no-closing-quotes
                            Activate or deactivate closing-quotes: Fix the
                            position of the closing quotes. Styles: default.
                            (default: True)
      --capitalize-first-letter, --no-capitalize-first-letter
                            Activate or deactivate capitalize-first-letter:
                            Capitalize the first letter of the docstring if
                            appropriate. Styles: default. (default: True)
      --final-period, --no-final-period
                            Activate or deactivate final-period: Add a period to
                            the end of single line docstrings and summaries.
                            Styles: default. (default: True)
      --quotes-type, --no-quotes-type
                            Activate or deactivate quotes-type: Change all opening
                            and closing quotes to be triple quotes. Styles:
                            default. (default: True)
      --numpydoc-section-order, --no-numpydoc-section-order
                            Activate or deactivate numpydoc-section-order: Change
                            section order to match numpydoc guidelines. Styles:
                            numpydoc. (default: True)
      --numpydoc-name-type-spacing, --no-numpydoc-name-type-spacing
                            Activate or deactivate numpydoc-name-type-spacing:
                            Ensure proper spacing around the colon separating
                            names from types. Styles: numpydoc. (default: True)
      --numpydoc-section-spacing, --no-numpydoc-section-spacing
                            Activate or deactivate numpydoc-section-spacing:
                            Ensure proper spacing between sections. Styles:
                            numpydoc. (default: True)
      --numpydoc-section-hyphen-length, --no-numpydoc-section-hyphen-length
                            Activate or deactivate numpydoc-section-hyphen-length:
                            Ensure hyphens after section header lines are proper
                            length. Styles: numpydoc. (default: True)

    optional formatters:
      these formatters are turned off by default

      --linewrap-full-docstring, --no-linewrap-full-docstring
                            Activate or deactivate linewrap-full-docstring:
                            Linewrap the docstring by the pre-defined line length.
                            Styles: default. (default: False)
