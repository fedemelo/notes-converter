from src.ir.nodes import Paragraph, Ref, Text


def test_wikilink_produces_ref(parser):
    doc = parser.parse("[[Grafos#Grafos ponderados|grafo ponderado]]")
    para = doc.children[0]
    assert isinstance(para.children[0], Ref)


def test_ref_label(parser):
    doc = parser.parse("[[Grafos#Grafos ponderados|grafo ponderado]]")
    ref = doc.children[0].children[0]
    assert ref.label == "sec:grafos_ponderados"


def test_ref_display_text(parser):
    doc = parser.parse("[[Grafos#Grafos ponderados|grafo ponderado]]")
    ref = doc.children[0].children[0]
    assert ref.text == "grafo ponderado"


def test_ref_label_strips_accents(parser):
    doc = parser.parse("[[File#Número de arcos|arcos]]")
    ref = doc.children[0].children[0]
    assert ref.label == "sec:numero_de_arcos"


def test_wikilink_with_backslash_hash(parser):
    doc = parser.parse(r"[[Teoría de Grafos\#Grafos ponderados|grafo ponderado]]")
    ref = doc.children[0].children[0]
    assert ref.label == "sec:grafos_ponderados"
    assert ref.text == "grafo ponderado"


def test_wikilink_inline_within_sentence(parser):
    doc = parser.parse("See [[X#Section|the section]] for details.")
    children = doc.children[0].children
    assert children[0] == Text("See ")
    assert isinstance(children[1], Ref)
    assert children[2] == Text(" for details.")


def test_ref_label_is_snake_case(parser):
    doc = parser.parse("[[X#Árbol de recubrimiento|árbol]]")
    ref = doc.children[0].children[0]
    assert ref.label == "sec:arbol_de_recubrimiento"


def test_wikilink_section_with_inline_math(parser):
    # $n$ inside the section name used to be split into a math_inline token by
    # dollarmath_plugin, preventing the wikilink regex from ever matching.
    doc = parser.parse(
        r"[[ Teoría de Grafos\#Conjunto de subconjuntos de cardinalidad $n$"
        r"|conjunto de subconjuntos de cardinalidad 2]]"
    )
    ref = doc.children[0].children[0]
    assert isinstance(ref, Ref)
    assert ref.label == "sec:conjunto_de_subconjuntos_de_cardinalidad_n"
    assert ref.text == "conjunto de subconjuntos de cardinalidad 2"
