from src.ir.nodes import Heading, Text
from src.parsers.latex.latex import LatexParser


def parse(src):
    return LatexParser().parse(src)


def test_part():
    doc = parse(r"\part{Introduction}")
    assert doc.children == [Heading(level=1, title=[Text("Introduction")], label="")]


def test_section():
    doc = parse(r"\section{Background}")
    assert doc.children == [Heading(level=2, title=[Text("Background")], label="")]


def test_subsection():
    doc = parse(r"\subsection{Details}")
    assert doc.children == [Heading(level=3, title=[Text("Details")], label="")]


def test_subsubsection():
    doc = parse(r"\subsubsection{Deep topic}")
    assert doc.children == [Heading(level=4, title=[Text("Deep topic")], label="")]


def test_paragraph_command():
    doc = parse(r"\paragraph{Minor note}")
    assert doc.children == [Heading(level=5, title=[Text("Minor note")], label="")]


def test_heading_with_label():
    doc = parse("\\section{Methods}\\label{sec:methods}")
    h = doc.children[0]
    assert h.level == 2
    assert h.title == [Text("Methods")]
    assert h.label == "sec:methods"


def test_heading_with_special_chars():
    doc = parse(r"\section{Álgebra lineal}")
    assert doc.children[0].title == [Text("Álgebra lineal")]


def test_multiple_headings():
    doc = parse("\\section{First}\n\\subsection{Second}")
    assert doc.children[0] == Heading(level=2, title=[Text("First")], label="")
    assert doc.children[1] == Heading(level=3, title=[Text("Second")], label="")
