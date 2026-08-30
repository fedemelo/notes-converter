from src.converters.md_to_latex import (
    CodeBlockEnvironment,
    InlineCodeCommand,
    convert_md_to_latex,
)
from src.converters.latex_dollar_to_paren import convert_latex_dollar_to_paren
from src.converters.latex_to_react.latex_to_react import convert_latex_code_to_react
from src.renderers.latex import DEFAULT_CODE_BLOCK_ENVIRONMENT, DEFAULT_INLINE_CODE_COMMAND
from src.routers.conversion import Conversion, ConversionOption

CONVERSIONS: list[Conversion] = [
    Conversion(
        tag_name="LaTeX → React JSX",
        endpoint_name="latex-to-react",
        source_format="LaTeX",
        target_format="React JSX",
        source_extension="tex",
        target_extension="txt",
        converter=convert_latex_code_to_react,
    ),
    Conversion(
        tag_name="Obsidian Markdown → LaTeX",
        endpoint_name="md-to-latex",
        source_format="Obsidian Markdown",
        target_format="LaTeX",
        source_extension="md",
        target_extension="tex",
        converter=convert_md_to_latex,
        options=[
            ConversionOption(
                name="inline_code_command",
                default=DEFAULT_INLINE_CODE_COMMAND,
                choices=InlineCodeCommand,
                description="LaTeX command used to typeset inline code, as \\command{...}",
            ),
            ConversionOption(
                name="code_block_environment",
                default=DEFAULT_CODE_BLOCK_ENVIRONMENT,
                choices=CodeBlockEnvironment,
                description="LaTeX environment used to typeset fenced code blocks",
            ),
        ],
    ),
    Conversion(
        tag_name="TeX delimiters $x$ and $$x$$ → LaTeX delimiters \\(x\\) and \\[x\\]",
        endpoint_name="latex-dollar-to-paren",
        source_format="LaTeX (dollar delimiters)",
        target_format="LaTeX (paren delimiters)",
        source_extension="tex",
        target_extension="tex",
        converter=convert_latex_dollar_to_paren,
    ),
]
