from src.ir.nodes import Hyperlink, Paragraph, Text
from src.parsers.latex.latex import LatexParser


def parse(src):
    return LatexParser().parse(src)


def test_href_target_and_text():
    doc = parse(r"\href{https://example.com}{Example}")
    assert doc.children == [
        Paragraph(children=[Hyperlink(target="https://example.com", text="Example")])
    ]


def test_href_in_surrounding_text():
    doc = parse(r"See \href{https://example.com}{here} for details.")
    p = doc.children[0]
    assert p.children == [
        Text("See "),
        Hyperlink(target="https://example.com", text="here"),
        Text(" for details."),
    ]


def test_hyperlink_target_and_text():
    doc = parse(r"\hyperlink{sec:intro}{Introduction}")
    assert doc.children == [
        Paragraph(children=[Hyperlink(target="sec:intro", text="Introduction")])
    ]


def test_hyperlink_in_surrounding_text():
    doc = parse(r"See \hyperlink{sec:bg}{Background} for context.")
    p = doc.children[0]
    assert p.children == [
        Text("See "),
        Hyperlink(target="sec:bg", text="Background"),
        Text(" for context."),
    ]


def test_multiple_hyperlinks():
    doc = parse(r"\hyperlink{a}{First} and \hyperlink{b}{Second}.")
    p = doc.children[0]
    assert p.children == [
        Hyperlink(target="a", text="First"),
        Text(" and "),
        Hyperlink(target="b", text="Second"),
        Text("."),
    ]
