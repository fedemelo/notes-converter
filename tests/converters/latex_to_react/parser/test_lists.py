import pytest

from src.exceptions import MalformedLatexError
from src.ir.nodes import ListItem, OrderedList, Text, UnorderedList
from src.parsers.latex.latex import LatexParser


def parse(src):
    return LatexParser().parse(src)


def test_itemize_single_item():
    doc = parse("\\begin{itemize}\n\\item first\n\\end{itemize}")
    assert doc.children == [
        UnorderedList(items=[ListItem(children=[Text("first")])])
    ]


def test_itemize_multiple_items():
    doc = parse("\\begin{itemize}\n\\item first\n\\item second\n\\end{itemize}")
    assert doc.children == [
        UnorderedList(items=[
            ListItem(children=[Text("first")]),
            ListItem(children=[Text("second")]),
        ])
    ]


def test_enumerate_single_item():
    doc = parse("\\begin{enumerate}\n\\item only\n\\end{enumerate}")
    assert doc.children == [
        OrderedList(items=[ListItem(children=[Text("only")])])
    ]


def test_enumerate_multiple_items():
    doc = parse("\\begin{enumerate}\n\\item first\n\\item second\n\\end{enumerate}")
    assert doc.children == [
        OrderedList(items=[
            ListItem(children=[Text("first")]),
            ListItem(children=[Text("second")]),
        ])
    ]


def test_list_in_surrounding_text():
    doc = parse("Intro.\n\n\\begin{itemize}\n\\item item\n\\end{itemize}")
    assert len(doc.children) == 2
    assert isinstance(doc.children[1], UnorderedList)


# ── Structural errors ─────────────────────────────────────────────────────────


def test_item_outside_list_raises():
    with pytest.raises(MalformedLatexError, match=r"\\item at line 1"):
        parse("\\item first")


def test_item_outside_list_reports_correct_line():
    with pytest.raises(MalformedLatexError, match=r"\\item at line 5"):
        parse("First paragraph.\n\nSecond paragraph.\n\n\\item orphan")
