import re

from src.latex_tools.math_delimiters import (
    MathDelimiterStyle,
    display_math_delimiters,
    inline_math_delimiters,
)

# Display math must be matched before inline so that $$ isn't consumed as two
# separate $ delimiters.
_DISPLAY_RE = re.compile(r"(?<!\\)\$\$(.*?)\$\$", re.DOTALL)
_INLINE_RE = re.compile(r"(?<!\\)\$((?:[^$\\]|\\.)*?)\$")

_DISPLAY_OPEN, _DISPLAY_CLOSE = display_math_delimiters(MathDelimiterStyle.LATEX)
_INLINE_OPEN, _INLINE_CLOSE = inline_math_delimiters(MathDelimiterStyle.LATEX)


def convert_latex_dollar_to_paren(source: str) -> str:
    result = _DISPLAY_RE.sub(
        lambda m: f"{_DISPLAY_OPEN}{m.group(1)}{_DISPLAY_CLOSE}", source
    )
    result = _INLINE_RE.sub(
        lambda m: f"{_INLINE_OPEN}{m.group(1)}{_INLINE_CLOSE}", result
    )
    return result
