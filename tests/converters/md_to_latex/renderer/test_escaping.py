from src.ir.nodes import Text


def test_plain_text(renderer):
    assert renderer._render_inline(Text("hello")) == "hello"


def test_unicode_passthrough(renderer):
    assert renderer._render_inline(Text("árbol")) == "árbol"


def test_percent(renderer):
    assert renderer._render_inline(Text("50%")) == r"50\%"


def test_ampersand(renderer):
    assert renderer._render_inline(Text("a & b")) == r"a \& b"


def test_dollar(renderer):
    assert renderer._render_inline(Text("$10")) == r"\$10"


def test_hash(renderer):
    assert renderer._render_inline(Text("#1")) == r"\#1"


def test_underscore(renderer):
    assert renderer._render_inline(Text("snake_case")) == r"snake\_case"


def test_braces(renderer):
    assert renderer._render_inline(Text("{x}")) == r"\{x\}"


def test_backslash(renderer):
    assert renderer._render_inline(Text("a\\b")) == r"a\textbackslash{}b"


def test_caret(renderer):
    assert renderer._render_inline(Text("x^2")) == r"x\^{}2"


def test_tilde(renderer):
    assert renderer._render_inline(Text("~a")) == r"\textasciitilde{}a"
