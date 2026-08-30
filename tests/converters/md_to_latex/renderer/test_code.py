from src.ir.nodes import InlineCode
from src.renderers.latex import LatexRenderer


def test_inline_code_default_command(renderer):
    assert renderer._render_inline(InlineCode("M")) == r"\texttt{M}"


def test_inline_code_escapes_special_characters(renderer):
    assert renderer._render_inline(InlineCode("M[i][j] = 1")) == r"\texttt{M[i][j] = 1}"
    assert renderer._render_inline(InlineCode("50%")) == r"\texttt{50\%}"


def test_inline_code_custom_command():
    renderer = LatexRenderer(code_command="Inline")
    assert renderer._render_inline(InlineCode("M")) == r"\Inline{M}"
