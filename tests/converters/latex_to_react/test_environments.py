from src.converters.latex_to_react.latex_to_react import convert_latex_code_to_react


def inline(content: str) -> str:
    return f"<M>{{r`{content}`}}</M>"


# ── tip ───────────────────────────────────────────────────────────────────────


def test_tip_environment():
    src = "\\begin{tip}\nUseful remark.\n\\end{tip}"
    result = convert_latex_code_to_react(src)
    assert result == "<Tip>\nUseful remark.\n</Tip>"


# ── advertencia (warning) ─────────────────────────────────────────────────────


def test_advertencia_environment():
    src = "\\begin{advertencia}\nWatch out.\n\\end{advertencia}"
    result = convert_latex_code_to_react(src)
    assert result == "<Warning>\nWatch out.\n</Warning>"


# ── notacion (notation) ───────────────────────────────────────────────────────


def test_notacion_environment():
    src = "\\begin{notacion}\nWe write $G = (V, E)$.\n\\end{notacion}"
    result = convert_latex_code_to_react(src)
    assert result == f"<Notation>\nWe write {inline('G = (V, E)')}.\n</Notation>"


# ── definicion ────────────────────────────────────────────────────────────────


def test_definicion_environment():
    src = "\\begin{definicion}{Tree}{tree}\nA connected acyclic graph.\n\\end{definicion}"
    result = convert_latex_code_to_react(src)
    assert result == '<Definition concept="Tree">\n    A connected acyclic graph.\n</Definition>'


def test_definicion_strips_body_whitespace():
    src = "\\begin{definicion}{Graph}{graph}\n\n  A set of vertices.\n\n\\end{definicion}"
    result = convert_latex_code_to_react(src)
    assert result == '<Definition concept="Graph">\n    A set of vertices.\n</Definition>'


def test_definicion_label_is_not_in_output():
    # The second argument (label) is silently dropped from the output.
    src = "\\begin{definicion}{Tree}{some-label}\nContent.\n\\end{definicion}"
    result = convert_latex_code_to_react(src)
    assert "some-label" not in result
    assert 'concept="Tree"' in result


def test_definicion_case_insensitive():
    src = "\\begin{Definicion}{Tree}{tree}\nContent.\n\\end{Definicion}"
    result = convert_latex_code_to_react(src)
    assert 'concept="Tree"' in result


# ── ejemplo (example) ─────────────────────────────────────────────────────────


def test_ejemplo_environment_with_title():
    src = "\\begin{ejemplo}{Graph coloring}{ex-coloring}\nColor each vertex.\n\\end{ejemplo}"
    result = convert_latex_code_to_react(src)
    assert result == '<Example title="Graph coloring">\n Color each vertex.\n</Example>'


def test_ejemplo_strips_body_whitespace():
    src = "\\begin{ejemplo}{Title}{label}\n\n  Content.\n\n\\end{ejemplo}"
    result = convert_latex_code_to_react(src)
    assert result == '<Example title="Title">\n Content.\n</Example>'


def test_ejemplo_label_is_not_in_output():
    src = "\\begin{ejemplo}{My Example}{ex-label}\nContent.\n\\end{ejemplo}"
    result = convert_latex_code_to_react(src)
    assert "ex-label" not in result
    assert 'title="My Example"' in result


def test_ejemplo_case_insensitive():
    src = "\\begin{Ejemplo}{Title}{label}\nContent.\n\\end{Ejemplo}"
    result = convert_latex_code_to_react(src)
    assert 'title="Title"' in result


def test_ejemplo_inline_math_rendered_as_component():
    src = "\\begin{ejemplo}{Title}{label}\nLet \\(x\\) be a value.\n\\end{ejemplo}"
    result = convert_latex_code_to_react(src)
    assert inline("x") in result


# ── teorema (theorem) ─────────────────────────────────────────────────────────


def test_teorema_environment_with_name():
    src = "\\begin{teorema}{König's theorem}{konig}\nBipartite graphs have equal parts.\n\\end{teorema}"
    result = convert_latex_code_to_react(src)
    assert result == '<Theorem name="König\'s theorem">\n    Bipartite graphs have equal parts.\n</Theorem>'


def test_teorema_strips_body_whitespace():
    src = "\\begin{teorema}{Title}{label}\n\n  Content.\n\n\\end{teorema}"
    result = convert_latex_code_to_react(src)
    assert result == '<Theorem name="Title">\n    Content.\n</Theorem>'


def test_teorema_label_is_not_in_output():
    src = "\\begin{teorema}{Pythagorean}{pythag}\nContent.\n\\end{teorema}"
    result = convert_latex_code_to_react(src)
    assert "pythag" not in result
    assert 'name="Pythagorean"' in result


def test_teorema_case_insensitive():
    src = "\\begin{Teorema}{Title}{label}\nContent.\n\\end{Teorema}"
    result = convert_latex_code_to_react(src)
    assert 'name="Title"' in result


def test_teorema_inline_math_rendered_as_component():
    src = "\\begin{teorema}{Title}{label}\nFor all \\(n > 0\\).\n\\end{teorema}"
    result = convert_latex_code_to_react(src)
    assert inline("n > 0") in result


# ── case-insensitivity ────────────────────────────────────────────────────────


def test_tip_environment_case_insensitive():
    src = "\\begin{Tip}\nUseful remark.\n\\end{Tip}"
    result = convert_latex_code_to_react(src)
    assert result == "<Tip>\nUseful remark.\n</Tip>"


def test_advertencia_environment_case_insensitive():
    src = "\\begin{Advertencia}\nWatch out.\n\\end{Advertencia}"
    result = convert_latex_code_to_react(src)
    assert result == "<Warning>\nWatch out.\n</Warning>"
