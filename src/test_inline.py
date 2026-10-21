import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes


class TestInline(unittest.TestCase):
    def test_no_delimiter(self):
        node = TextNode("This is a test with a code block word", TextType.TEXT)
        new_node = split_nodes_delimiter([node], "`", TextType.TEXT)
        self.assertEqual(new_node, [node])

    def test_unbalanced_delimitter(self):
        node = TextNode("This is a test `with a code block word", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.TEXT)

    def test_balanced_delimiter(self):
        node = TextNode("This is a test with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is a test with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)])

    def test_bold(self):
        node = TextNode("This is a test with a **bold text** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is a test with a ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" word", TextType.TEXT)])

    def test_italic(self):
        node = TextNode("This is a test with a _italic text_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("This is a test with a ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" word", TextType.TEXT)])

    def test_delimiter_at_start(self):
        node = TextNode("``This is a test with a delimiter at the start of the word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.TEXT)
        self.assertEqual(new_nodes,
            [TextNode("This is a test with a delimiter at the start of the word", TextType.TEXT)])

    def test_mixed_list(self):
        nodes = [
            TextNode("already bold, don't touch me", TextType.BOLD),
            TextNode("This has a `code snippet` in it", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("already bold, don't touch me", TextType.BOLD),
            TextNode("This has a ", TextType.TEXT),
            TextNode("code snippet", TextType.CODE),
            TextNode(" in it", TextType.TEXT)])

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [to google](https://www.google.com)"
        )
        self.assertListEqual([("to google", "https://www.google.com")], matches)

    def test_extract_multiple_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [to google](https://www.google.com) and [to youtube](https://www.youtube.com)"
        )
        self.assertListEqual([("to google", "https://www.google.com"), ("to youtube", "https://www.youtube.com")], matches)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![image2](http://imgur.com/abf23.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"),
            ("image2", "http://imgur.com/abf23.png")], matches)

    def test_extract_no_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with nothing"
        )
        self.assertListEqual([], matches)

    def test_extract_no_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with nothing"
        )
        self.assertListEqual([], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_no_images(self):
        node = TextNode(
            "This is text with nothing",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with nothing", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_images_at_start(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) This is text with nothing",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" This is text with nothing", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_only_images(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes,
        )


    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://imgur.com/zjjcJKZ.png) and another [second link](https://imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_no_links(self):
        node = TextNode(
            "This is text with nothing",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with nothing", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_links_at_start(self):
        node = TextNode(
            "[link](https://imgur.com/zjjcJKZ.png) This is text with nothing",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://imgur.com/zjjcJKZ.png"),
                TextNode(" This is text with nothing", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_only_links(self):
        node = TextNode(
            "[link](https://imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://imgur.com/zjjcJKZ.png")
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )


if __name__ == "__main__":
    unittest.main()
