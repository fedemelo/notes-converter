from __future__ import annotations

import re
import unicodedata

from markdown_it import MarkdownIt
from markdown_it.token import Token
from mdit_py_plugins.dollarmath import dollarmath_plugin

from src.ir.nodes import (
    BlockNode,
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

_CALLOUT_RE = re.compile(r"^\[!(\w+)\]\s*(.*)", re.IGNORECASE)

# Matches [[File\#Section|display]] and [[File#Section|display]].
# Both the file and section parts are optional; only display is required.
_WIKILINK_RE = re.compile(
    r"\[\["
    r"[^\]|#\\]*"       # optional file name
    r"(?:\\?#"          # \# or #
    r"([^\]|]+))?"      # section name (group 1)
    r"\|"
    r"([^\]]+)"         # display text (group 2)
    r"\]\]"
)


def to_label(title: str) -> str:
    """Convert a title to a snake_case ASCII label suitable for LaTeX \\label."""
    nfd = unicodedata.normalize("NFD", title)
    ascii_only = "".join(c for c in nfd if unicodedata.category(c) != "Mn")
    cleaned = re.sub(r"[^a-z0-9\s]", "", ascii_only.lower())
    return re.sub(r"\s+", "_", cleaned.strip())


def _inline_plain_text(nodes: list[InlineNode]) -> str:
    """Extract plain text from inline nodes for label generation."""
    parts = []
    for node in nodes:
        if isinstance(node, Text):
            parts.append(node.content)
        elif isinstance(node, (Emphasis, Strong)):
            parts.append(_inline_plain_text(node.children))
    return "".join(parts)


class ObsidianMarkdownParser:
    def __init__(self) -> None:
        self._md = MarkdownIt().use(dollarmath_plugin)

    def parse(self, source: str) -> Document:
        tokens = self._md.parse(source)
        return Document(children=self._parse_blocks(tokens))

    # ── Block-level parsing ───────────────────────────────────────────────────

    def _parse_blocks(self, tokens: list[Token]) -> list[BlockNode]:
        nodes: list[BlockNode] = []
        i = 0
        while i < len(tokens):
            token = tokens[i]

            if token.type == "heading_open":
                level = int(token.tag[1])
                inline = tokens[i + 1]
                title = self._parse_inlines(inline.children or [])
                label = to_label(_inline_plain_text(title))
                nodes.append(Heading(level=level, title=title, label=label))
                i += 3  # heading_open, inline, heading_close

            elif token.type == "paragraph_open":
                inline = tokens[i + 1]
                children = self._parse_inlines(inline.children or [])
                nodes.append(Paragraph(children=children))
                i += 3  # paragraph_open, inline, paragraph_close

            elif token.type == "math_block":
                nodes.append(DisplayMath(content=token.content.strip()))
                i += 1

            elif token.type == "blockquote_open":
                inner, i = self._consume_block(
                    tokens, i, "blockquote_open", "blockquote_close"
                )
                callout = self._try_parse_callout(inner)
                if callout is not None:
                    nodes.append(callout)
                else:
                    nodes.extend(self._parse_blocks(inner))

            else:
                i += 1

        return nodes

    def _consume_block(
        self,
        tokens: list[Token],
        start: int,
        open_type: str,
        close_type: str,
    ) -> tuple[list[Token], int]:
        """Returns (inner_tokens, next_index) for a matched open/close pair."""
        depth = 1
        i = start + 1
        while i < len(tokens) and depth > 0:
            if tokens[i].type == open_type:
                depth += 1
            elif tokens[i].type == close_type:
                depth -= 1
            i += 1
        return tokens[start + 1 : i - 1], i

    def _try_parse_callout(self, inner: list[Token]) -> BlockNode | None:
        """Detects an Obsidian callout (> [!type] title) and returns a semantic node."""
        for idx, token in enumerate(inner):
            if token.type != "inline":
                continue
            # Match only the first line — without a blank line the whole callout is one
            # paragraph whose inline children are separated by a softbreak token.
            first_line = token.content.split("\n")[0]
            m = _CALLOUT_RE.match(first_line)
            if not m:
                return None  # First inline is not a callout marker.
            callout_type = m.group(1).lower()
            title = m.group(2).strip()
            body = self._build_callout_body(token, inner[idx + 1 :])
            if callout_type in ("tip", "definition"):
                return Definition(title=title, label=to_label(title), body=body)
            if callout_type == "info":
                return Theorem(title=title, label=to_label(title), body=body)
            if callout_type == "note":
                return Note(body=body)
            return None  # Unknown callout type — fall through to ordinary blockquote.
        return None

    def _build_callout_body(
        self, title_token: Token, remaining: list[Token]
    ) -> list[BlockNode]:
        """Collects body blocks from a callout.

        When there is no blank line between the callout title and body, the
        body text appears after the first softbreak in the title's inline
        children. When a blank line is present the body arrives as separate
        block tokens in *remaining*.
        """
        body: list[BlockNode] = []
        children = title_token.children or []
        break_idx = next(
            (i for i, c in enumerate(children) if c.type in ("softbreak", "hardbreak")),
            None,
        )
        if break_idx is not None:
            body_inline = children[break_idx + 1 :]
            if body_inline:
                body.append(Paragraph(children=self._parse_inlines(body_inline)))
        body.extend(self._parse_blocks(remaining))
        return body

    # ── Inline-level parsing ──────────────────────────────────────────────────

    def _parse_inlines(self, tokens: list[Token]) -> list[InlineNode]:
        nodes: list[InlineNode] = []
        i = 0
        while i < len(tokens):
            token = tokens[i]

            if token.type == "text":
                if token.content:
                    nodes.extend(self._split_wikilinks(token.content))
                i += 1

            elif token.type == "math_inline":
                nodes.append(InlineMath(content=token.content))
                i += 1

            elif token.type == "em_open":
                close = self._find_close(tokens, i + 1, "em_close")
                children = self._parse_inlines(tokens[i + 1 : close])
                nodes.append(Emphasis(children=children))
                i = close + 1

            elif token.type == "strong_open":
                close = self._find_close(tokens, i + 1, "strong_close")
                children = self._parse_inlines(tokens[i + 1 : close])
                nodes.append(Strong(children=children))
                i = close + 1

            elif token.type == "image":
                src = token.attrGet("src") or ""
                alt = token.content
                nodes.append(Image(src=src, alt=alt))
                i += 1

            elif token.type in ("softbreak", "hardbreak"):
                nodes.append(Text(content=" "))
                i += 1

            else:
                i += 1

        return nodes

    def _split_wikilinks(self, content: str) -> list[InlineNode]:
        """Split a text string into Text and Ref nodes on wiki-link boundaries."""
        nodes: list[InlineNode] = []
        last = 0
        for m in _WIKILINK_RE.finditer(content):
            if m.start() > last:
                nodes.append(Text(content[last : m.start()]))
            section = (m.group(1) or "").strip()
            display = m.group(2).strip()
            label = "sec:" + to_label(section) if section else ""
            nodes.append(Ref(label=label, text=display))
            last = m.end()
        if last < len(content):
            nodes.append(Text(content[last:]))
        return nodes or [Text(content)]

    def _find_close(self, tokens: list[Token], start: int, close_type: str) -> int:
        for j in range(start, len(tokens)):
            if tokens[j].type == close_type:
                return j
        return len(tokens)
