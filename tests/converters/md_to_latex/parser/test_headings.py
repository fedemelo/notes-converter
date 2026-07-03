from src.ir.nodes import Heading, InlineMath, Text


def test_h1(parser):
    doc = parser.parse("# Title")
    assert doc.children == [Heading(level=1, title=[Text("Title")], label="title")]


def test_h2(parser):
    doc = parser.parse("## Title")
    assert doc.children == [Heading(level=2, title=[Text("Title")], label="title")]


def test_h3(parser):
    doc = parser.parse("### Title")
    assert doc.children == [Heading(level=3, title=[Text("Title")], label="title")]


def test_unicode_title(parser):
    doc = parser.parse("# Árboles")
    assert doc.children == [Heading(level=1, title=[Text("Árboles")], label="arboles")]


def test_label_is_snake_case(parser):
    doc = parser.parse("## Grafos ponderados")
    assert doc.children[0].label == "grafos_ponderados"


def test_label_strips_accents(parser):
    doc = parser.parse("## Número de arcos")
    assert doc.children[0].label == "numero_de_arcos"


def test_inline_math_in_title(parser):
    doc = parser.parse("# Let $G$ be a graph")
    node = doc.children[0]
    assert node.title == [Text("Let "), InlineMath("G"), Text(" be a graph")]
    # Math content is skipped when deriving the label.
    assert node.label == "let_be_a_graph"
