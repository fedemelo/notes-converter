import pytest

from src.converters.latex_to_react.latex_to_react import convert_latex_code_to_react


def block(content: str) -> str:
    return f"<M block>\n    {{r`{content}`}}\n</M>"


def inline(content: str) -> str:
    return f"<M>{{r`{content}`}}</M>"


# ── Inline math ($...$) ───────────────────────────────────────────────────────


def test_inline_math_dollar():
    assert convert_latex_code_to_react("$x$") == inline("x")


def test_inline_math_dollar_with_expression():
    assert convert_latex_code_to_react("$x^2 + y^2$") == inline("x^2 + y^2")


def test_inline_math_dollar_preserves_surrounding_text():
    assert convert_latex_code_to_react("Sea $n$ el orden.") == f"Sea {inline('n')} el orden."


def test_multiple_inline_math_dollar():
    result = convert_latex_code_to_react("$a$ and $b$")
    assert result == f"{inline('a')} and {inline('b')}"


# ── Block math ($$...$$) ──────────────────────────────────────────────────────


def test_block_math_dollar_dollar():
    assert convert_latex_code_to_react("$$E = mc^2$$") == block("E = mc^2")


def test_block_math_dollar_dollar_preserves_surrounding_text():
    # $$...$$ is block-level; surrounding text becomes separate paragraphs.
    src = "Sea $$E = mc^2$$ la ecuación."
    assert convert_latex_code_to_react(src) == f"Sea\n{block('E = mc^2')}\nla ecuación."


def test_block_math_dollar_dollar_not_split_into_two_inline():
    # $$x$$ must be matched as one block, not as two inline $x$ pairs.
    assert convert_latex_code_to_react("$$x$$") == block("x")


# ── Inline math (\(...\)) ─────────────────────────────────────────────────────


def test_inline_math_paren():
    assert convert_latex_code_to_react(r"\(x\)") == inline("x")


def test_inline_math_paren_with_expression():
    assert convert_latex_code_to_react(r"\(a + b\)") == inline("a + b")


def test_inline_math_paren_preserves_surrounding_text():
    result = convert_latex_code_to_react(r"Sea \(G\) un grafo.")
    assert result == f"Sea {inline('G')} un grafo."


# ── Block math (\[...\]) ──────────────────────────────────────────────────────


def test_block_math_bracket():
    assert convert_latex_code_to_react(r"\[E = mc^2\]") == block("E = mc^2")


def test_block_math_bracket_preserves_surrounding_text():
    # \[...\] is block-level; surrounding text becomes separate paragraphs.
    result = convert_latex_code_to_react(r"Formula: \[a = b\] fin.")
    assert result == f"Formula:\n{block('a = b')}\nfin."


def test_block_math_bracket_multiline():
    src = "\\[\nE = mc^2\n\\]"
    assert convert_latex_code_to_react(src) == block("\nE = mc^2\n")


# ── equation* environment ─────────────────────────────────────────────────────


def test_equation_star_environment():
    src = r"\begin{equation*}E = mc^2\end{equation*}"
    assert convert_latex_code_to_react(src) == block("E = mc^2")


def test_equation_star_environment_multiline():
    src = "\\begin{equation*}\nE = mc^2\n\\end{equation*}"
    assert convert_latex_code_to_react(src) == block("\nE = mc^2\n")


# ── gather* environment ───────────────────────────────────────────────────────


def test_gather_star_environment():
    body = "\nX = 1 \\\\\nY = 2\n"
    src = f"\\begin{{gather*}}{body}\\end{{gather*}}"
    expected_content = f"\\begin{{gather*}}{body}\\end{{gather*}}"
    assert convert_latex_code_to_react(src) == block(expected_content)


# ── align* environment ────────────────────────────────────────────────────────


def test_align_star_environment():
    body = "\na &= b \\\\\nc &= d\n"
    src = f"\\begin{{align*}}{body}\\end{{align*}}"
    expected_content = f"\\begin{{align*}}{body}\\end{{align*}}"
    assert convert_latex_code_to_react(src) == block(expected_content)
