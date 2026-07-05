from src.converters.latex_to_react.latex_to_react import convert_latex_code_to_react


def test_comment_becomes_jsx_comment():
    assert convert_latex_code_to_react("%comment\n") == "{/* comment */}"


def test_comment_with_space_preserves_space():
    assert convert_latex_code_to_react("% comment\n") == "{/*  comment */}"


def test_comment_in_text():
    src = "Some text.\n% A comment\nMore text."
    result = convert_latex_code_to_react(src)
    assert result == "Some text.\n{/*  A comment */}\nMore text."


def test_multiple_comments():
    src = "%first\n%second\n"
    result = convert_latex_code_to_react(src)
    assert result == "{/* first */}\n{/* second */}"


def test_inline_comment_at_end_of_line():
    # A trailing comment splits the surrounding text into separate blocks.
    src = "Some content. %trailing comment\nNext line."
    result = convert_latex_code_to_react(src)
    assert result == "Some content.\n{/* trailing comment */}\nNext line."
