from src.converters.latex_to_react.latex_to_react import convert_latex_code_to_react


def test_part_becomes_h1():
    assert convert_latex_code_to_react(r"\part{Introduction}") == "<h1>Introduction</h1>"


def test_section_becomes_h2():
    assert convert_latex_code_to_react(r"\section{Background}") == "<h2>Background</h2>"


def test_subsection_becomes_h3():
    assert convert_latex_code_to_react(r"\subsection{Details}") == "<h3>Details</h3>"


def test_subsubsection_becomes_h4():
    assert (
        convert_latex_code_to_react(r"\subsubsection{Deep topic}")
        == "<h4>Deep topic</h4>"
    )


def test_paragraph_becomes_h5():
    assert (
        convert_latex_code_to_react(r"\paragraph{Minor note}") == "<h5>Minor note</h5>"
    )


def test_heading_preserves_surrounding_text():
    src = "Intro text.\n\\section{Methods}\nBody text."
    result = convert_latex_code_to_react(src)
    assert result == "Intro text.\n<h2>Methods</h2>\nBody text."


def test_multiple_headings():
    src = "\\section{First}\n\\subsection{Second}"
    result = convert_latex_code_to_react(src)
    assert result == "<h2>First</h2>\n<h3>Second</h3>"


def test_heading_with_special_chars_in_title():
    result = convert_latex_code_to_react(r"\section{Álgebra lineal}")
    assert result == "<h2>Álgebra lineal</h2>"
