from src.ir.nodes import (
    Definition,
    Example,
    InlineMath,
    Note,
    Notation,
    Paragraph,
    Text,
    Theorem,
    Warning,
)
from src.parsers.latex.latex import LatexParser


def parse(src):
    return LatexParser().parse(src)


def test_tip_environment():
    doc = parse("\\begin{tip}\nUseful remark.\n\\end{tip}")
    assert doc.children == [Note(body=[Paragraph(children=[Text("Useful remark.")])])]


def test_advertencia_environment():
    doc = parse("\\begin{advertencia}\nWatch out.\n\\end{advertencia}")
    assert doc.children == [Warning(body=[Paragraph(children=[Text("Watch out.")])])]


def test_notacion_environment():
    doc = parse("\\begin{notacion}\nWe write $G$.\n\\end{notacion}")
    note = doc.children[0]
    assert isinstance(note, Notation)
    assert note.body[0].children == [Text("We write "), InlineMath(content="G"), Text(".")]


def test_definicion_environment():
    doc = parse("\\begin{definicion}{Tree}{tree}\nA connected acyclic graph.\n\\end{definicion}")
    d = doc.children[0]
    assert isinstance(d, Definition)
    assert d.title == "Tree"
    assert d.label == "tree"
    assert d.body == [Paragraph(children=[Text("A connected acyclic graph.")])]


def test_definicion_case_insensitive():
    doc = parse("\\begin{Definicion}{Tree}{tree}\nContent.\n\\end{Definicion}")
    assert isinstance(doc.children[0], Definition)
    assert doc.children[0].title == "Tree"


def test_ejemplo_environment():
    doc = parse("\\begin{ejemplo}{Graph coloring}{ex-col}\nColor each vertex.\n\\end{ejemplo}")
    e = doc.children[0]
    assert isinstance(e, Example)
    assert e.title == "Graph coloring"
    assert e.label == "ex-col"
    assert e.body == [Paragraph(children=[Text("Color each vertex.")])]


def test_ejemplo_case_insensitive():
    doc = parse("\\begin{Ejemplo}{Title}{label}\nContent.\n\\end{Ejemplo}")
    assert isinstance(doc.children[0], Example)


def test_teorema_environment():
    doc = parse("\\begin{teorema}{König}{konig}\nBipartite graphs.\n\\end{teorema}")
    t = doc.children[0]
    assert isinstance(t, Theorem)
    assert t.title == "König"
    assert t.label == "konig"
    assert t.body == [Paragraph(children=[Text("Bipartite graphs.")])]


def test_teorema_case_insensitive():
    doc = parse("\\begin{Teorema}{Title}{label}\nContent.\n\\end{Teorema}")
    assert isinstance(doc.children[0], Theorem)


def test_inline_math_inside_environment_body():
    doc = parse("\\begin{tip}\nLet \\(x\\) be a value.\n\\end{tip}")
    body_para = doc.children[0].body[0]
    assert InlineMath(content="x") in body_para.children
