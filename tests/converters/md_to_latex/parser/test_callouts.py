from src.ir.nodes import (
    Definition,
    InlineMath,
    Note,
    Paragraph,
    Text,
    Theorem,
)

# [!tip] -> Definition


def test_tip_callout_produces_definition(parser):
    doc = parser.parse("> [!tip] Continuity\n> Body.")
    assert isinstance(doc.children[0], Definition)


def test_definition_title(parser):
    doc = parser.parse("> [!tip] Grafo regular bipartito\n> Body.")
    assert doc.children[0].title == "Grafo regular bipartito"


def test_definition_label_snake_case(parser):
    doc = parser.parse("> [!tip] Grafo regular bipartito\n> Body.")
    assert doc.children[0].label == "grafo_regular_bipartito"


def test_definition_label_strips_accents(parser):
    doc = parser.parse("> [!tip] Árbol\n> Body.")
    assert doc.children[0].label == "arbol"


def test_definition_body_no_blank_line(parser):
    doc = parser.parse("> [!tip] Continuity\n> A function $f$ is continuous.")
    node = doc.children[0]
    assert node.body == [
        Paragraph(
            children=[Text("A function "), InlineMath("f"), Text(" is continuous.")]
        )
    ]


def test_definition_body_with_blank_line(parser):
    doc = parser.parse("> [!tip] Continuity\n>\n> A function is continuous.")
    node = doc.children[0]
    assert node.body == [Paragraph(children=[Text("A function is continuous.")])]


# [!info] -> Theorem


def test_info_callout_produces_theorem(parser):
    doc = parser.parse("> [!info] Grafo\n> Body.")
    assert isinstance(doc.children[0], Theorem)


def test_theorem_title(parser):
    doc = parser.parse("> [!info] König's theorem\n> Body.")
    assert doc.children[0].title == "König's theorem"


def test_theorem_label(parser):
    doc = parser.parse("> [!info] Teorema de König\n> Body.")
    assert doc.children[0].label == "teorema_de_konig"


def test_theorem_body(parser):
    doc = parser.parse("> [!info] Some theorem\n> It holds that $x = 1$.")
    node = doc.children[0]
    assert node.body == [
        Paragraph(children=[Text("It holds that "), InlineMath("x = 1"), Text(".")])
    ]


# [!note] -> Note


def test_note_callout_produces_note(parser):
    doc = parser.parse("> [!note]\n> Some remark.")
    assert isinstance(doc.children[0], Note)


def test_note_body(parser):
    doc = parser.parse("> [!note]\n> Some remark.")
    node = doc.children[0]
    assert node.body == [Paragraph(children=[Text("Some remark.")])]


# Unknown -> Paragraph


def test_unknown_callout_falls_through_to_paragraph(parser):
    doc = parser.parse("> [!warning] Watch out\n> Body.")
    assert not any(isinstance(n, (Definition, Theorem, Note)) for n in doc.children)
