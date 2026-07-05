from src.ir.nodes import (
    Comment,
    Definition,
    DisplayMath,
    Example,
    Figure,
    Heading,
    ListItem,
    Notation,
    Note,
    OrderedList,
    Paragraph,
    Text,
    Theorem,
    UnorderedList,
    VerticalSpace,
    Warning,
)
from src.renderers.react import ReactRenderer


def render(node):
    return ReactRenderer()._render_block(node)


# ── Headings ──────────────────────────────────────────────────────────────────


def test_heading_h1():
    assert render(Heading(level=1, title=[Text("Intro")])) == "<h1>Intro</h1>"


def test_heading_h2():
    assert render(Heading(level=2, title=[Text("Background")])) == "<h2>Background</h2>"


def test_heading_h3():
    assert render(Heading(level=3, title=[Text("Details")])) == "<h3>Details</h3>"


def test_heading_h4():
    assert render(Heading(level=4, title=[Text("Deep")])) == "<h4>Deep</h4>"


def test_heading_h5():
    assert render(Heading(level=5, title=[Text("Minor")])) == "<h5>Minor</h5>"


# ── Paragraph ─────────────────────────────────────────────────────────────────


def test_paragraph():
    assert render(Paragraph(children=[Text("Hello")])) == "Hello"


# ── Display math ──────────────────────────────────────────────────────────────


def test_display_math():
    assert render(DisplayMath(content="E = mc^2")) == "<M block>\n    {r`E = mc^2`}\n</M>"


def test_display_math_with_newlines():
    assert render(DisplayMath(content="\nE = mc^2\n")) == "<M block>\n    {r`\nE = mc^2\n`}\n</M>"


# ── Lists ─────────────────────────────────────────────────────────────────────


def test_unordered_list():
    node = UnorderedList(items=[
        ListItem(children=[Text("first")]),
        ListItem(children=[Text("second")]),
    ])
    assert render(node) == "<ul>\n<li>first</li>\n<li>second</li>\n</ul>"


def test_ordered_list():
    node = OrderedList(items=[
        ListItem(children=[Text("first")]),
        ListItem(children=[Text("second")]),
    ])
    assert render(node) == "<ol>\n<li>first</li>\n<li>second</li>\n</ol>"


# ── Custom environments ───────────────────────────────────────────────────────


def test_note():
    node = Note(body=[Paragraph(children=[Text("A tip.")])])
    assert render(node) == "<Tip>\nA tip.\n</Tip>"


def test_warning():
    node = Warning(body=[Paragraph(children=[Text("Watch out.")])])
    assert render(node) == "<Warning>\nWatch out.\n</Warning>"


def test_notation():
    node = Notation(body=[Paragraph(children=[Text("We write G.")])])
    assert render(node) == "<Notation>\nWe write G.\n</Notation>"


def test_definition():
    node = Definition(title="Tree", label="tree", body=[Paragraph(children=[Text("A graph.")])])
    assert render(node) == '<Definition concept="Tree">\n    A graph.\n</Definition>'


def test_example():
    node = Example(title="Coloring", label="col", body=[Paragraph(children=[Text("Color it.")])])
    assert render(node) == '<Example title="Coloring">\n Color it.\n</Example>'


def test_theorem():
    node = Theorem(title="König", label="konig", body=[Paragraph(children=[Text("Bipartite.")])])
    assert render(node) == '<Theorem name="König">\n    Bipartite.\n</Theorem>'


# ── Comment ───────────────────────────────────────────────────────────────────


def test_comment():
    assert render(Comment(content=" A comment")) == "{/*  A comment */}"


def test_comment_no_space():
    assert render(Comment(content="TODO")) == "{/* TODO */}"


# ── Discarded nodes ───────────────────────────────────────────────────────────


def test_figure_renders_empty():
    assert render(Figure(src="img.png")) == ""


def test_vertical_space_renders_empty():
    assert render(VerticalSpace(amount="1cm")) == ""
