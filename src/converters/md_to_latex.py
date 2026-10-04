from enum import Enum

from src.latex_tools.math_delimiters import DEFAULT_MATH_DELIMITER_STYLE, MathDelimiterStyle
from src.parsers.markdown.obsidian import ObsidianMarkdownParser
from src.renderers.latex import (
    DEFAULT_CODE_BLOCK_ENVIRONMENT,
    DEFAULT_INLINE_CODE_COMMAND,
    LatexRenderer,
)

_parser = ObsidianMarkdownParser()


class InlineCodeCommand(str, Enum):
    """LaTeX commands available for typesetting inline code, each taking one {argument}."""

    TEXTT = DEFAULT_INLINE_CODE_COMMAND
    INLINE = "Inline"


class CodeBlockEnvironment(str, Enum):
    """LaTeX environments available for typesetting fenced code blocks."""

    VERBATIM = DEFAULT_CODE_BLOCK_ENVIRONMENT
    PSEUDOCODE = "pseudocode"


def convert_md_to_latex(
    text: str,
    inline_code_command: str = DEFAULT_INLINE_CODE_COMMAND,
    code_block_environment: str = DEFAULT_CODE_BLOCK_ENVIRONMENT,
    math_delimiter_style: str = DEFAULT_MATH_DELIMITER_STYLE.value,
) -> str:
    renderer = LatexRenderer(
        inline_code_command=inline_code_command,
        code_block_environment=code_block_environment,
        math_delimiter_style=MathDelimiterStyle(math_delimiter_style),
    )
    return renderer.render(_parser.parse(text))
