from __future__ import annotations

import re
from typing import Any

from docutils import nodes
from sphinx import addnodes, application
from sphinx.transforms import SphinxTransform

DOCUMENTATION_LINK = "https://pydocstringformatter.readthedocs.io/en/latest/"


class LinkTransformer(SphinxTransform):
    """Transformer to make all internal links actually internal.

    For example:
    Transforms https://pydocstringformatter.readthedocs.io/en/latest/usage.html
    into a link to docs/usage.rst.
    """

    # Set priority very low so that we run after everything else has been done
    default_priority = 1000

    docs_regex = re.compile(r".*[/\\]docs[/\\]")

    def apply(self, **_: dict[str, Any]) -> None:
        """Apply the transformation."""
        for node in self.document.traverse(nodes.reference):
            if (
                "refuri" in node
                and node["refuri"].startswith(DOCUMENTATION_LINK)
                # Don't 'fix' the ReadTheDocs badge
                and not node["refuri"].endswith("?badge=latest")
            ):
                # Get the ref link
                link = node["refuri"].replace(DOCUMENTATION_LINK, "")
                link = link.replace(".html", ".rst")

                # Get the source link
                source_link = self.document["source"]
                source_link = re.sub(self.docs_regex, "", source_link)
                source_link = source_link.replace(".rst", "")

                # Create pending xref
                ref = addnodes.pending_xref(
                    refdoc=source_link,
                    reftype="myst",
                    reftarget=link,
                    refexplicit=True,
                    refdomain=True,
                    refwarn=True,
                )

                # Make inline and add text for link
                inline = nodes.inline(classes=["xref", "myst"])
                inline += node.children[0]
                ref += inline

                # Replace previous link
                node.parent.replace(node, ref)


def setup(app: application.Sphinx) -> None:
    """Required function to register the Sphinx extension."""
    app.add_transform(LinkTransformer)
