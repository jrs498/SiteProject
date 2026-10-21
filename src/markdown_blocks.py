from enum import Enum

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

def markdown_to_blocks(markdown: str) -> list[str]:
    split_markdown = markdown.split("\n\n")
    blocks = []
    for current in split_markdown:
        current = current.strip()
        if current == "":
            continue
        else:
            blocks.append(current)
    return blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(markdown_block: str) -> BlockType:
    #HEADING
    if markdown_block.startswith(("# ", "## ","### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    #CODE
    if markdown_block.startswith("```\n") and markdown_block.endswith("```"):
        return BlockType.CODE

    lines = markdown_block.split("\n")
    #QUOTE
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    #UNORDERED_LIST
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    #ORDERED_LIST
    orderd_list = True
    for index, line in enumerate(lines, start=1):
        if line.startswith(f"{index}. "):
            continue
        else:
            orderd_list = False
            break
    if orderd_list:
        return BlockType.ORDERED_LIST
    #PARAGRAPH
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            heading_counter = 0
            start = 0
            for i in range(len(block)):
                if block[i] == " ":
                    start = i + 1
                    break
                else:
                    heading_counter += 1
            block_nodes.append(ParentNode(f"h{heading_counter}", text_to_children(block[start:])))
        elif block_type == BlockType.PARAGRAPH:
            lines = block.split("\n")
            cleaned_block = [line.strip() for line in lines]
            text_block = " ".join(cleaned_block)
            block_nodes.append(ParentNode("p", text_to_children(text_block)))
        elif block_type == BlockType.CODE:
            text = block[4:]
            text = text[:-3]
            code_node = TextNode(text, TextType.TEXT)
            code_html_child = text_node_to_html_node(code_node)
            block_nodes.append(ParentNode("pre", [ParentNode("code", [code_html_child])]))
        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            cleaned_block = [line.lstrip(">").strip() for line in lines]
            text_block = " ".join(cleaned_block)
            block_nodes.append(ParentNode("blockquote", text_to_children(text_block)))
        elif block_type == BlockType.ORDERED_LIST:
            items = []
            lines = block.split("\n")
            for line in lines:
                index = line.index(". ") + 2
                items.append(ParentNode("li", text_to_children(line[index:])))
            block_nodes.append(ParentNode("ol", items))
        elif block_type == BlockType.UNORDERED_LIST:
            items = []
            lines = block.split("\n")
            for line in lines:
                items.append(ParentNode("li", text_to_children(line[2:])))
            block_nodes.append(ParentNode("ul", items))
        else:
            raise ValueError("Error: an incorrect block type was passed")
    return ParentNode("div", block_nodes)


def text_to_children(text):
    to_textnode_list = text_to_textnodes(text)
    nodes = []
    for textnode in to_textnode_list:
        nodes.append(text_node_to_html_node(textnode))
    return nodes

def extract_title(markdown: str) -> str:
    if markdown.startswith(("# ", "## ","### ", "#### ", "##### ", "###### ")):
        return markdown.lstrip("#")[1:]
    else:
        raise Exception("Error: Invalid markdown header")
