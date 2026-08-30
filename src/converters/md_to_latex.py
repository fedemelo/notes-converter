from enum import Enum

from src.parsers.markdown.obsidian import ObsidianMarkdownParser
from src.renderers.latex import DEFAULT_CODE_COMMAND, LatexRenderer

_parser = ObsidianMarkdownParser()


class CodeCommand(str, Enum):
    """LaTeX commands available for typesetting inline code, each taking one {argument}."""

    TEXTT = DEFAULT_CODE_COMMAND
    INLINE = "Inline"


def convert_md_to_latex(text: str, code_command: str = DEFAULT_CODE_COMMAND) -> str:
    renderer = LatexRenderer(code_command=code_command)
    return renderer.render(_parser.parse(text))
