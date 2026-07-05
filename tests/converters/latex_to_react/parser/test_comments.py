from src.ir.nodes import Comment, Paragraph, Text
from src.parsers.latex.latex import LatexParser


def parse(src):
    return LatexParser().parse(src)


def test_comment_line():
    doc = parse("%comment\n")
    assert doc.children == [Comment(content="comment")]


def test_comment_preserves_text_after_percent():
    doc = parse("% A comment\n")
    assert doc.children == [Comment(content=" A comment")]


def test_comment_and_paragraph():
    doc = parse("% A comment\nSome text.")
    assert doc.children[0] == Comment(content=" A comment")
    assert doc.children[1] == Paragraph(children=[Text("Some text.")])


def test_multiple_comments():
    doc = parse("%first\n%second\n")
    assert doc.children == [Comment(content="first"), Comment(content="second")]


def test_inline_comment_at_end_of_line():
    doc = parse("Some content. %trailing comment\nNext line.")
    assert doc.children[0] == Paragraph(children=[Text("Some content.")])
    assert doc.children[1] == Comment(content="trailing comment")
    assert doc.children[2] == Paragraph(children=[Text("Next line.")])
