from __future__ import annotations

from collections import OrderedDict

from pydocstringformatter._formatting.base import NumpydocSectionFormatter


class NumpydocSectionOrderingFormatter(NumpydocSectionFormatter):
    """Change section order to match numpydoc guidelines."""

    name = "numpydoc-section-order"

    numpydoc_section_order = (
        "Summary",
        "Parameters",
        "Attributes",
        "Methods",
        "Returns",
        "Yields",
        "Receives",
        "Other Parameters",
        "Raises",
        "Warns",
        "Warnings",
        "See Also",
        "Notes",
        "References",
        "Examples",
    )

    def treat_sections(
        self, sections: OrderedDict[str, list[str]]
    ) -> OrderedDict[str, list[str]]:
        """Sort the numpydoc sections into the numpydoc order."""
        for sec_name in reversed(self.numpydoc_section_order):
            try:
                sections.move_to_end(sec_name, last=False)
            except KeyError:
                pass
        return sections


class NumpydocNameColonTypeFormatter(NumpydocSectionFormatter):
    """Ensure proper spacing around the colon separating names from types."""

    name = "numpydoc-name-type-spacing"

    numpydoc_sections_with_parameters = (
        "Parameters",
        "Attributes",
        "Returns",
        "Yields",
        "Receives",
        "Other Parameters",
        "See Also",
    )

    def treat_sections(
        self, sections: OrderedDict[str, list[str]]
    ) -> OrderedDict[str, list[str]]:
        """Ensure proper spacing around the colon separating names from types."""
        for section_name, section_lines in sections.items():
            if section_name in self.numpydoc_sections_with_parameters:
                # Any section that gets here has a line of hyphens
                initial_indent = section_lines[1].index("-")
                for index, line in enumerate(section_lines):
                    if (
                        # There is content on this line (at least the initial indent)
                        len(line) > initial_indent
                        # and the first character after the indent for
                        # the docstring is a name, not an additional
                        # indent indicating a description rather than
                        # a line with name and type
                        and not line[initial_indent].isspace()
                        # and there is a colon to separate the name
                        # from the type (functions returning only one
                        # thing don't put a name in their "Returns"
                        # section)
                        and ":" in line
                    ):
                        line_name, line_type = line.split(":", 1)
                        if line_type:
                            # Avoid adding trailing whitespace
                            # Colon ending first line is suggested for long
                            # "See Also" links
                            section_lines[index] = (
                                f"{line_name.rstrip():s} : {line_type.lstrip():s}"
                            )
        return sections


class NumpydocSectionSpacingFormatter(NumpydocSectionFormatter):
    """Ensure proper spacing between sections."""

    name = "numpydoc-section-spacing"

    def treat_sections(
        self, sections: OrderedDict[str, list[str]]
    ) -> OrderedDict[str, list[str]]:
        """Ensure proper spacing between sections."""
        for section_lines in sections.values():
            last_line = section_lines[-1]
            if not (last_line == "" or last_line.isspace()) and len(sections) > 1:
                section_lines.append("")
        return sections


class NumpydocSectionHyphenLengthFormatter(NumpydocSectionFormatter):
    """Ensure hyphens after section header lines are proper length."""

    name = "numpydoc-section-hyphen-length"

    def treat_sections(
        self, sections: OrderedDict[str, list[str]]
    ) -> OrderedDict[str, list[str]]:
        """Ensure section header lines are proper length."""
        first_section = True
        for section_name, section_lines in sections.items():
            if section_name != "Summary":
                # Skip the summary, deprecation warning and extended
                # summary.  They have neither a section header nor the
                # line of hyphens after it.
                indent_length = section_lines[1].index("-")
                section_lines[1] = " " * indent_length + "-" * len(section_name)
                if first_section:
                    # If the second line were not hyphens, the section name
                    # would be summary.  This assumes triple quotes, but that
                    # seems fine for a multi-line docstring.
                    section_lines[1] = f"{section_lines[1]:s}---"
            first_section = False
        return sections
