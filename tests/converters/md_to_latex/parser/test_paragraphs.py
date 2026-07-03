from src.ir.nodes import Paragraph, Text


def test_plain_paragraph(parser):
    doc = parser.parse("Hello world")
    assert doc.children == [Paragraph(children=[Text("Hello world")])]


def test_unicode_paragraph(parser):
    doc = parser.parse("Un árbol es un grafo simple.")
    assert doc.children == [Paragraph(children=[Text("Un árbol es un grafo simple.")])]


def test_multiple_paragraphs(parser):
    doc = parser.parse("First\n\nSecond")
    assert doc.children == [
        Paragraph(children=[Text("First")]),
        Paragraph(children=[Text("Second")]),
    ]
