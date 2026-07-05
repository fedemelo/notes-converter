from src.converters.latex_to_react.latex_to_react import convert_latex_code_to_react


# ── \ref ──────────────────────────────────────────────────────────────────────


def test_ref_is_removed():
    assert convert_latex_code_to_react(r"\ref{sec:intro}") == ""


def test_ref_in_text_is_removed():
    result = convert_latex_code_to_react(r"See \ref{sec:intro} for details.")
    assert result == "See  for details."


# ── \autoref ──────────────────────────────────────────────────────────────────


def test_autoref_is_removed():
    assert convert_latex_code_to_react(r"\autoref{sec:intro}") == ""


def test_autoref_in_text_is_removed():
    result = convert_latex_code_to_react(r"See \autoref{fig:graph}.")
    assert result == "See ."


# ── figure environment ────────────────────────────────────────────────────────


def test_figure_environment_is_removed():
    src = "\\begin{figure}\n\\includegraphics{img.png}\n\\end{figure}"
    assert convert_latex_code_to_react(src) == ""


def test_figure_in_text_is_removed():
    src = "Before.\n\\begin{figure}\n\\includegraphics{img.png}\n\\end{figure}\nAfter."
    result = convert_latex_code_to_react(src)
    assert result == "Before.\nAfter."


# ── \noindent ─────────────────────────────────────────────────────────────────


def test_noindent_is_removed():
    assert convert_latex_code_to_react(r"\noindent") == ""


def test_noindent_with_trailing_space_is_removed():
    assert convert_latex_code_to_react(r"\noindent text") == "text"


# ── \label ────────────────────────────────────────────────────────────────────


def test_label_is_removed():
    assert convert_latex_code_to_react(r"\label{sec:intro}") == ""


def test_label_in_text_is_removed():
    result = convert_latex_code_to_react(r"\section{Methods}\label{sec:methods}")
    assert result == "<h2>Methods</h2>"


# ── \vspace ───────────────────────────────────────────────────────────────────


def test_vspace_is_removed():
    assert convert_latex_code_to_react(r"\vspace{1cm}") == ""


def test_vspace_in_text_is_removed():
    result = convert_latex_code_to_react(r"Text above.\vspace{2em}Text below.")
    assert result == "Text above.\nText below."
