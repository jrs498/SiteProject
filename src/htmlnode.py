

from pty import CHILD


class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
         self.tag = tag
         self.value = value
         self.children = children
         self.props = props

    def __repr__(self):
        return f"tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r}"

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        formatted: list[str] = []
        if not self.props:
            return ""
        for key, value in self.props.items():
            formatted.append(f" {key}=\"{value}\"")

        return "".join(formatted)

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict = None):
        super().__init__(tag, value, None, props)

    def __repr__(self):
        return f"tag={self.tag!r}, value={self.value!r}, props={self.props!r}"

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if not self.tag:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict = None):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        if self.children is None:
            raise ValueError("Error: Missing children")

        formatted = ""
        for child in self.children:
            formatted += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{formatted}</{self.tag}>"
