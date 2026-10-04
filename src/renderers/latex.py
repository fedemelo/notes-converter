from __future__ import annotations

import re

from src.ir.nodes import (
    BlockNode,
    CodeBlock,
    Comment,
    Definition,
    DisplayMath,
    Document,
    Emphasis,
    Heading,
    Image,
    InlineCode,
    InlineMath,
    InlineNode,
    Italic,
    Note,
    Paragraph,
    Ref,
    Strong,
    Text,
    Theorem,
)
from src.latex_tools.math_delimiters import (
    DEFAULT_MATH_DELIMITER_STYLE,
    MathDelimiterStyle,
    display_math_delimiters,
    inline_math_delimiters,
)

DEFAULT_INLINE_CODE_COMMAND = "texttt"
DEFAULT_CODE_BLOCK_ENVIRONMENT = "verbatim"

_HEADING_COMMANDS = {
    1: r"\part",
    2: r"\section",
    3: r"\subsection",
    4: r"\subsubsection",
    5: r"\subsubsection",
    6: r"\subsubsection",
}

# Single-pass LaTeX escaping — backslash must be handled first.
# Environments that are themselves display-math containers; no \[...\] wrapper needed.
_STANDALONE_ENV_RE = re.compile(
    r"^\\begin\{"
    r"(equation\*?|gather\*?|align\*?|multline\*?|flalign\*?|eqnarray\*?|alignat\*?)"
    r"\}"
)

_SPECIAL = re.compile(r"[\\&%$#_{}\^~]")
_ESCAPE_MAP = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "^": r"\^{}",
    "~": r"\textasciitilde{}",
}


class LatexRenderer:
    def __init__(
        self,
        inline_code_command: str = DEFAULT_INLINE_CODE_COMMAND,
        code_block_environment: str = DEFAULT_CODE_BLOCK_ENVIRONMENT,
        math_delimiter_style: MathDelimiterStyle = DEFAULT_MATH_DELIMITER_STYLE,
    ) -> None:
        self._inline_code_command = inline_code_command
        self._code_block_environment = code_block_environment
        self._math_delimiter_style = MathDelimiterStyle(math_delimiter_style)

    def render(self, doc: Document) -> str:
        return "\n\n".join(
            rendered for node in doc.children if (rendered := self._render_block(node))
        )

    # ── Block rendering ───────────────────────────────────────────────────────

    def _render_block(self, node: BlockNode) -> str:
        match node:
            case Heading():
                cmd = _HEADING_COMMANDS.get(node.level, r"\subsubsection")
                result = f"{cmd}{{{self._render_inlines(node.title)}}}"
                if node.label:
                    result += f"\n\\label{{sec:{node.label}}}"
                return result

            case Paragraph():
                return self._render_inlines(node.children)

            case DisplayMath():
                if _STANDALONE_ENV_RE.match(node.content.strip()):
                    return node.content.strip()
                open_, close = display_math_delimiters(self._math_delimiter_style)
                return f"{open_}\n{node.content}\n{close}"

            case CodeBlock():
                env = self._code_block_environment
                return f"\\begin{{{env}}}\n{node.content}\n\\end{{{env}}}"

            case Definition():
                return (
                    f"\\begin{{definicion}}{{{node.title}}}{{{node.label}}}\n"
                    f"{self._render_body(node.body)}\n"
                    f"\\end{{definicion}}"
                )

            case Theorem():
                return (
                    f"\\begin{{teorema}}{{{node.title}}}{{{node.label}}}\n"
                    f"{self._render_body(node.body)}\n"
                    f"\\end{{teorema}}"
                )

            case Note():
                return (
                    f"\\begin{{tip}}\n"
                    f"{self._render_body(node.body)}\n"
                    f"\\end{{tip}}"
                )

            case Comment():
                return f"%{node.content}"

            case _:
                raise NotImplementedError(
                    f"LatexRenderer has no rendering for block node {type(node).__name__}"
                )

    def _render_body(self, blocks: list[BlockNode]) -> str:
        joined = "\n\n".join(self._render_block(b) for b in blocks)
        if not joined:
            return ""
        return "\n".join("  " + line for line in joined.split("\n"))

    # ── Inline rendering ──────────────────────────────────────────────────────

    def _render_inlines(self, nodes: list[InlineNode]) -> str:
        return "".join(self._render_inline(n) for n in nodes)

    def _render_inline(self, node: InlineNode) -> str:
        match node:
            case Text():
                return self._escape(node.content)

            case InlineMath():
                if node.display:
                    stripped = node.content.strip()
                    if _STANDALONE_ENV_RE.match(stripped):
                        return stripped
                    open_, close = display_math_delimiters(self._math_delimiter_style)
                    return f"{open_}\n{node.content}\n{close}"
                open_, close = inline_math_delimiters(self._math_delimiter_style)
                return f"{open_}{node.content}{close}"

            case Italic():
                return f"\\textit{{{self._render_inlines(node.children)}}}"

            case Emphasis():
                return f"\\emph{{{self._render_inlines(node.children)}}}"

            case Strong():
                return f"\\textbf{{{self._render_inlines(node.children)}}}"

            case Image():
                lines = [
                    "\\begin{figure}[h]",
                    "  \\centering",
                    f"  \\includegraphics{{{node.src}}}",
                ]
                if node.alt:
                    lines.append(f"  \\caption{{{self._escape(node.alt)}}}")
                lines.append("\\end{figure}")
                return "\n".join(lines)

            case Ref():
                return f"\\hyperref[{node.label}]{{{node.text}}}"

            case InlineCode():
                return f"\\{self._inline_code_command}{{{self._escape(node.content)}}}"

            case _:
                raise NotImplementedError(
                    f"LatexRenderer has no rendering for inline node {type(node).__name__}"
                )

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _escape(self, text: str) -> str:
        return _SPECIAL.sub(lambda m: _ESCAPE_MAP[m.group()], text)
