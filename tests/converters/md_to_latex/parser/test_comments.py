from src.ir.nodes import Comment, Paragraph, Text


def test_todo_comment(parser):
    doc = parser.parse("#TODO Leohnard Euler!")
    assert doc.children == [Comment(content="TODO Leohnard Euler!")]


def test_comment_without_body(parser):
    doc = parser.parse("#TODO")
    assert doc.children == [Comment(content="TODO")]


def test_comment_other_tag(parser):
    doc = parser.parse("#FIXME revisit this proof")
    assert doc.children == [Comment(content="FIXME revisit this proof")]


def test_lowercase_hash_tag_is_not_comment(parser):
    # #todo (lowercase) is a normal Obsidian tag, not our convention.
    doc = parser.parse("#todo something")
    assert not any(isinstance(c, Comment) for c in doc.children)


def test_comment_does_not_consume_surrounding_paragraphs(parser):
    src = "First paragraph.\n\n#TODO fix this\n\nLast paragraph."
    doc = parser.parse(src)
    assert isinstance(doc.children[0], Paragraph)
    assert doc.children[1] == Comment(content="TODO fix this")
    assert isinstance(doc.children[2], Paragraph)
