from src.ir.nodes import Emphasis, Paragraph, Strong, Text


def test_bold(parser):
    doc = parser.parse("**bold**")
    assert doc.children == [Paragraph(children=[Strong(children=[Text("bold")])])]


def test_italic(parser):
    doc = parser.parse("*italic*")
    assert doc.children == [Paragraph(children=[Emphasis(children=[Text("italic")])])]


def test_bold_within_sentence(parser):
    doc = parser.parse("An **árbol** is a tree.")
    assert doc.children == [
        Paragraph(
            children=[
                Text("An "),
                Strong(children=[Text("árbol")]),
                Text(" is a tree."),
            ]
        )
    ]


def test_italic_within_sentence(parser):
    doc = parser.parse("A *connected* graph.")
    assert doc.children == [
        Paragraph(
            children=[
                Text("A "),
                Emphasis(children=[Text("connected")]),
                Text(" graph."),
            ]
        )
    ]
