import subprocess

from sphinx import application


def write_usage_page() -> None:
    """Write docs/usage.rst."""

    # Get the help message
    with subprocess.Popen(
        ["pydocstringformatter", "-h"], stdout=subprocess.PIPE
    ) as proc:
        assert proc.stdout
        out = proc.stdout.readlines()

    # Add correct indentation for the code block
    help_message = "    ".join(i.decode("utf-8") for i in out)
    # Remove indentation from completely empty lines
    help_message = help_message.replace("    \n", "\n")

    with open("usage.rst", mode="w", encoding="utf-8") as file:
        file.write(f"""Usage
=====

Current usage of ``pydocstringformatter``:

.. code-block:: shell

    {help_message}""")


def setup(_: application.Sphinx) -> None:
    """Required function to register the Sphinx extension."""
    write_usage_page()
