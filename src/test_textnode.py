import unittest
from textnode import *


class TestTextNode(unittest.TestCase):

    
    def test_initialization(self):
        # Test the TextNode initialization without URL
        node = TextNode("Hello", TextType.TEXT)
        self.assertEqual(node.text, "Hello")
        self.assertEqual(node.text_type, TextType.TEXT)
        self.assertIsNone(node.url)

    def test_initialization_with_url(self):
        # Test TextNode initialization with URL
        node = TextNode("Google", TextType.LINK, "https://www.google.com")
        self.assertEqual(node.text, "Google")
        self.assertEqual(node.text_type, TextType.LINK)
        self.assertEqual(node.url, "https://www.google.com")

    def test_eq_same_values(self):
        # Test equality method with equal TextNode objects
        node1 = TextNode("Hello", TextType.TEXT)
        node2 = TextNode("Hello", TextType.TEXT)
        self.assertTrue(node1 == node2)

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



if __name__ == "__main__":
    unittest.main()


### Not handling properly the case when multiple delimeters are present in the text
