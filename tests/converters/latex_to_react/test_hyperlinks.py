from src.converters.latex_to_react.latex_to_react import convert_latex_code_to_react


def test_hyperlink_keeps_only_visible_text():
    result = convert_latex_code_to_react(r"\hyperlink{sec:intro}{Introduction}")
    assert result == "Introduction"


def test_hyperlink_in_surrounding_text():
    result = convert_latex_code_to_react(r"See \hyperlink{sec:bg}{Background} for context.")
    assert result == "See Background for context."


def test_multiple_hyperlinks():
    src = r"\hyperlink{a}{First} and \hyperlink{b}{Second}."
    result = convert_latex_code_to_react(src)
    assert result == "First and Second."
