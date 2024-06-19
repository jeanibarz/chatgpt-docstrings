from __future__ import annotations

import lsprotocol.types as lsp
from pygls import workspace


def create_workspace_edit(
    document: lsp.Document, text_edits: list[lsp.TextEdit]
) -> lsp.WorkspaceEdit:
    """
    Creates a workspace edit object to apply text edits to a document.

    Args:
        document (lsp.Document): The document to be edited.
        text_edits (list[lsp.TextEdit]): List of text edits to be applied.

    Returns:
        lsp.WorkspaceEdit: A workspace edit object containing the document changes with the specified text edits.
    """
    return lsp.WorkspaceEdit(
        document_changes=[
            lsp.TextDocumentEdit(
                text_document=lsp.VersionedTextDocumentIdentifier(
                    uri=document.uri,
                    version=0 if document.version is None else document.version,
                ),
                edits=text_edits,
            )
        ]
    )


def get_line_endings(lines: list[str]) -> str:
    """
    Return the line ending used in the given list of lines.

    Args:
        lines (list[str]): A list of strings representing lines of text.

    Returns:
        str: The line ending used in the lines. Returns "\r\n" if the first line ends with "\r\n", otherwise returns "\n".
        Returns None if an exception occurs.
    """
    try:
        if lines[0][-2:] == "\r\n":
            return "\r\n"
        return "\n"
    except Exception:
        return None


def match_line_endings(document: workspace.Document, text: str) -> str:
    """
    Returns the text with line endings matching the document's line endings.

    Args:
        document (workspace.Document): The document to match line endings with.
        text (str): The text to adjust line endings for.

    Returns:
        str: The text with line endings adjusted to match the document's line endings.
    """
    expected = get_line_endings(document.source.splitlines(keepends=True))
    actual = get_line_endings(text.splitlines(keepends=True))
    if actual == expected or actual is None or expected is None:
        return text
    return text.replace(actual, expected)
