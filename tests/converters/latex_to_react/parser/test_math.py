from src.ir.nodes import DisplayMath, InlineMath, Paragraph, Text
from src.parsers.latex.latex import LatexParser


def parse(src):
    return LatexParser().parse(src)


def test_inline_math_dollar():
    doc = parse("$x$")
    assert doc.children == [Paragraph(children=[InlineMath(content="x")])]


def test_inline_math_dollar_expression():
    doc = parse("$x^2 + y^2$")
    assert doc.children[0].children == [InlineMath(content="x^2 + y^2")]


def test_inline_math_paren():
    doc = parse(r"\(x\)")
    assert doc.children[0].children == [InlineMath(content="x")]


def test_inline_math_paren_expression():
    doc = parse(r"\(a + b\)")
    assert doc.children[0].children == [InlineMath(content="a + b")]


def test_dollar_dollar_is_display_math():
    doc = parse("$$E = mc^2$$")
    assert doc.children == [DisplayMath(content="E = mc^2")]


def test_dollar_dollar_in_surrounding_text_splits_into_blocks():
    doc = parse("Sea $$E = mc^2$$ la ecuación.")
    assert doc.children == [
        Paragraph(children=[Text("Sea")]),
        DisplayMath(content="E = mc^2"),
        Paragraph(children=[Text("la ecuación.")]),
    ]


def test_block_math_bracket_single_line():
    doc = parse(r"\[E = mc^2\]")
    assert doc.children == [DisplayMath(content="E = mc^2")]


def test_block_math_bracket_multiline():
    doc = parse("\\[\nE = mc^2\n\\]")
    assert doc.children == [DisplayMath(content="\nE = mc^2\n")]


def test_equation_star_environment():
    doc = parse(r"\begin{equation*}E = mc^2\end{equation*}")
    assert doc.children == [DisplayMath(content="E = mc^2")]


def test_equation_star_environment_multiline():
    doc = parse("\\begin{equation*}\nE = mc^2\n\\end{equation*}")
    assert doc.children == [DisplayMath(content="\nE = mc^2\n")]


def test_gather_star_rewraps():
    body = "\nX = 1 \\\\\nY = 2\n"
    src = f"\\begin{{gather*}}{body}\\end{{gather*}}"
    doc = parse(src)
    assert doc.children == [
        DisplayMath(content=rf"\begin{{gather*}}{body}\end{{gather*}}")
    ]


def test_align_star_rewraps():
    body = "\na &= b \\\\\nc &= d\n"
    src = f"\\begin{{align*}}{body}\\end{{align*}}"
    doc = parse(src)
    assert doc.children == [
        DisplayMath(content=rf"\begin{{align*}}{body}\end{{align*}}")
    ]
