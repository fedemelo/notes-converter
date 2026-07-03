from __future__ import annotations

import re

from src.ir.nodes import (
    BlockNode,
    Comment,
    Definition,
    DisplayMath,
    Document,
    Emphasis,
    Heading,
    Image,
    InlineMath,
    InlineNode,
    Note,
    Paragraph,
    Ref,
    Strong,
    Text,
    Theorem,
)

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
                return f"\\[\n{node.content}\n\\]"

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
                return ""

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
                    return f"\\[\n{node.content}\n\\]"
                return f"\\({node.content}\\)"

            case Emphasis():
                return f"\\textit{{{self._render_inlines(node.children)}}}"

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

            case _:
                return ""

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _escape(self, text: str) -> str:
        return _SPECIAL.sub(lambda m: _ESCAPE_MAP[m.group()], text)
