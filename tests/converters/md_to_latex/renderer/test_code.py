from src.ir.nodes import CodeBlock, InlineCode
from src.renderers.latex import LatexRenderer


def test_inline_code_default_command(renderer):
    assert renderer._render_inline(InlineCode("M")) == r"\texttt{M}"


def test_inline_code_escapes_special_characters(renderer):
    assert renderer._render_inline(InlineCode("M[i][j] = 1")) == r"\texttt{M[i][j] = 1}"
    assert renderer._render_inline(InlineCode("50%")) == r"\texttt{50\%}"


def test_inline_code_custom_command():
    renderer = LatexRenderer(inline_code_command="Inline")
    assert renderer._render_inline(InlineCode("M")) == r"\Inline{M}"


def test_code_block_default_environment(renderer):
    assert (
        renderer._render_block(CodeBlock("def f():\n    pass"))
        == "\\begin{verbatim}\ndef f():\n    pass\n\\end{verbatim}"
    )


def test_code_block_custom_environment():
    renderer = LatexRenderer(code_block_environment="pseudocode")
    assert (
        renderer._render_block(CodeBlock("if x then y"))
        == "\\begin{pseudocode}\nif x then y\n\\end{pseudocode}"
    )
