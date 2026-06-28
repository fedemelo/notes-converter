from src.converters.latex_dollar_to_paren import convert_latex_dollar_to_paren


def test_inline_math():
    assert convert_latex_dollar_to_paren("$x = 1$") == r"\(x = 1\)"


def test_display_math():
    assert convert_latex_dollar_to_paren("$$E = mc^2$$") == r"\[E = mc^2\]"


def test_display_math_multiline():
    src = "$$\nE = mc^2\n$$"
    assert convert_latex_dollar_to_paren(src) == "\\[\nE = mc^2\n\\]"


def test_display_processed_before_inline():
    # $$...$$ must not be consumed as two $...$ pairs.
    assert convert_latex_dollar_to_paren("$$a + b$$") == r"\[a + b\]"


def test_escaped_dollar_not_matched():
    assert convert_latex_dollar_to_paren(r"costs \$5") == r"costs \$5"


def test_surrounding_text_preserved():
    src = "Sea $n$ el orden del grafo."
    assert convert_latex_dollar_to_paren(src) == r"Sea \(n\) el orden del grafo."


def test_mixed_inline_and_display():
    src = "Sea $n$ el orden. $$n = |V|$$ Fin."
    assert convert_latex_dollar_to_paren(src) == r"Sea \(n\) el orden. \[n = |V|\] Fin."


def test_multiple_inline():
    src = "$a$ and $b$"
    assert convert_latex_dollar_to_paren(src) == r"\(a\) and \(b\)"


def test_content_with_pipes():
    # Vertical bars inside math should pass through unchanged.
    assert convert_latex_dollar_to_paren("$|G|$") == r"\(|G|\)"
    assert convert_latex_dollar_to_paren("$$|G| = |V|.$$") == r"\[|G| = |V|.\]"
