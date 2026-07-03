from src.ir.nodes import Image, Paragraph, Text


def test_image(parser):
    doc = parser.parse("![A diagram](figures/diagram.png)")
    assert doc.children == [
        Paragraph(children=[Image(src="figures/diagram.png", alt="A diagram")])
    ]


def test_image_empty_alt(parser):
    doc = parser.parse("![](figures/fig.png)")
    assert doc.children == [Paragraph(children=[Image(src="figures/fig.png", alt="")])]


def test_obsidian_embed(parser):
    doc = parser.parse("![[graph.png]]")
    assert doc.children == [Paragraph(children=[Image(src="graph.png", alt="")])]


def test_obsidian_embed_subdirectory(parser):
    doc = parser.parse("![[figures/graph.png]]")
    assert doc.children == [
        Paragraph(children=[Image(src="figures/graph.png", alt="")])
    ]


def test_obsidian_embed_inline_with_text(parser):
    doc = parser.parse("See ![[fig.png]] for details.")
    assert doc.children == [
        Paragraph(
            children=[
                Text(content="See "),
                Image(src="fig.png", alt=""),
                Text(content=" for details."),
            ]
        )
    ]
