from src.ir.nodes import InlineCode, Paragraph, Text


def test_inline_code(parser):
    doc = parser.parse("Use `M` here")
    assert doc.children == [
        Paragraph(children=[Text("Use "), InlineCode("M"), Text(" here")])
    ]


def test_inline_code_preserves_special_characters(parser):
    doc = parser.parse("Call `M[i][j] = 1`")
    assert doc.children == [
        Paragraph(children=[Text("Call "), InlineCode("M[i][j] = 1")])
    ]
