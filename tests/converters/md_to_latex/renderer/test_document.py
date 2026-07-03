from src.ir.nodes import Document, Heading, Paragraph, Text


def test_blocks_joined_by_blank_line(renderer):
    doc = Document(
        children=[
            Heading(level=2, title=[Text("Title")]),
            Paragraph(children=[Text("Body")]),
        ]
    )
    assert renderer.render(doc) == "\\section{Title}\n\nBody"


def test_empty_document(renderer):
    assert renderer.render(Document(children=[])) == ""
