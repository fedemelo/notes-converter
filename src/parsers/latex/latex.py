from __future__ import annotations

import re

from src.exceptions import MalformedLatexError
from src.ir.nodes import (
    BlockNode,
    Comment,
    Definition,
    DisplayMath,
    Document,
    Emphasis,
    Example,
    Figure,
    Heading,
    Hyperlink,
    InlineMath,
    InlineNode,
    Italic,
    ListItem,
    Notation,
    Note,
    OrderedList,
    Paragraph,
    Quote,
    Ref,
    Strong,
    Text,
    Theorem,
    Underline,
    UnorderedList,
    VerticalSpace,
    Warning,
)

_HEADING_CMDS: dict[str, int] = {
    r"\part": 1,
    r"\section": 2,
    r"\subsection": 3,
    r"\subsubsection": 4,
    r"\paragraph": 5,
}

# Environments whose body is parsed as blocks (no extra args).
_SIMPLE_ENVS: dict[str, type] = {
    "tip": Note,
    "advertencia": Warning,
    "notacion": Notation,
}

# Environments with {title}{label} args before the body.
_TITLED_ENVS: dict[str, type] = {
    "definicion": Definition,
    "ejemplo": Example,
    "teorema": Theorem,
}

# Math environments whose LaTeX wrapper must be preserved in the IR.
_WRAP_MATH_ENVS = {"gather*", "align*"}

_HEADING_RE = re.compile(
    r"\\(part|section|subsection|subsubsection|paragraph)\{"
)

# A position where a block-level element begins.
_BLOCK_START_RE = re.compile(
    r"\\begin\{"
    r"|\\(?:part|section|subsection|subsubsection|paragraph)\{"
    r"|\\vspace\{"
    r"|\\noindent(?=[ \t\n]|$)"
    r"|\\\["
    r"|\$\$"
    r"|%"
    r"|\n\n"
    r"|\\item(?=[ \t\n]|$)"
)

_ITEM_RE = re.compile(r"\\item(?=[ \t\n]|$)")


class LatexParser:
    """Parse a LaTeX string into a Document of IR nodes."""

    def parse(self, source: str) -> Document:
        self._src = source
        self._pos = 0
        return Document(children=self._parse_blocks())

    # ── Block-level ───────────────────────────────────────────────────────────

    def _parse_blocks(self, stop_tag: str | None = None) -> list[BlockNode]:
        blocks: list[BlockNode] = []
        while self._pos < len(self._src):
            if stop_tag and self._src[self._pos:].startswith(stop_tag):
                break
            self._skip_blank()
            if self._pos >= len(self._src):
                break
            if stop_tag and self._src[self._pos:].startswith(stop_tag):
                break
            node = self._next_block()
            if node is not None:
                blocks.append(node)
        return blocks

    def _next_block(self) -> BlockNode | None:
        s = self._src
        p = self._pos

        if s[p:].startswith(r"\begin{"):
            return self._parse_env()

        m = _HEADING_RE.match(s, p)
        if m:
            return self._parse_heading(m.group(1))

        if s[p:p + 2] == "$$":
            return self._parse_display_math_dollar_dollar()

        if s[p:p + 2] == r"\[":
            return self._parse_display_math_bracket()

        if s[p] == "%":
            return self._parse_comment()

        if s[p:].startswith(r"\vspace{"):
            return self._parse_vspace()

        if s[p:].startswith(r"\noindent"):
            self._pos += len(r"\noindent")
            if self._pos < len(s) and s[self._pos] in " \t":
                self._pos += 1
            return None

        if _ITEM_RE.match(s[p:]):
            line = self._src[:p].count('\n') + 1
            raise MalformedLatexError(
                f"\\item at line {line} is outside a list environment "
                f"(\\item is only valid inside \\begin{{itemize}} or \\begin{{enumerate}})"
            )

        return self._parse_paragraph()

    # ── Environment dispatch ──────────────────────────────────────────────────

    def _parse_env(self) -> BlockNode | None:
        m = re.match(r"\\begin\{([^}]+)\}", self._src[self._pos:])
        if not m:
            return self._parse_paragraph()
        raw_env = m.group(1)
        env = raw_env.lower()
        self._pos += m.end()

        if env == "equation*":
            return DisplayMath(content=self._consume_until_end(raw_env))

        if env in _WRAP_MATH_ENVS:
            body = self._consume_until_end(raw_env)
            return DisplayMath(
                content=rf"\begin{{{raw_env}}}{body}\end{{{raw_env}}}"
            )

        if env == "figure":
            return self._parse_env_figure(raw_env)

        if env in ("itemize", "enumerate"):
            body = self._consume_until_end(raw_env)
            items = self._items_from(body)
            cls = UnorderedList if env == "itemize" else OrderedList
            return cls(items=items)

        if env in _SIMPLE_ENVS:
            body = self._consume_until_end(raw_env)
            return _SIMPLE_ENVS[env](body=self._blocks_from(body))

        if env in _TITLED_ENVS:
            title = self._consume_braced()
            label = self._consume_braced()
            body = self._consume_until_end(raw_env)
            return _TITLED_ENVS[env](
                title=title, label=label, body=self._blocks_from(body)
            )

        self._consume_until_end(raw_env)
        return None

    def _parse_env_figure(self, raw_env: str) -> Figure:
        body = self._consume_until_end(raw_env)
        src_m = re.search(r"\\includegraphics\{([^}]+)\}", body)
        cap_m = re.search(r"\\caption\{([^}]+)\}", body)
        return Figure(
            src=src_m.group(1) if src_m else "",
            caption=cap_m.group(1) if cap_m else "",
        )

    # ── Block parsers ─────────────────────────────────────────────────────────

    def _parse_heading(self, cmd_name: str) -> Heading:
        self._pos += len(f"\\{cmd_name}")
        title_raw = self._consume_braced()
        label = ""
        self._skip_inline_space()
        if self._src[self._pos:].startswith(r"\label{"):
            self._pos += len(r"\label{")
            end = self._src.index("}", self._pos)
            label = self._src[self._pos:end]
            self._pos = end + 1
        return Heading(
            level=_HEADING_CMDS[f"\\{cmd_name}"],
            title=self._inlines_from(title_raw),
            label=label,
        )

    def _parse_display_math_bracket(self) -> DisplayMath:
        self._pos += 2  # skip \[
        end = self._src.find(r"\]", self._pos)
        if end == -1:
            content = self._src[self._pos:]
            self._pos = len(self._src)
        else:
            content = self._src[self._pos:end]
            self._pos = end + 2
        return DisplayMath(content=content)

    def _parse_display_math_dollar_dollar(self) -> DisplayMath:
        self._pos += 2  # skip $$
        end = self._src.find("$$", self._pos)
        if end == -1:
            content = self._src[self._pos:]
            self._pos = len(self._src)
        else:
            content = self._src[self._pos:end]
            self._pos = end + 2
        return DisplayMath(content=content)

    def _parse_comment(self) -> Comment:
        self._pos += 1  # skip %
        end = self._src.find("\n", self._pos)
        if end == -1:
            content = self._src[self._pos:]
            self._pos = len(self._src)
        else:
            content = self._src[self._pos:end]
            self._pos = end + 1  # consume the newline too
        return Comment(content=content)

    def _parse_vspace(self) -> VerticalSpace:
        self._pos += len(r"\vspace")
        return VerticalSpace(amount=self._consume_braced())

    def _parse_paragraph(self) -> Paragraph | None:
        m = _BLOCK_START_RE.search(self._src, self._pos)
        end = m.start() if m else len(self._src)
        raw = self._src[self._pos:end].strip()
        self._pos = end
        if not raw:
            return None
        return Paragraph(children=self._inlines_from(raw))

    # ── Inline-level ──────────────────────────────────────────────────────────

    def _inlines_from(self, text: str) -> list[InlineNode]:
        """Parse all inline nodes from a string, using a temporary cursor."""
        saved = (self._src, self._pos)
        self._src, self._pos = text, 0
        nodes: list[InlineNode] = []
        while self._pos < len(self._src):
            node = self._next_inline()
            if node is not None:
                nodes.append(node)
        self._src, self._pos = saved
        return _merge_text(nodes)

    def _next_inline(self) -> InlineNode | None:
        s, p = self._src, self._pos

        if s[p] == "$":
            self._pos += 1
            end = s.find("$", self._pos)
            content = s[self._pos:end] if end != -1 else s[self._pos:]
            self._pos = end + 1 if end != -1 else len(s)
            return InlineMath(content=content)

        if s[p:p + 2] == r"\(":
            self._pos += 2
            end = s.find(r"\)", self._pos)
            content = s[self._pos:end] if end != -1 else s[self._pos:]
            self._pos = end + 2 if end != -1 else len(s)
            return InlineMath(content=content)

        if s[p:].startswith(r"\textbf{"):
            self._pos += len(r"\textbf")
            return Strong(children=self._inlines_from(self._consume_braced()))

        if s[p:].startswith(r"\textit{"):
            self._pos += len(r"\textit")
            return Italic(children=self._inlines_from(self._consume_braced()))

        if s[p:].startswith(r"\emph{"):
            self._pos += len(r"\emph")
            return Emphasis(children=self._inlines_from(self._consume_braced()))

        if s[p:].startswith(r"\underline{"):
            self._pos += len(r"\underline")
            return Underline(children=self._inlines_from(self._consume_braced()))

        if s[p:].startswith(r"\say{"):
            self._pos += len(r"\say")
            return Quote(children=self._inlines_from(self._consume_braced()))

        if s[p:].startswith(r"\href{"):
            self._pos += len(r"\href")
            target = self._consume_braced()
            text = self._consume_braced()
            return Hyperlink(target=target, text=text)

        if s[p:].startswith(r"\hyperlink{"):
            self._pos += len(r"\hyperlink")
            target = self._consume_braced()
            text = self._consume_braced()
            return Hyperlink(target=target, text=text)

        if s[p:].startswith(r"\ref{"):
            self._pos += len(r"\ref")
            return Ref(label=self._consume_braced(), text="")

        if s[p:].startswith(r"\autoref{"):
            self._pos += len(r"\autoref")
            return Ref(label=self._consume_braced(), text="")

        if s[p:].startswith(r"\label{"):
            self._pos += len(r"\label")
            self._consume_braced()
            return None

        if s[p:].startswith(r"\noindent"):
            self._pos += len(r"\noindent")
            if self._pos < len(s) and s[self._pos] in " \t":
                self._pos += 1
            return None

        self._pos += 1
        return Text(content=s[p])

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _consume_until_end(self, env: str) -> str:
        end_tag = rf"\end{{{env}}}"
        idx = self._src.find(end_tag, self._pos)
        if idx == -1:
            content = self._src[self._pos:]
            self._pos = len(self._src)
        else:
            content = self._src[self._pos:idx]
            self._pos = idx + len(end_tag)
        return content

    def _consume_braced(self) -> str:
        s = self._src
        if self._pos >= len(s) or s[self._pos] != "{":
            return ""
        self._pos += 1
        start = self._pos
        depth = 1
        while self._pos < len(s) and depth:
            if s[self._pos] == "{":
                depth += 1
            elif s[self._pos] == "}":
                depth -= 1
            self._pos += 1
        return s[start:self._pos - 1]

    def _blocks_from(self, text: str) -> list[BlockNode]:
        saved = (self._src, self._pos)
        self._src, self._pos = text, 0
        blocks = self._parse_blocks()
        self._src, self._pos = saved
        return blocks

    def _items_from(self, content: str) -> list[ListItem]:
        items = []
        for m in re.finditer(r"\\item(.+?)(?=\\item|\Z)", content, re.DOTALL):
            children = self._inlines_from(m.group(1).strip())
            items.append(ListItem(children=children))
        return items

    def _skip_blank(self) -> None:
        while self._pos < len(self._src) and self._src[self._pos] in " \t\n\r":
            self._pos += 1

    def _skip_inline_space(self) -> None:
        while self._pos < len(self._src) and self._src[self._pos] in " \t":
            self._pos += 1


def _merge_text(nodes: list[InlineNode]) -> list[InlineNode]:
    out: list[InlineNode] = []
    for node in nodes:
        if isinstance(node, Text) and out and isinstance(out[-1], Text):
            out[-1] = Text(out[-1].content + node.content)
        else:
            out.append(node)
    return out
