import pytest

from src.converters.latex_to_react.latex_to_react import convert_latex_code_to_react
from src.exceptions import MalformedLatexError


# ── Individual items ──────────────────────────────────────────────────────────


def test_item_outside_list_raises_error():
    with pytest.raises(MalformedLatexError, match=r"\\item"):
        convert_latex_code_to_react("\\item first\n")


def test_multiple_items_outside_list_raises_error():
    with pytest.raises(MalformedLatexError, match=r"\\item"):
        convert_latex_code_to_react("\\item first\n\\item second\n")


# ── itemize environment ───────────────────────────────────────────────────────


def test_itemize_becomes_ul():
    src = "\\begin{itemize}\n\\item first\n\\item second\n\\end{itemize}"
    result = convert_latex_code_to_react(src)
    assert result == "<ul>\n<li>first</li>\n<li>second</li>\n</ul>"


def test_itemize_single_item():
    src = "\\begin{itemize}\n\\item only\n\\end{itemize}"
    result = convert_latex_code_to_react(src)
    assert result == "<ul>\n<li>only</li>\n</ul>"


# ── enumerate environment ─────────────────────────────────────────────────────


def test_enumerate_becomes_ol():
    src = "\\begin{enumerate}\n\\item first\n\\item second\n\\end{enumerate}"
    result = convert_latex_code_to_react(src)
    assert result == "<ol>\n<li>first</li>\n<li>second</li>\n</ol>"


def test_enumerate_single_item():
    src = "\\begin{enumerate}\n\\item only\n\\end{enumerate}"
    result = convert_latex_code_to_react(src)
    assert result == "<ol>\n<li>only</li>\n</ol>"


# ── List inside text ──────────────────────────────────────────────────────────


def test_list_preserves_surrounding_text():
    src = "Intro.\n\\begin{itemize}\n\\item item\n\\end{itemize}\nOutro."
    result = convert_latex_code_to_react(src)
    assert result == "Intro.\n<ul>\n<li>item</li>\n</ul>\nOutro."
