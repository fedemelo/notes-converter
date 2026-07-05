from __future__ import annotations

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

_HEADING_TAGS = {1: "h1", 2: "h2", 3: "h3", 4: "h4", 5: "h5", 6: "h6"}


class ReactRenderer:
    def render(self, doc: Document) -> str:
        parts = [self._render_block(node) for node in doc.children]
        return "\n".join(p for p in parts if p)

    # ── Block rendering ───────────────────────────────────────────────────────

    def _render_block(self, node: BlockNode) -> str:
        match node:
            case Heading():
                tag = _HEADING_TAGS.get(node.level, "h6")
                return f"<{tag}>{self._render_inlines(node.title)}</{tag}>"

            case Paragraph():
                return self._render_inlines(node.children)

            case DisplayMath():
                return f"<M block>\n    {{r`{node.content}`}}\n</M>"

            case UnorderedList():
                inner = "\n".join(self._render_list_item(i) for i in node.items)
                return f"<ul>\n{inner}\n</ul>"

            case OrderedList():
                inner = "\n".join(self._render_list_item(i) for i in node.items)
                return f"<ol>\n{inner}\n</ol>"

            case Note():
                return f"<Tip>\n{self._render_body(node.body)}\n</Tip>"

            case Warning():
                return f"<Warning>\n{self._render_body(node.body)}\n</Warning>"

            case Notation():
                return f"<Notation>\n{self._render_body(node.body)}\n</Notation>"

            case Definition():
                return (
                    f'<Definition concept="{node.title}">\n'
                    f"    {self._render_body(node.body)}\n"
                    f"</Definition>"
                )

            case Example():
                return (
                    f'<Example title="{node.title}">\n'
                    f" {self._render_body(node.body)}\n"
                    f"</Example>"
                )

            case Theorem():
                return (
                    f'<Theorem name="{node.title}">\n'
                    f"    {self._render_body(node.body)}\n"
                    f"</Theorem>"
                )

            case Comment():
                return f"{{/* {node.content} */}}"

            case Figure() | VerticalSpace():
                return ""

            case _:
                raise NotImplementedError(
                    f"ReactRenderer has no rendering for block node {type(node).__name__}"
                )

    def _render_list_item(self, item: ListItem) -> str:
        return f"<li>{self._render_inlines(item.children)}</li>"

    def _render_body(self, blocks: list[BlockNode]) -> str:
        parts = [self._render_block(b) for b in blocks]
        return "\n".join(p for p in parts if p)

    # ── Inline rendering ──────────────────────────────────────────────────────

    def _render_inlines(self, nodes: list[InlineNode]) -> str:
        return "".join(self._render_inline(n) for n in nodes)

    def _render_inline(self, node: InlineNode) -> str:
        match node:
            case Text():
                return node.content

            case InlineMath():
                if node.display:
                    return f"<M block>\n    {{r`{node.content}`}}\n</M>"
                return f"<M>{{r`{node.content}`}}</M>"

            case Strong():
                return f"<b>{self._render_inlines(node.children)}</b>"

            case Italic():
                return f"<i>{self._render_inlines(node.children)}</i>"

            case Emphasis():
                return f"<em>{self._render_inlines(node.children)}</em>"

            case Underline():
                return f"<u>{self._render_inlines(node.children)}</u>"

            case Quote():
                return f'"{self._render_inlines(node.children)}"'

            case Hyperlink():
                return node.text

            case Ref():
                return ""

            case _:
                raise NotImplementedError(
                    f"ReactRenderer has no rendering for inline node {type(node).__name__}"
                )
