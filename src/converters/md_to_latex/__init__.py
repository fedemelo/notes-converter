from .parsers.obsidian import ObsidianMarkdownParser
from .renderers.latex import LatexRenderer


def convert_md_to_latex(source: str) -> str:
    doc = ObsidianMarkdownParser().parse(source)
    return LatexRenderer().render(doc)
