import re

# Display math must be matched before inline so that $$ isn't consumed as two
# separate $ delimiters.
_DISPLAY_RE = re.compile(r"(?<!\\)\$\$(.*?)\$\$", re.DOTALL)
_INLINE_RE = re.compile(r"(?<!\\)\$((?:[^$\\]|\\.)*?)\$")


def convert_latex_dollar_to_paren(source: str) -> str:
    result = _DISPLAY_RE.sub(r"\\[\1\\]", source)
    result = _INLINE_RE.sub(r"\\(\1\\)", result)
    return result
