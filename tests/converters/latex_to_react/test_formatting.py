from src.converters.latex_to_react.latex_to_react import convert_latex_code_to_react


# ── Bold ──────────────────────────────────────────────────────────────────────


def test_textbf_becomes_bold():
    assert convert_latex_code_to_react(r"\textbf{important}") == "<b>important</b>"


def test_textbf_preserves_surrounding_text():
    result = convert_latex_code_to_react(r"This is \textbf{bold} text.")
    assert result == "This is <b>bold</b> text."


# ── Italic ────────────────────────────────────────────────────────────────────


def test_textit_becomes_italic():
    assert convert_latex_code_to_react(r"\textit{slanted}") == "<i>slanted</i>"


def test_textit_preserves_surrounding_text():
    result = convert_latex_code_to_react(r"This is \textit{italic} text.")
    assert result == "This is <i>italic</i> text."


# ── Underline ─────────────────────────────────────────────────────────────────


def test_underline_becomes_u():
    assert convert_latex_code_to_react(r"\underline{underlined}") == "<u>underlined</u>"


# ── Emphasis ──────────────────────────────────────────────────────────────────


def test_emph_becomes_em():
    assert convert_latex_code_to_react(r"\emph{emphasis}") == "<em>emphasis</em>"


# ── Say (quotes) ──────────────────────────────────────────────────────────────


def test_say_becomes_double_quotes():
    assert convert_latex_code_to_react(r'\say{hello}') == '"hello"'


def test_say_preserves_surrounding_text():
    result = convert_latex_code_to_react(r'He said \say{hello} to her.')
    assert result == 'He said "hello" to her.'


# ── Combinations ──────────────────────────────────────────────────────────────


def test_multiple_formatting_commands():
    result = convert_latex_code_to_react(r"\textbf{bold} and \textit{italic}")
    assert result == "<b>bold</b> and <i>italic</i>"
