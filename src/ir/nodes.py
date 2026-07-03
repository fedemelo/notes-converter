from __future__ import annotations

from dataclasses import dataclass, field

# ── Inline nodes ──────────────────────────────────────────────────────────────
# Nodes that flow within a line of text.


@dataclass
class Text:
    content: str


@dataclass
class InlineMath:
    content: str
    display: bool = False  # True for $$...$$, renders as \[...\]


@dataclass
class Emphasis:
    children: list[InlineNode] = field(default_factory=list)


@dataclass
class Strong:
    children: list[InlineNode] = field(default_factory=list)


@dataclass
class Image:
    src: str
    alt: str


@dataclass
class Ref:
    label: str  # full LaTeX label, e.g. "sec:grafos_ponderados"
    text: str  # display text shown in the document


InlineNode = Text | InlineMath | Emphasis | Strong | Image | Ref

# ── Block nodes ───────────────────────────────────────────────────────────────
# Nodes that occupy their own vertical space in a document.


@dataclass
class Paragraph:
    children: list[InlineNode] = field(default_factory=list)


@dataclass
class Heading:
    level: int
    title: list[InlineNode] = field(default_factory=list)
    label: str = ""  # snake_case base label; renderer adds the "sec:" prefix


@dataclass
class DisplayMath:
    content: str


@dataclass
class Definition:
    title: str
    label: str
    body: list[BlockNode] = field(default_factory=list)


@dataclass
class Theorem:
    title: str
    label: str
    body: list[BlockNode] = field(default_factory=list)


@dataclass
class Note:
    body: list[BlockNode] = field(default_factory=list)


@dataclass
class Comment:
    content: str  # text after the leading #, e.g. "TODO fix this"


@dataclass
class Document:
    children: list[BlockNode] = field(default_factory=list)


BlockNode = Paragraph | Heading | DisplayMath | Definition | Theorem | Note | Comment
