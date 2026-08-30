from src.ir.nodes import CodeBlock, InlineCode, Paragraph, Text


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


def test_fenced_code_block(parser):
    doc = parser.parse("```\ndef f():\n    pass\n```")
    assert doc.children == [CodeBlock("def f():\n    pass")]
