from src.ir.nodes import DisplayMath, InlineMath
from src.renderers.latex import LatexRenderer


def test_inline_math_dollar_style():
    renderer = LatexRenderer(math_delimiter_style="dollar")
    assert renderer._render_inline(InlineMath("x = 1")) == "$x = 1$"


def test_display_math_dollar_style():
    renderer = LatexRenderer(math_delimiter_style="dollar")
    assert renderer._render_block(DisplayMath(content="E = mc^2")) == "$$\nE = mc^2\n$$"


def test_inline_display_math_dollar_style():
    renderer = LatexRenderer(math_delimiter_style="dollar")
    node = InlineMath("a + b", display=True)
    assert renderer._render_inline(node) == "$$\na + b\n$$"


def test_display_math_standalone_env_unaffected_by_style():
    content = "\\begin{gather*}\nX = 1\n\\end{gather*}"
    renderer = LatexRenderer(math_delimiter_style="dollar")
    assert renderer._render_block(DisplayMath(content=content)) == content


def test_math_delimiter_style_defaults_to_latex(renderer):
    assert renderer._render_inline(InlineMath("x = 1")) == r"\(x = 1\)"
