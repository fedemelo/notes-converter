from src.ir.nodes import Emphasis, Image, InlineMath, Ref, Strong, Text


def test_inline_math(renderer):
    assert renderer._render_inline(InlineMath("x = 1")) == r"\(x = 1\)"


def test_inline_display_math_plain(renderer):
    assert renderer._render_inline(InlineMath("a + b", display=True)) == "\\[\na + b\n\\]"


def test_inline_display_math_gather_no_brackets(renderer):
    content = "\n\\begin{gather*}\nX = 1 \\\\\nY = 2\n\\end{gather*}\n"
    expected = "\\begin{gather*}\nX = 1 \\\\\nY = 2\n\\end{gather*}"
    assert renderer._render_inline(InlineMath(content, display=True)) == expected


def test_inline_display_math_align_no_brackets(renderer):
    content = "\n\\begin{align*}\na &= b\n\\end{align*}\n"
    expected = "\\begin{align*}\na &= b\n\\end{align*}"
    assert renderer._render_inline(InlineMath(content, display=True)) == expected


def test_inline_math_preserves_content(renderer):
    assert renderer._render_inline(InlineMath(r"\frac{a}{b}")) == r"\(\frac{a}{b}\)"


def test_emphasis(renderer):
    assert (
        renderer._render_inline(Emphasis(children=[Text("word")])) == r"\emph{word}"
    )


def test_strong(renderer):
    assert renderer._render_inline(Strong(children=[Text("word")])) == r"\textbf{word}"


def test_nested_emphasis_in_strong(renderer):
    node = Strong(children=[Text("a "), Emphasis(children=[Text("b")])])
    assert renderer._render_inline(node) == r"\textbf{a \emph{b}}"


def test_image_produces_figure(renderer):
    result = renderer._render_inline(Image(src="fig.png", alt="A graph"))
    assert r"\begin{figure}" in result
    assert r"\includegraphics{fig.png}" in result
    assert r"\caption{A graph}" in result
    assert r"\end{figure}" in result


def test_image_escapes_alt_text(renderer):
    result = renderer._render_inline(Image(src="fig.png", alt="50% data"))
    assert r"\caption{50\% data}" in result


def test_ref(renderer):
    node = Ref(label="sec:grafos_ponderados", text="grafo ponderado")
    assert (
        renderer._render_inline(node)
        == r"\hyperref[sec:grafos_ponderados]{grafo ponderado}"
    )
