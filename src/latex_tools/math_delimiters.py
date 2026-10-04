from enum import Enum


class MathDelimiterStyle(str, Enum):
    """How math is delimited in rendered LaTeX: TeX-style $ / $$, or proper LaTeX \\(\\) / \\[\\]."""

    DOLLAR = "dollar"
    LATEX = "latex"


DEFAULT_MATH_DELIMITER_STYLE = MathDelimiterStyle.LATEX

_INLINE_DELIMITERS = {
    MathDelimiterStyle.DOLLAR: ("$", "$"),
    MathDelimiterStyle.LATEX: (r"\(", r"\)"),
}

_DISPLAY_DELIMITERS = {
    MathDelimiterStyle.DOLLAR: ("$$", "$$"),
    MathDelimiterStyle.LATEX: (r"\[", r"\]"),
}


def inline_math_delimiters(style: MathDelimiterStyle) -> tuple[str, str]:
    return _INLINE_DELIMITERS[MathDelimiterStyle(style)]


def display_math_delimiters(style: MathDelimiterStyle) -> tuple[str, str]:
    return _DISPLAY_DELIMITERS[MathDelimiterStyle(style)]
