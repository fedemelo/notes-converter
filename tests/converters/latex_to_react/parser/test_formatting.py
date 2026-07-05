from src.ir.nodes import Emphasis, Italic, Paragraph, Quote, Strong, Text, Underline
from src.parsers.latex.latex import LatexParser


def parse(src):
    return LatexParser().parse(src)


def para(src):
    return parse(src).children[0]


def test_textbf():
    assert para(r"\textbf{bold}").children == [Strong(children=[Text("bold")])]


def test_textit():
    assert para(r"\textit{italic}").children == [Italic(children=[Text("italic")])]


def test_emph():
    assert para(r"\emph{emphasis}").children == [Emphasis(children=[Text("emphasis")])]


def test_underline():
    assert para(r"\underline{underlined}").children == [Underline(children=[Text("underlined")])]


def test_say():
    assert para(r"\say{hello}").children == [Quote(children=[Text("hello")])]


def test_formatting_preserves_surrounding_text():
    p = para(r"This is \textbf{bold} text.")
    assert p.children == [Text("This is "), Strong(children=[Text("bold")]), Text(" text.")]


def test_multiple_formatting_in_one_paragraph():
    p = para(r"\textbf{bold} and \textit{italic}")
    assert p.children == [
        Strong(children=[Text("bold")]),
        Text(" and "),
        Italic(children=[Text("italic")]),
    ]
