from __future__ import annotations

import re

import lsprotocol.types as lsp

from server import LSP_SERVER
from utils.code_parser import FuncParser, NotFuncException


@LSP_SERVER.feature(
    lsp.TEXT_DOCUMENT_COMPLETION, lsp.CompletionOptions(
        trigger_characters=['"'])
)
def completions(params: lsp.CompletionParams) -> None | lsp.CompletionList:
    """
    Completes the code snippet with a docstring if the cursor is at the beginning of a function definition.

    Args:
        params (lsp.CompletionParams): The completion parameters containing the cursor position and text document URI.

    Returns:
        None | lsp.CompletionList: Returns None if the cursor is not at the beginning of a function definition, otherwise returns a completion list with the generated docstring.
    """
    cursor = params.position
    uri = params.text_document.uri
    document = LSP_SERVER.workspace.get_document(uri)
    source = document.source

    validate = document.lines[cursor.line][0: cursor.character]
    if re.match(r'^(\s{4})+"""$', validate):
        try:
            parsed_func = FuncParser(source, cursor)
        except NotFuncException:
            return
        if cursor.line != parsed_func.suite.line:
            return
        completion_text = (
            "" if parsed_func.docstring_range else 'Await docstring generation..."""'
        )
        return _create_completion_list(cursor, completion_text)
    return


def _create_completion_list(
    cursor: lsp.Position, completion_text: str
) -> lsp.CompletionList:
    """
    Create a completion list for generating a docstring using ChatGPT.

    Args:
        cursor (lsp.Position): The cursor position.
        completion_text (str): The completion text for the docstring.

    Returns:
        lsp.CompletionList: A completion list with a single item for generating a docstring using ChatGPT.
    """
    return lsp.CompletionList(
        is_incomplete=False,
        items=[
            lsp.CompletionItem(
                label="Generate Docstring (ChatGPT)",
                kind=lsp.CompletionItemKind.Text,
                text_edit=lsp.TextEdit(
                    range=lsp.Range(start=cursor, end=cursor),
                    new_text=completion_text,
                ),
                command=lsp.Command(
                    title="Generate Docstring (ChatGPT)",
                    command="chatgpt-docstrings.generateDocstring",
                ),
            ),
        ],
    )
