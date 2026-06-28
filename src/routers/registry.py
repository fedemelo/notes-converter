from src.converters.latex_to_react.latex_to_react import convert_latex_code_to_react
from src.converters.md_to_latex import convert_md_to_latex
from src.routers.conversion import Conversion

CONVERSIONS: list[Conversion] = [
    Conversion(
        name="latex-to-react",
        source_format="LaTeX",
        target_format="React JSX",
        source_extension="tex",
        target_extension="txt",
        converter=convert_latex_code_to_react,
    ),
    Conversion(
        name="md-to-latex",
        source_format="Obsidian Markdown",
        target_format="LaTeX",
        source_extension="md",
        target_extension="tex",
        converter=convert_md_to_latex,
    ),
]
