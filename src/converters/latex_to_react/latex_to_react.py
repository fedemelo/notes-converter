from re import DOTALL, IGNORECASE, Match, compile, error, escape

from fastapi import UploadFile

from src.exceptions import RegexProcessingError, conversion_error_handler
from src.latex_tools.tex_reader import decode_file_to_string


@conversion_error_handler
async def convert_tex_to_react(file: UploadFile) -> str:
    tex_content = await decode_file_to_string(file)
    react_content = convert_latex_code_to_react(tex_content)
    return react_content


def convert_latex_code_to_react(tex_content: str) -> str:

    stages = {
        # Temporarily remove ref commands
        "removing \\ref commands": (r"\\ref\{(.+?)\}", ""),
        "removing \\autoref commands": (r"\\autoref\{(.+?)\}", ""),
        # Temporarily remove figures
        "removing figures": (regex_to_match_environment_content("figure"), ""),
        "removing \\noindent commands": (r"\\noindent\s?", ""),
        "replacing display math, $$, by custom LaTeX react component": (
            regex_to_match_between_delimiters(r"\$\$", r"\$\$"),
            transform_block_math,
        ),
        "replacing inline math, $, by custom LaTeX react component": (
            regex_to_match_between_delimiters(r"\$", r"\$"),
            transform_inline_math,
        ),
        "replacing display math, \\[, by custom LaTeX react component": (
            regex_to_match_between_delimiters(r"\\\[", r"\\\]"),
            transform_block_math,
        ),
        "replacing inline math, \\(, by custom LaTeX react component": (
            regex_to_match_between_delimiters(r"\\\(", r"\\\)"),
            transform_inline_math,
        ),
        "replacing block math within equation* environment": (
            regex_to_match_environment_content(r"equation*"),
            transform_block_math,
        ),
        "replacing block math within_gather* environment": (
            regex_to_match_environment_content(r"gather*"),
            transform_gather_block_math,
        ),
        "replacing block math within align* environment": (
            regex_to_match_environment_content(r"align*"),
            transform_align_block_math,
        ),
        "replacing parts by level 1 headers": (
            regex_to_match_command_content("part"),
            regex_to_put_content_in_html_tag("h1"),
        ),
        "replacing sections by level 2 headers": (
            regex_to_match_command_content("section"),
            regex_to_put_content_in_html_tag("h2"),
        ),
        "replacing subsections by level 3 headers": (
            regex_to_match_command_content("subsection"),
            regex_to_put_content_in_html_tag("h3"),
        ),
        "replacing subsubsections by level 4 headers": (
            regex_to_match_command_content("subsubsection"),
            regex_to_put_content_in_html_tag("h4"),
        ),
        "formatting bold text": (
            regex_to_match_command_content("textbf"),
            regex_to_put_content_in_html_tag("b"),
        ),
        "formatting italic text": (
            regex_to_match_command_content("textit"),
            regex_to_put_content_in_html_tag("i"),
        ),
        "formatting underlined text": (
            regex_to_match_command_content("underline"),
            regex_to_put_content_in_html_tag("u"),
        ),
        "formatting emphasized text": (
            regex_to_match_command_content("emph"),
            regex_to_put_content_in_html_tag("em"),
        ),
        "replacing list items": (
            r"\\item(.+?)\n",
            regex_to_put_content_in_html_tag("li") + "\n",
        ),
        "replace itemize environment by ul tag": (
            regex_to_match_environment_content("itemize"),
            regex_to_put_content_in_html_tag("ul"),
        ),
        "replace enumerate environment by ol tag": (
            regex_to_match_environment_content("enumerate"),
            regex_to_put_content_in_html_tag("ol"),
        ),
        "replace tip environment by custom react component": (
            regex_to_match_environment_content("tip"),
            regex_to_put_content_in_html_tag("Tip"),
        ),
        "replace warning environment by custom react component": (
            regex_to_match_environment_content("advertencia"),
            regex_to_put_content_in_html_tag("Warning"),
        ),
        "replace notacion environment by custom react component": (
            regex_to_match_environment_content("notacion"),
            regex_to_put_content_in_html_tag("Notation"),
        ),
        "replace definicion environment by custom react component": (
            regex_to_match_definition_environment(),
            transform_definition_environment,
        ),
        "replace ejemplo environment by custom react component": (
            regex_to_match_ejemplo_environment(),
            transform_ejemplo_environment,
        ),
        "replace teorema environment by custom react component": (
            regex_to_match_teorema_environment(),
            transform_teorema_environment,
        ),
        "converting latex comments to html comments": (
            r"%([^\n]*?)(\n)",
            r"{/* \1 */}",
        ),
        "replacing say by double quotes": (
            regex_to_match_command_content("say"),
            r'"\1"',
        ),
        "removing \\hyperlink commands": (
            regex_to_match_hyperlink_command(),
            transform_hyperlink_command,
        ),
        "removing labels": (regex_to_match_command_content("label"), ""),
        "removing vspace commands": (regex_to_match_command_content("vspace"), ""),
        "replace paragraph commands by h5 headers": (
            regex_to_match_command_content("paragraph"),
            regex_to_put_content_in_html_tag("h5"),
        ),
    }

    for stage, pattern in stages.items():
        regex, replacement = pattern
        try:
            tex_content = compile(regex).sub(replacement, tex_content)
            print(stage[0].upper() + stage[1:])
        except error as e:
            raise RegexProcessingError(stage, pattern, str(e))
    return tex_content


def transform_block_math(match: Match) -> str:
    """
    Enclose in my custom react LaTeX block component.
    """
    content = match.group(1)
    return wrap_in_react_latex(content, block=True)


def wrap_in_react_latex(content: str, block: bool = False) -> str:
    if block:
        return (
            """<M block>
    {r`"""
            + content
            + """`}
</M>"""
        )
    else:
        return "<M>{r`" + content + "`}</M>"


def transform_inline_math(match: Match) -> str:
    """Enclose in my custom react LaTeX inline component"""
    content = match.group(1)
    return wrap_in_react_latex(content)


def transform_gather_block_math(match: Match) -> str:
    content = match.group(1)
    re_add_gather = r"\begin{gather*}" + content + r"\end{gather*}"
    return wrap_in_react_latex(re_add_gather, block=True)


def transform_align_block_math(match: Match) -> str:
    content = match.group(1)
    re_add_align = r"\begin{align*}" + content + r"\end{align*}"
    return wrap_in_react_latex(re_add_align, block=True)


def regex_to_match_between_delimiters(bgin_delimiter: str, end_delimiter: str) -> str:
    """Recieves a delimiter and returns a regex to match content between two delimiters.
    If a delimiter is a special character in regex, it must be escaped. E.g: $ -> \\$
    """
    # Caveat:

    # As the match is non-greedy, it will match the shortest possible content between
    # the delimiters. That means that if the end_delimiter character appears in the
    # content, the match will end at its first occurrence, which in most cases is not
    # the desired behavior.

    # That could be fixed by doing a proper parsing of the content, but that would be
    # a much more complex solution, and given that this is much of a specific use case,
    # I don't think it's worth the effort.
    return bgin_delimiter + r"(.+?)" + end_delimiter


def regex_to_match_command_content(command: str) -> str:
    """Recieves a command and returns a regex to match content between curly braces
    after the command."""
    # Same caveat as the previous function: if the content contains the closing curly
    # brace, the match will end at its first occurrence, which is not the desired
    # behavior.
    return r"\\" + command + r"\{(.+?)\}"


def regex_to_match_environment_content(environment: str) -> str:
    """Receives an environment and returns a regex to match content between the begin
    and end of the environment, including content that spans multiple lines."""
    pattern = (
        r"\\begin\{"
        + escape(environment)
        + r"\}(.+?)\\end\{"
        + escape(environment)
        + r"\}"
    )
    return compile(pattern, DOTALL)


def regex_to_put_content_in_html_tag(tag: str) -> str:
    """Recieves an html tag and returns a regex to wrap matched content in the tag."""
    return "<" + tag + r">\1</" + tag + ">"


def regex_to_match_definition_environment() -> str:
    """Regex to match definicion environment with two parameters, case-insensitive."""
    pattern = r"\\begin\{definicion\}\{(.+?)\}\{(.*?)\}(.+?)\\end\{definicion\}"
    return compile(pattern, DOTALL | IGNORECASE)


def transform_definition_environment(match: Match) -> str:
    concept = match.group(1)
    content = match.group(3).strip()
    return f'<Definition concept="{concept}">\n    {content}\n</Definition>'


def regex_to_match_ejemplo_environment() -> str:
    """Regex to match ejemplo environment with two parameters, case-insensitive."""
    pattern = r"\\begin\{ejemplo\}\{(.+?)\}\{(.*?)\}(.+?)\\end\{ejemplo\}"
    return compile(pattern, DOTALL | IGNORECASE)


def regex_to_match_teorema_environment() -> str:
    """Regex to match teorema environment with two parameters, case-insensitive."""
    pattern = r"\\begin\{teorema\}\{(.+?)\}\{(.*?)\}(.+?)\\end\{teorema\}"
    return compile(pattern, DOTALL | IGNORECASE)


def transform_ejemplo_environment(match: Match) -> str:
    title = match.group(1).strip()
    content = match.group(3).strip()
    content = content.replace(r"\(", "<M>").replace(r"\)", "</M>")

    if title:
        return f'<Example title="{title}">\n {content}\n</Example>'
    else:
        return f"<Example>\n {content}\n</Example>"


def transform_teorema_environment(match: Match) -> str:
    name = match.group(1).strip()
    content = match.group(3).strip()
    content = content.replace(r"\(", "<M>").replace(r"\)", "</M>")

    if name:
        return f'<Theorem name="{name}">\n    {content}\n</Theorem>'
    else:
        return f"<Theorem>\n    {content}\n</Theorem>"


def regex_to_match_hyperlink_command() -> str:
    """Regex to match \\hyperlink command with two parameters."""
    pattern = r"\\hyperlink\{(.+?)\}\{(.+?)\}"
    return compile(pattern)


def transform_hyperlink_command(match: Match) -> str:
    """Extract the visible text from the \\hyperlink command."""
    visible_text = match.group(2)
    return visible_text
