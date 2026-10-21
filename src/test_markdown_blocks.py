
import unittest

from markdown_blocks import markdown_to_blocks, BlockType, block_to_block_type, markdown_to_html_node, extract_title

class TestMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_extra_newlines(self):
        md = """



This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line





- This is a list
- with items

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_trailing_blank_lines(self):
        md = """

This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test__block_to_block_type_heading(self):
        no_space = block_to_block_type("#This is wrong")
        one_hashtag = block_to_block_type("# Just one hash")
        two_hashtag = block_to_block_type("## Just two hash")
        three_hashtag = block_to_block_type("### Just three hash")
        four_hashtag = block_to_block_type("#### Just four hash")
        five_hashtag = block_to_block_type("##### Just five hash")
        six_hashtag = block_to_block_type("###### Just six hash")
        seven_hashtag = block_to_block_type("####### Just seven hash")
        self.assertEqual(no_space, BlockType.PARAGRAPH)
        self.assertEqual(one_hashtag, BlockType.HEADING)
        self.assertEqual(two_hashtag, BlockType.HEADING)
        self.assertEqual(three_hashtag, BlockType.HEADING)
        self.assertEqual(four_hashtag, BlockType.HEADING)
        self.assertEqual(five_hashtag, BlockType.HEADING)
        self.assertEqual(six_hashtag, BlockType.HEADING)
        self.assertEqual(seven_hashtag, BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph(self):
        empty = block_to_block_type(" ")
        self.assertEqual(empty, BlockType.PARAGRAPH)
        no_proper_type = block_to_block_type("random stuff")
        self.assertEqual(no_proper_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_code(self):
        multiline_code = block_to_block_type("```\nThis is a multiline code block\n```")
        self.assertEqual(multiline_code, BlockType.CODE)

    def test_block_to_block_type_quote(self):
        multiline_quote = block_to_block_type(">This is with no space\n> This is with a space\n>Luke I am your father")
        self.assertEqual(multiline_quote, BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        incorrect = block_to_block_type("-No space\n- Correct space")
        self.assertEqual(incorrect, BlockType.PARAGRAPH)
        correct = block_to_block_type("- Correct space\n- Correct space again")
        self.assertEqual(correct, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        incorrect_zero = block_to_block_type("0. Can't start a list with 0\n1. This should be the start")
        self.assertEqual(incorrect_zero, BlockType.PARAGRAPH)
        incorrect_format = block_to_block_type("1. Good\n2. Good\n3.Bad")
        self.assertEqual(incorrect_format, BlockType.PARAGRAPH)
        correct = block_to_block_type("1. Good\n2. Good\n3. Good\n4. Good\n5. Good\n6. Good\n7. Good\n8. Good\n9. Good\n10. Good")
        self.assertEqual(correct, BlockType.ORDERED_LIST)

    def test_div_header(self):
        md ="# Hello"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>Hello</h1></div>")

    def test_div_paragraph(self):
        md = """
        There's a snake in my
        boot
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>There's a snake in my boot</p></div>")

    def test_div_quote(self):
        md = """
> some quote text
> more quote text
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>some quote text more quote text</blockquote></div>",
        )

    def test_div_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_div_unordered(self):
        md = """
- milk
- eggs
- butter
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>milk</li><li>eggs</li><li>butter</li></ul></div>",
        )

    def test_div_ordered(self):
        md = """
1. milk
2. eggs
3. butter
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>milk</li><li>eggs</li><li>butter</li></ol></div>",
        )

    def test_div_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_div_all(self):
        md ="""# Celestia

All hail the Heavenly Principles

## Hobbit

- **What is it? What do you smell?**
- **Man flesh**
- **I can't carry the ring Mr Frodo**
- **But I can carry you**

### StarWars

1. _Euaraauuuuughhhhhghhhhh!_

#### Always Sunny

> Dee you dumb bitch
> You haven't thought of the smell you bitch

##### Always Sunny 2

```
A day in the life-- well, the other morning, I wake up and I find a dog sniffin' at my wound. He's fully aroused - mind you -
so I'm thinking "oh great, what does this jerk want?" Of course I know what he wants, he's looking at me right in the eyes, he does not have to say it - not that he could.
[Starts sucking on a lemon] Urrggghhhh that is- that is tart! That is really tart. I mean does my scar look like a dog's *censored*? You know, maybe, I don't know,
I'm not going to sit here and try to get inside the mind of a dog! I mean that's God's work. Well, not that I believe in God, I don't. Not since that chinaman stole my kidney.
```

###### StarWars 2

A bad list of star wars ranked

1. Episode 4
2. Episode 5
3. Episode 3
4. Episode 2
5. Episode 1
6. Episode 6
7. Rogue One

The rest are **TRASH**

> Sheev Palpatine (Darth Sidious)

```
Did you ever hear the tragedy of Darth Plagueis The Wise? I thought not. It’s not a story the Jedi would tell you. It’s a Sith legend.
Darth Plagueis was a Dark Lord of the Sith, so powerful and so wise he could use the Force to influence the midichlorians to create life…
He had such a knowledge of the dark side that he could even keep the ones he cared about from dying.
The dark side of the Force is a pathway to many abilities some consider to be unnatural. He became so powerful…
the only thing he was afraid of was losing his power, which eventually, of course, he did. Unfortunately, he taught his apprentice everything he knew, then his apprentice killed him in his sleep.
Ironic. He could save others from death, but not himself
```

- **The END**

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = (
                    "<div>"
                    "<h1>Celestia</h1>"
                    "<p>All hail the Heavenly Principles</p>"
                    "<h2>Hobbit</h2>"
                    "<ul><li><b>What is it? What do you smell?</b></li><li><b>Man flesh</b></li><li><b>I can't carry the ring Mr Frodo</b></li><li><b>But I can carry you</b></li></ul>"
                    "<h3>StarWars</h3>"
                    "<ol><li><i>Euaraauuuuughhhhhghhhhh!</i></li></ol>"
                    "<h4>Always Sunny</h4>"
                    "<blockquote>Dee you dumb bitch You haven't thought of the smell you bitch</blockquote>"
                    "<h5>Always Sunny 2</h5>"
                    "<pre><code>A day in the life-- well, the other morning, I wake up and I find a dog sniffin' at my wound. He's fully aroused - mind you -\n"
                    "so I'm thinking \"oh great, what does this jerk want?\" Of course I know what he wants, he's looking at me right in the eyes, he does not have to say it - not that he could.\n"
                    "[Starts sucking on a lemon] Urrggghhhh that is- that is tart! That is really tart. I mean does my scar look like a dog's *censored*? You know, maybe, I don't know,\n"
                    "I'm not going to sit here and try to get inside the mind of a dog! I mean that's God's work. Well, not that I believe in God, I don't. Not since that chinaman stole my kidney.\n</code></pre>"
                    "<h6>StarWars 2</h6>"
                    "<p>A bad list of star wars ranked</p>"
                    "<ol><li>Episode 4</li><li>Episode 5</li><li>Episode 3</li><li>Episode 2</li><li>Episode 1</li><li>Episode 6</li><li>Rogue One</li></ol>"
                    "<p>The rest are <b>TRASH</b></p>"
                    "<blockquote>Sheev Palpatine (Darth Sidious)</blockquote>"
                    "<pre><code>Did you ever hear the tragedy of Darth Plagueis The Wise? I thought not. It’s not a story the Jedi would tell you. It’s a Sith legend.\n"
                    "Darth Plagueis was a Dark Lord of the Sith, so powerful and so wise he could use the Force to influence the midichlorians to create life…\n"
                    "He had such a knowledge of the dark side that he could even keep the ones he cared about from dying.\n"
                    "The dark side of the Force is a pathway to many abilities some consider to be unnatural. He became so powerful…\n"
                    "the only thing he was afraid of was losing his power, which eventually, of course, he did. Unfortunately, he taught his apprentice everything he knew, then his apprentice killed him in his sleep.\n"
                    "Ironic. He could save others from death, but not himself\n</code></pre>"
                    "<ul><li><b>The END</b></li></ul>"
                    "</div>"
                )

        self.assertEqual(html, expected_html)

    def test_extract_title(self):
        md1 = extract_title("# Hello")
        self.assertEqual(md1, "Hello")
        md2 = extract_title("## Hello")
        self.assertEqual(md2, "Hello")
        md3 = extract_title("### Hello")
        self.assertEqual(md3, "Hello")
        md4 = extract_title("#### Hello")
        self.assertEqual(md4, "Hello")
        md5 = extract_title("##### Hello")
        self.assertEqual(md5, "Hello")
        md6 = extract_title("###### Hello")
        self.assertEqual(md6, "Hello")
        with self.assertRaises(Exception):
            extract_title("####### Hello")
        with self.assertRaises(Exception):
            extract_title("####Hello")
        with self.assertRaises(Exception):
            extract_title("Hello")




if __name__ == "__main__":
    unittest.main()
