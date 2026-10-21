from textnode import TextNode, TextType
from directory_del_and_copy import directory_copy_delete
from page_generation import generate_pages_recursive

import sys


def main():
    node = TextNode("some text", TextType.BOLD, "https://example.com")
    print(node)
    directory_copy_delete("static/", "docs/")
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()
