from typing_extensions import Text

from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
           node_parts = node.text.split(delimiter)
           if len(node_parts) % 2 == 0:
               raise Exception("Invalid Markdown syntax, delimiter does not match")
           else:
                for i in range(len(node_parts)):
                    if node_parts[i] == "":
                        continue
                    current_text = node_parts[i]
                    if i % 2 == 0:
                        current_type = TextType.TEXT
                    else:
                        current_type = text_type
                    new_nodes.append(TextNode(current_text, current_type))
    return new_nodes

def extract_markdown_images(text) -> list[tuple]:
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
           node_parts = extract_markdown_images(node.text)
           if node_parts == []:
               new_nodes.append(node)
           else:
               remaining = node.text
               for image_alt, image_link in node_parts:
                   sections = remaining.split(f"![{image_alt}]({image_link})", 1)
                   if sections[0] != "":
                       new_nodes.append(TextNode(sections[0], TextType.TEXT))
                   new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                   remaining = sections[1]
               if remaining != "":
                   new_nodes.append(TextNode(remaining, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
           node_parts = extract_markdown_links(node.text)
           if node_parts == []:
               new_nodes.append(node)
           else:
               remaining = node.text
               for link_alt, link in node_parts:
                   sections = remaining.split(f"[{link_alt}]({link})", 1)
                   if sections[0] != "":
                       new_nodes.append(TextNode(sections[0], TextType.TEXT))
                   new_nodes.append(TextNode(link_alt, TextType.LINK, link))
                   remaining = sections[1]
               if remaining != "":
                   new_nodes.append(TextNode(remaining, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text) -> list[TextNode]:
    new_nodes = [TextNode(text, TextType.TEXT)]

    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes
