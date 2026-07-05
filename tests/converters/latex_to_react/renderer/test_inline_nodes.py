import pytest

from src.ir.nodes import (
    Emphasis,
    Hyperlink,
    Image,
    InlineMath,
    Italic,
    Quote,
    Ref,
    Strong,
    Text,
    Underline,
)
from src.renderers.react import ReactRenderer


def render(node):
    return ReactRenderer()._render_inline(node)


def test_text():
    assert render(Text(content="Hello")) == "Hello"


def test_inline_math():
    assert render(InlineMath(content="x")) == "<M>{r`x`}</M>"


def test_inline_math_expression():
    assert render(InlineMath(content="x^2 + y^2")) == "<M>{r`x^2 + y^2`}</M>"


def test_inline_math_display():
    assert render(InlineMath(content="E = mc^2", display=True)) == "<M block>\n    {r`E = mc^2`}\n</M>"


def test_strong():
    assert render(Strong(children=[Text("bold")])) == "<b>bold</b>"


def test_italic():
    assert render(Italic(children=[Text("slanted")])) == "<i>slanted</i>"


def test_emphasis():
    assert render(Emphasis(children=[Text("italic")])) == "<em>italic</em>"


def test_underline():
    assert render(Underline(children=[Text("underlined")])) == "<u>underlined</u>"


def test_quote():
    assert render(Quote(children=[Text("hello")])) == '"hello"'


def test_hyperlink_shows_text_only():
    assert render(Hyperlink(target="sec:intro", text="Introduction")) == "Introduction"


def test_ref_renders_empty():
    assert render(Ref(label="sec:foo", text="")) == ""


def test_nested_strong_in_emphasis():
    node = Emphasis(children=[Strong(children=[Text("bold italic")])])
    assert render(node) == "<em><b>bold italic</b></em>"


def test_image_raises_not_implemented():
    with pytest.raises(NotImplementedError, match="Image"):
        render(Image(src="fig.png", alt="a graph"))
