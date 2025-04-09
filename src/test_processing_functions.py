import unittest
from textnode import *
from node_processing_functions import *
class test_processing_functions(unittest.TestCase):
        ###
        ###
        # Tests for text_node_to_html_node
        
    def test_text_node_to_html_node_TEXT(self):
        # Test text_node_to_html_node with TEXT text
        node = TextNode("Hello", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Hello")

    def test_text_node_to_html_node_bold(self):
        # Test text_node_to_html_node with bold text
        node = TextNode("Hello", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Hello")

    def test_text_node_to_html_node_italic(self):
        # Test text_node_to_html_node with italic text  
        node = TextNode("Hello", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Hello")

    def test_text_node_to_html_node_code(self):
        # Test text_node_to_html_node with code text
        node = TextNode("Hello", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Hello")

    def test_text_node_to_html_node_link(self):
        # Test text_node_to_html_node with a link
        node = TextNode("Google", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Google")
        self.assertEqual(html_node.props,{'href': "https://www.google.com"})

    def test_text_node_to_html_node_image(self):
        # Test text_node_to_html_node with an image
        node = TextNode("Image", TextType.IMAGE, {'src': "https://www.example.com/image.jpg", 'alt': "alt text"})
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props['alt'], "Image")

    def test_text_node_to_html_node_invalid_type(self):
        # Test text_node_to_html_node with invalid TextType
        with self.assertRaises(Exception): 
        # Expect an exception when trying to create a TextNode with an invalid type
            TextNode("Invalid", TextType.OTHER)
    
    def test_eq_different_values(self):
        # Test equality method with different text
        node1 = TextNode("Hello", TextType.TEXT)
        node2 = TextNode("World", TextType.TEXT)
        self.assertFalse(node1 == node2)

        # Test equality method with different text_type
        node3 = TextNode("Hello", TextType.BOLD)
        self.assertFalse(node1 == node3)

        # Test equality method with different URL
        node4 = TextNode("Google", TextType.LINK, "https://www.google.com")
        node5 = TextNode("Google", TextType.LINK, "https://www.bing.com")
        self.assertFalse(node4 == node5)

    def test_repr(self):
        # Test __repr__ method for TextNode
        node = TextNode("Hello", TextType.TEXT)
        self.assertEqual(repr(node), "TextNode(Hello, normal, None)")

    def test_repr_with_url(self):
        # Test __repr__ with URL
        node = TextNode("Google", TextType.LINK, "https://www.google.com")
        self.assertEqual(repr(node), "TextNode(Google, link, https://www.google.com)")
    
    

    ###
    ###
    #Tests for split_nodes_delimeter

    def test_split_nodes_delimiter_valid(self):
        # Test splitting nodes with a valid delimiter (e.g., '**' for bold)
        
        # Create a list of TextNode objects to pass to the function
        node1 = TextNode("This is **bold** text.", TextType.TEXT)
        nodes = [node1]
        
        # Call the function with '**' as the delimiter and TextType.BOLD as the text_type
        result = split_nodes_delimiter(nodes, '**', TextType.BOLD)

        # Check the result
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_invalid(self):
        # Test that an exception is raised if the number of delimiters is odd
        
        node1 = TextNode("This is **bold text.", TextType.TEXT)  # Invalid because it has an odd number of '**'
        nodes = [node1]

        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(nodes, '**', TextType.BOLD)
        
        self.assertTrue('Invalid Markdown Syntax' in str(context.exception))
    '''
    def test_split_nodes_empty_text(self):
        # Test splitting nodes with an empty string
        node1 = TextNode("", TextType.TEXT)
        nodes = [node1]

        result = split_nodes_delimiter(nodes, '**', TextType.BOLD)

        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(result, expected)
    '''
    def test_split_nodes_no_delimiter(self):
        # Test passing a text with no delimiters
        node1 = TextNode("This is a normal text.", TextType.TEXT)
        nodes = [node1]

        result = split_nodes_delimiter(nodes, '**', TextType.BOLD)

        expected = [TextNode("This is a normal text.", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_at_start(self):
        # Test splitting nodes with a delimiter at the start of the text
        node1 = TextNode("**Bold text** at the begining of the **line**", TextType.TEXT)
        nodes = [node1]

        result = split_nodes_delimiter(nodes, '**', TextType.BOLD)

        expected = [TextNode("Bold text", TextType.BOLD), TextNode(" at the begining of the ", TextType.TEXT), TextNode("line", TextType.BOLD)]
        self.assertEqual(result, expected)

    
    ###
    ###
    #Tests for extract_markdown_images
    def test_single_image(self):
        text = "This is an image ![alt text](image_url.jpg)"
        expected = [("alt text", "image_url.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_multiple_images(self):
        text = "Here are two images: ![first](first_image.jpg) and ![second](second_image.png)"
        expected = [("first", "first_image.jpg"), ("second", "second_image.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_no_images(self):
        text = "This is just text without images."
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_with_special_characters_in_alt_text(self):
        text = "Here is an image ![alt text with *special characters*](image.jpg)"
        expected = [("alt text with *special characters*", "image.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_with_special_characters_in_url(self):
        text = "Here is an image ![alt text](https://example.com/images/image_with_special_chars_%.jpg)"
        expected = [("alt text", "https://example.com/images/image_with_special_chars_%.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_with_empty_alt_text(self):
        text = "This is an image ![](image.jpg)"
        expected = [("", "image.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)


    ###
    ###
    #Tests for extract_markdown_links

    def test_single_link(self):
        text = "This is a link [Google](https://google.com)"
        expected = [("Google", "https://google.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_multiple_links(self):
        text = "Here are two links: [Google](https://google.com) and [GitHub](https://github.com)"
        expected = [("Google", "https://google.com"), ("GitHub", "https://github.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_no_links(self):
        text = "This is just text without links."
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    def test_link_with_special_characters_in_text(self):
        text = "Here is a link to [GitHub with *special characters*](https://github.com)"
        expected = [("GitHub with *special characters*", "https://github.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_link_with_special_characters_in_url(self):
        text = "Here is a link to [Special GitHub](https://github.com/special%25chars)"
        expected = [("Special GitHub", "https://github.com/special%25chars")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_empty_link_text(self):
        text = "This is a link with empty text: [](https://example.com)" 
        expected = [("", "https://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_link_with_extra_exclamation_mark(self):
        text = "This is a non-image link ![example](https://example.com)"
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)
###
###
#Tests for split_nodes_image

    def test_split_images(self):
        node1 = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node1])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_image_single_image(self):
        # Test case where there is a single image in the text
        old_nodes = [TextNode("This is an image ![alt text](http://example.com/image.jpg) and some more text.", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        
        expected_nodes = [
            TextNode("This is an image ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "http://example.com/image.jpg"),
            TextNode(" and some more text.", TextType.TEXT)
        ]
        
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_image_multiple_images(self):
        # Test case with multiple images in the text
        old_nodes = [TextNode("Image 1 ![alt1](http://example.com/image1.jpg) and Image 2 ![alt2](http://example.com/image2.jpg)", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        
        expected_nodes = [
            TextNode("Image 1 ", TextType.TEXT),
            TextNode("alt1", TextType.IMAGE, "http://example.com/image1.jpg"),
            TextNode(" and Image 2 ", TextType.TEXT),
            TextNode("alt2", TextType.IMAGE, "http://example.com/image2.jpg")
        ]
        
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_image_no_image(self):
        # Test case where there are no images in the text
        old_nodes = [TextNode("Just some normal text without any image.", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        
        self.assertEqual(new_nodes, old_nodes)

    def test_split_nodes_image_empty_text(self):
        # Test case where the text is empty
        old_nodes = [TextNode("", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        
        self.assertEqual(new_nodes, old_nodes)

    ###
    ###
    #Tests for split_nodes_link
    
    def test_split_nodes_link_single_link(self):
        # Test case where there is a single link in the text
        old_nodes = [TextNode("This is a link [Google](http://google.com) to search.", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        
        expected_nodes = [
            TextNode("This is a link ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "http://google.com"),
            TextNode(" to search.", TextType.TEXT)
        ]
        
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_link_multiple_links(self):
        # Test case with multiple links in the text
        old_nodes = [TextNode("Visit [Google](http://google.com) or [Yahoo](http://yahoo.com).", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        
        expected_nodes = [
            TextNode("Visit ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "http://google.com"),
            TextNode(" or ", TextType.TEXT),
            TextNode("Yahoo", TextType.LINK, "http://yahoo.com"),
            TextNode(".", TextType.TEXT)
        ]
        
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_link_no_link(self):
        # Test case where there are no links in the text
        old_nodes = [TextNode("Just some normal text without any link.", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        
        self.assertEqual(new_nodes, old_nodes)

    def test_split_nodes_link_empty_text(self):
        # Test case where the text is empty
        old_nodes = [TextNode("", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        
        self.assertEqual(new_nodes, old_nodes)

    def test_split_nodes_image_malformed_markdown(self):
        # Test case where the image markdown is malformed
        old_nodes = [TextNode("This is a malformed image ![alt text(http://example.com/image.jpg)", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        
        # Since it's malformed, we expect the node to remain unchanged
        self.assertEqual(new_nodes, old_nodes)

    def test_split_nodes_link_malformed_markdown(self):
        # Test case where the link markdown is malformed
        old_nodes = [TextNode("This is a malformed link [Google(http://google.com)", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        
        # Since it's malformed, we expect the node to remain unchanged
        self.assertEqual(new_nodes, old_nodes)

###
###
#Tests for text_to_text_nodes

    def test_text_to_text_nodes_bold(self):
        # Test case where text contains bold markdown (**bold**)
        text = "This is **bold** text."
        text_nodes = text_to_text_nodes(text)
        
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT)
        ]
        
        self.assertEqual(text_nodes, expected_nodes)

    def test_text_to_text_nodes_italic(self):
        # Test case where text contains italic markdown (_italic_)
        text = "This is _italic_ text."
        text_nodes = text_to_text_nodes(text)
        
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.TEXT)
        ]
        
        self.assertEqual(text_nodes, expected_nodes)

    def test_text_to_text_nodes_code(self):
        # Test case where text contains code markdown (`code`)
        text = "This is `code` text."
        text_nodes = text_to_text_nodes(text)
        
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text.", TextType.TEXT)
        ]
        
        self.assertEqual(text_nodes, expected_nodes)

    def test_text_to_text_nodes_link(self):
        # Test case where text contains a link markdown ([Google](http://google.com))
        text = "This is a link to [Google](http://google.com)."
        text_nodes = text_to_text_nodes(text)
        
        expected_nodes = [
            TextNode("This is a link to ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "http://google.com"),
            TextNode(".", TextType.TEXT)
        ]
        
        self.assertEqual(text_nodes, expected_nodes)

    def test_text_to_text_nodes_image(self):
        # Test case where text contains an image markdown (![alt text](http://example.com/image.jpg))
        text = "Here is an image ![alt text](http://example.com/image.jpg)."
        text_nodes = text_to_text_nodes(text)
        
        expected_nodes = [
            TextNode("Here is an image ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "http://example.com/image.jpg"),
            TextNode(".", TextType.TEXT)
        ]
        
        self.assertEqual(text_nodes, expected_nodes)

    def test_text_to_text_nodes_combined_formats(self):
        # Test case where text contains bold, italic, code, links, and images together
        text = "This is **bold** and _italic_ with `code`, a [link](http://example.com), and an image ![image](http://example.com/img.jpg)."
        text_nodes = text_to_text_nodes(text)
        
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(", a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "http://example.com"),
            TextNode(", and an image ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "http://example.com/img.jpg"),
            TextNode(".", TextType.TEXT)
        ]
        
        self.assertEqual(text_nodes, expected_nodes)

    def test_text_to_text_nodes_plain_text(self):
        # Test case where there is no formatting, just plain text
        text = "This is just plain text."
        text_nodes = text_to_text_nodes(text)
        
        expected_nodes = [
            TextNode("This is just plain text.", TextType.TEXT)
        ]
        
        self.assertEqual(text_nodes, expected_nodes)

    def test_text_to_text_nodes_empty_text(self):
        # Test case with empty text
        text = ""
        text_nodes = text_to_text_nodes(text)
        
        self.assertEqual(text_nodes, [])

    def test_text_to_text_nodes_malformed_bold(self):
        # Test case with malformed bold markdown (no closing asterisks)
        text = "This is **bold text."
        
        # Expecting an exception to be raised due to malformed bold markdown
        with self.assertRaises(Exception) as context:
            text_nodes = text_to_text_nodes(text)
        
        # Check if the exception message matches our expected message for malformed markdown
        self.assertTrue('Invalid Markdown Syntax' in str(context.exception))
        

    def test_text_to_text_nodes_malformed_link(self):
        # Test case with malformed link markdown (missing closing parenthesis)
        text = "This is a malformed [link(http://example.com"
        text_nodes = text_to_text_nodes(text)
        
        # Since it's malformed, we expect it to be treated as plain text
        expected_nodes = [
            TextNode("This is a malformed [link(http://example.com", TextType.TEXT)
        ]
        
        self.assertEqual(text_nodes, expected_nodes)

###
###
#Tests for markdown_to_blocks

    def test_basic_case(self):
        text = "First block\n\n Second block"
        result = markdown_to_blocks(text)
        self.assertEqual(result, ["First block", "Second block"])

    def test_extra_spaces(self):
        text = "   First block   \n\n   Second block    "
        result = markdown_to_blocks(text)
        self.assertEqual(result, ["First block", "Second block"])

    def test_tab_removal(self):
        text = "First block with a tab:\n    tabbed line\n\nSecond block"
        result = markdown_to_blocks(text)
        self.assertEqual(result, ["First block with a tab:\ntabbed line", "Second block"])

    def test_empty_input(self):
        text = ""
        result = markdown_to_blocks(text)
        self.assertEqual(result, [])

    def test_multiple_paragraphs_with_multiple_newlines(self):
        text = "First block\n\nSecond block\n\nThird block"
        result = markdown_to_blocks(text)
        self.assertEqual(result, ["First block", "Second block", "Third block"])

    def test_no_newline(self):
        text = "No newline input"
        result = markdown_to_blocks(text)
        self.assertEqual(result, ["No newline input"])

    def test_untrimmed_block(self):
        text = "   First block\n\nSecond block"
        result = markdown_to_blocks(text)
        self.assertEqual(result, ["First block", "Second block"])

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
###
###
##Tests for block_to_block_type

    def test_heading_1(self):
        text_block = "# Heading 1"
        result = block_to_block_type(text_block)
        self.assertEqual(result, BlockType.HEADING)

    def test_heading_2(self):
        text_block = "## Heading 2"
        result = block_to_block_type(text_block)
        self.assertEqual(result, BlockType.HEADING)

    def test_code_block(self):
        text_block = "```\nSome code\n```"
        result = block_to_block_type(text_block)
        self.assertEqual(result, BlockType.CODE)

    def test_quote_block(self):
        text_block = "> This is a quote"
        result = block_to_block_type(text_block)
        self.assertEqual(result, BlockType.QUOTE)

    def test_unordered_list(self):
        text_block = "- Item 1\n- Item 2\n- Item 3"
        result = block_to_block_type(text_block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        text_block = "1. First item\n2. Second item\n3. Third item"
        result = block_to_block_type(text_block)
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_paragraph(self):
        text_block = "This is just a normal paragraph."
        result = block_to_block_type(text_block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_mixed_content(self):
        text_block = "# Heading\nSome normal text\n- Unordered list item"
        result = block_to_block_type(text_block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_edge_case_empty_string(self):
        text_block = ""
        result = block_to_block_type(text_block)
        self.assertEqual(result, BlockType.PARAGRAPH)  # Assumption: Empty input is considered a paragraph

    def test_edge_case_code_with_mixed_content(self):
        text_block = "```\nSome code\n- List item\n```"
        result = block_to_block_type(text_block)
        self.assertEqual(result, BlockType.CODE)

    def test_edge_case_invalid_ordered_list(self):
        text_block = "1. First item\n3. Second item\n2. Third item"
        result = block_to_block_type(text_block)
        self.assertEqual(result, BlockType.PARAGRAPH)  # Not a valid ordered list
    
    def test_large_markdown_input(self):
        
        blocks = ['#Main Heading', 'This is a paragraph with some **bold** and *italic* text.', '##Subheading 1',
                   '1. First ordered list item\n2. Second ordered list item\n3. Third ordered list item', '###Subheading 2',
                     '>This is a blockquote.', '```def hello_world():\n    print("Hello, world!")```']
        expected_block_types = [
            BlockType.HEADING,   # # Main Heading
            BlockType.PARAGRAPH, # Paragraph with **bold** and *italic* text
            BlockType.HEADING,   # ## Subheading 1
            BlockType.ORDERED_LIST,  # Ordered list
            BlockType.HEADING,   # ### Subheading 2
            BlockType.QUOTE,     # Blockquote
            BlockType.CODE,      # Code block
            
        ]

        for i, block in enumerate(blocks):
            result = block_to_block_type(block)
            self.assertEqual(result, expected_block_types[i])


###
###
##Tests for markdown_to_html_node 

    def test_paragraphs(self):
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



    def test_blockquote(self):
        md = """
            >This is a blockquote
            >that spans multiple lines.
            """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote that spans multiple lines.</blockquote></div>",
        )

    def test_ordered_list(self):
        md = """
            1. Item 1
            2. Item 2
            3. Item 3
            """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol></div>",
        )

    def test_unordered_list(self):
        md = """
            - Item 1
            - Item 2
            - Item 3
            """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>",
        )

    def test_heading(self):
        md = """
            # Heading 1

            ## Heading 2

            ### Heading 3
            """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>",
        )



if __name__ == "__main__":
    unittest.main()