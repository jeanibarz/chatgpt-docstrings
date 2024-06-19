import re
import openai


async def get_docstring(api_key: str, model: str, prompt: str) -> str:
    """
    Get a docstring using OpenAI's ChatCompletion API.

    Args:
        api_key (str): The API key for accessing OpenAI's API.
        model (str): The model to use for generating the docstring.
        prompt (str): The prompt to provide for generating the docstring.

    Returns:
        str: The generated docstring string.
    """
    openai.api_key = api_key
    response = await openai.ChatCompletion.acreate(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "When you generate a docstring, "
                    "return me only a string that I can add to my code."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )
    docstring = response.choices[0].message.content
    return docstring


def format_docstring(
    docstring: str, indent_level: int, docs_new_line: bool, quotes_new_line: bool
) -> str:
    """
    Format the given docstring with specified indent level, new lines for docs, and new lines for quotes.

    Args:
        docstring (str): The original docstring to format.
        indent_level (int): The number of spaces to indent the docstring.
        docs_new_line (bool): Whether to add new lines around the docstring content.
        quotes_new_line (bool): Whether to add a new line for opening quotes.

    Returns:
        str: The formatted docstring.
    """
    if not docstring:
        return '"""\n\n"""' if docs_new_line else '""""""'

    pattern = r'(?:"""([^"]*?)"""|\'\'\'([^\']*?)\'\'\')'
    while True:
        match = re.search(pattern, docstring, re.DOTALL)
        if match:
            matched_content = match.group(0)
            # Remove triple quotes and strip whitespace
            inner_content = matched_content[3:-3].strip()

            # Replace original matched content with inner content
            docstring = docstring[:match.start()] + \
                inner_content + docstring[match.end():]
        else:
            break

    # Match the content within triple double or triple single quotes
    match = re.search(r'(?:"""([^"]*?)"""|\'\'\'([^\']*?)\'\'\')',
                      docstring, flags=re.DOTALL)
    if match:
        docstring = match.group()

    # Remove leading and trailing whitespaces, newlines, and quotes
    docstring = docstring.strip().strip('"""').strip("'''").strip()

    # Remove leading indents from each line
    lines = docstring.splitlines()
    if len(lines) > 1:
        # Find the minimum indentation level
        min_indent = min(len(line) - len(line.lstrip())
                         for line in lines[1:] if line.strip())

        # Adjust the indentation of lines
        adjusted_lines = []
        for idx, line in enumerate(lines):
            if idx == 0:
                adjusted_lines.append(line)
            else:
                adjusted_lines.append(line[min_indent:])

    # Join the lines back into a single string
    docstring = "\n".join(adjusted_lines)

    # Add new lines around the docstring content if required
    if docs_new_line:
        docstring = f"\n{docstring}\n"
    else:
        docstring = f"{docstring}\n"

    # Add quotes
    docstring = f'"""{docstring}"""'

    # Add indents
    indents = " " * indent_level * 4
    docstring = "\n".join([f"{indents}{line}" if line.strip(
    ) else line for line in docstring.splitlines()])

    # Add new line for opening quotes if required
    if quotes_new_line:
        docstring = f"\n{docstring}"

    return docstring
