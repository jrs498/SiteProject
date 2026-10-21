from textnode import TextNode, TextType
from directory_del_and_copy import directory_copy_delete
from page_generation import generate_pages_recursive


def main():
    node = TextNode("some text", TextType.BOLD, "https://example.com")
    print(node)
    directory_copy_delete("static/", "public/")
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
