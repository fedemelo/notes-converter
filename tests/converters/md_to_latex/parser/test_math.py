from src.ir.nodes import DisplayMath, InlineMath, Paragraph, Text


def test_inline_math(parser):
    doc = parser.parse("Let $x = 1$.")
    assert doc.children == [
        Paragraph(children=[Text("Let "), InlineMath("x = 1"), Text(".")])
    ]


def test_inline_math_in_sentence(parser):
    doc = parser.parse("Sea $T$ un grafo simple.")
    assert doc.children == [
        Paragraph(children=[Text("Sea "), InlineMath("T"), Text(" un grafo simple.")])
    ]


def test_display_math(parser):
    doc = parser.parse("$$\nE = mc^2\n$$")
    assert doc.children == [DisplayMath(content="E = mc^2")]


def test_display_math_multiline(parser):
    doc = parser.parse("$$\na + b \\\\\n= c\n$$")
    assert doc.children == [DisplayMath(content="a + b \\\\\n= c")]


def test_display_math_gather_env(parser):
    src = "$$\n\\begin{gather*}\nX = 1 \\\\\nY = 2\n\\end{gather*}\n$$"
    doc = parser.parse(src)
    assert doc.children == [
        DisplayMath(content="\\begin{gather*}\nX = 1 \\\\\nY = 2\n\\end{gather*}")
    ]


def test_display_math_equation_env(parser):
    src = "$$\n\\begin{equation}\nE = mc^2\n\\end{equation}\n$$"
    doc = parser.parse(src)
    assert doc.children == [
        DisplayMath(content="\\begin{equation}\nE = mc^2\n\\end{equation}")
    ]


def test_display_math_align_env(parser):
    src = "$$\n\\begin{align*}\na &= b \\\\\nc &= d\n\\end{align*}\n$$"
    doc = parser.parse(src)
    assert doc.children == [
        DisplayMath(content="\\begin{align*}\na &= b \\\\\nc &= d\n\\end{align*}")
    ]


def test_display_math_gather_inline_attached(parser):
    # $$ attached to surrounding text — dollarmath parses as math_inline_double,
    # not math_block; content should still carry the raw \begin{gather*} body.
    src = "before:$$\n\\begin{gather*}\nX = 1\n\\end{gather*}\n$$after"
    doc = parser.parse(src)
    para = doc.children[0]
    assert para.children[0] == Text("before:")
    assert para.children[1] == InlineMath(
        "\n\\begin{gather*}\nX = 1\n\\end{gather*}\n", display=True
    )
    assert para.children[2] == Text("after")


def test_inline_display_math(parser):
    # $$...$$ inline in a sentence — dollarmath used to mis-tokenize this,
    # treating the two $$ as separate single-dollar delimiters.
    doc = parser.parse(
        "denotado por $|G|$, como el número de vértices: "
        "$$|G| = |V|.$$"
        "Es usual usar $n$ para $n = |G|$."
    )
    para = doc.children[0]
    children = para.children
    assert children[0] == Text("denotado por ")
    assert children[1] == InlineMath("|G|")
    assert children[2] == Text(", como el número de vértices: ")
    assert children[3] == InlineMath("|G| = |V|.", display=True)
    assert children[4] == Text("Es usual usar ")
    assert children[5] == InlineMath("n")
    assert children[6] == Text(" para ")
    assert children[7] == InlineMath("n = |G|")
    assert children[8] == Text(".")
