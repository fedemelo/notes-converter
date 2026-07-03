from src.ir.nodes import (
    Comment,
    Definition,
    DisplayMath,
    Heading,
    InlineMath,
    Note,
    Paragraph,
    Text,
    Theorem,
)

# ── Headings ──────────────────────────────────────────────────────────────────


def test_heading_part(renderer):
    node = Heading(level=1, title=[Text("Title")], label="title")
    assert renderer._render_block(node) == "\\part{Title}\n\\label{sec:title}"


def test_heading_section(renderer):
    node = Heading(level=2, title=[Text("Background")], label="background")
    assert (
        renderer._render_block(node) == "\\section{Background}\n\\label{sec:background}"
    )


def test_heading_subsection(renderer):
    node = Heading(level=3, title=[Text("Details")], label="details")
    assert renderer._render_block(node) == "\\subsection{Details}\n\\label{sec:details}"


def test_heading_subsubsection_level4(renderer):
    node = Heading(level=4, title=[Text("Deep")], label="deep")
    assert renderer._render_block(node) == "\\subsubsection{Deep}\n\\label{sec:deep}"


def test_heading_subsubsection_level5(renderer):
    node = Heading(level=5, title=[Text("Deeper")], label="deeper")
    assert (
        renderer._render_block(node) == "\\subsubsection{Deeper}\n\\label{sec:deeper}"
    )


def test_heading_no_label_omits_label_command(renderer):
    node = Heading(level=2, title=[Text("Title")])  # label=""
    assert renderer._render_block(node) == r"\section{Title}"


def test_heading_with_math_in_title(renderer):
    node = Heading(
        level=2,
        title=[Text("Let "), InlineMath("G"), Text(" be a graph")],
        label="let_g_be_a_graph",
    )
    assert (
        renderer._render_block(node)
        == "\\section{Let \\(G\\) be a graph}\n\\label{sec:let_g_be_a_graph}"
    )


# ── Paragraph ─────────────────────────────────────────────────────────────────


def test_paragraph(renderer):
    assert renderer._render_block(Paragraph(children=[Text("Hello")])) == "Hello"


def test_paragraph_with_inline_math(renderer):
    node = Paragraph(children=[Text("Sea "), InlineMath("T"), Text(" un árbol.")])
    assert renderer._render_block(node) == r"Sea \(T\) un árbol."


# ── Display math ──────────────────────────────────────────────────────────────


def test_display_math(renderer):
    assert (
        renderer._render_block(DisplayMath(content="E = mc^2")) == "\\[\nE = mc^2\n\\]"
    )


_GATHER_BODY = "X = 1 \\\\\nY = 2"
_GATHER_CONTENT = f"\\begin{{gather*}}\n{_GATHER_BODY}\n\\end{{gather*}}"


def test_display_math_gather_no_brackets(renderer):
    assert renderer._render_block(DisplayMath(content=_GATHER_CONTENT)) == _GATHER_CONTENT


def test_display_math_equation_no_brackets(renderer):
    content = "\\begin{equation}\nE = mc^2\n\\end{equation}"
    assert renderer._render_block(DisplayMath(content=content)) == content


def test_display_math_align_no_brackets(renderer):
    content = "\\begin{align*}\na &= b \\\\\nc &= d\n\\end{align*}"
    assert renderer._render_block(DisplayMath(content=content)) == content


def test_display_math_multline_no_brackets(renderer):
    content = "\\begin{multline}\na + b \\\\\n+ c\n\\end{multline}"
    assert renderer._render_block(DisplayMath(content=content)) == content


def test_display_math_plain_still_wrapped(renderer):
    assert renderer._render_block(DisplayMath(content="a + b = c")) == "\\[\na + b = c\n\\]"


# ── Definition ────────────────────────────────────────────────────────────────


def test_definition_empty_body(renderer):
    node = Definition(title="Tree", label="tree", body=[])
    result = renderer._render_block(node)
    assert result == "\\begin{definicion}{Tree}{tree}\n\n\\end{definicion}"


def test_definition_body_indented(renderer):
    node = Definition(
        title="Tree",
        label="tree",
        body=[Paragraph(children=[Text("A connected acyclic graph.")])],
    )
    result = renderer._render_block(node)
    assert "  A connected acyclic graph." in result


def test_definition_title_not_escaped(renderer):
    # Title goes directly into a LaTeX argument — caller is responsible for valid LaTeX.
    node = Definition(title="Graph $G$", label="graph_g", body=[])
    assert "{Graph $G$}" in renderer._render_block(node)


# ── Theorem ───────────────────────────────────────────────────────────────────


def test_theorem_empty_body(renderer):
    node = Theorem(title="König", label="konig", body=[])
    result = renderer._render_block(node)
    assert result == "\\begin{teorema}{König}{konig}\n\n\\end{teorema}"


def test_theorem_body_indented(renderer):
    node = Theorem(
        title="König",
        label="konig",
        body=[Paragraph(children=[Text("Bipartite graphs have equal parts.")])],
    )
    result = renderer._render_block(node)
    assert "  Bipartite graphs have equal parts." in result


# ── Comment ───────────────────────────────────────────────────────────────────


def test_comment_renders_as_latex_percent(renderer):
    assert renderer._render_block(Comment("TODO fix this")) == "%TODO fix this"


def test_comment_no_extra_space(renderer):
    assert renderer._render_block(Comment("FIXME")) == "%FIXME"


# ── Note ──────────────────────────────────────────────────────────────────────


def test_note_structure(renderer):
    node = Note(body=[])
    assert renderer._render_block(node) == "\\begin{tip}\n\n\\end{tip}"


def test_note_body_indented(renderer):
    node = Note(body=[Paragraph(children=[Text("A useful remark.")])])
    result = renderer._render_block(node)
    assert "  A useful remark." in result
