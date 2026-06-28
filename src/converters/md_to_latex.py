from src.parsers.markdown.obsidian import ObsidianMarkdownParser
from src.renderers.latex import LatexRenderer

_parser = ObsidianMarkdownParser()
_renderer = LatexRenderer()


def convert_md_to_latex(text: str) -> str:
    return _renderer.render(_parser.parse(text))
