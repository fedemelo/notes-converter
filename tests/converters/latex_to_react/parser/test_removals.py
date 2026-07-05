from src.ir.nodes import Figure, Paragraph, Ref, Text, VerticalSpace
from src.parsers.latex.latex import LatexParser


def parse(src):
    return LatexParser().parse(src)


def test_ref_becomes_ref_node():
    doc = parse(r"\ref{sec:intro}")
    assert doc.children == [Paragraph(children=[Ref(label="sec:intro", text="")])]


def test_autoref_becomes_ref_node():
    doc = parse(r"\autoref{fig:graph}")
    assert doc.children == [Paragraph(children=[Ref(label="fig:graph", text="")])]


def test_figure_becomes_figure_node():
    src = "\\begin{figure}\n\\includegraphics{img.png}\n\\end{figure}"
    doc = parse(src)
    assert doc.children == [Figure(src="img.png", caption="")]


def test_figure_with_caption():
    src = "\\begin{figure}\n\\includegraphics{img.png}\n\\caption{A graph}\n\\end{figure}"
    doc = parse(src)
    assert doc.children[0] == Figure(src="img.png", caption="A graph")


def test_noindent_is_discarded():
    doc = parse("\\noindent Some text.")
    assert doc.children == [Paragraph(children=[Text("Some text.")])]


def test_label_inline_is_discarded():
    doc = parse(r"Some text.\label{sec:foo}")
    assert doc.children == [Paragraph(children=[Text("Some text.")])]


def test_vspace_becomes_vertical_space_node():
    doc = parse(r"\vspace{1cm}")
    assert doc.children == [VerticalSpace(amount="1cm")]
