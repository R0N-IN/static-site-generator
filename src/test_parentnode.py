import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):

    def test_initialization(self):
        # Test the ParentNode initialization without props
        parent = ParentNode("div", [])
        self.assertEqual(parent.tag, "div")
        self.assertEqual(parent.children, [])
        self.assertIsNone(parent.props)

    def test_initialization_with_props(self):
        # Test ParentNode initialization with props
        parent = ParentNode("div", [], {'class': 'container'})
        self.assertEqual(parent.props, {'class': 'container'})

    def test_to_html_empty_children(self):
        # Test to_html raises error if children is None
        parent = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_html_no_tag(self):
        # Test to_html raises error if tag is None
        parent = ParentNode(None, [])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_html_basic(self):
        # Test to_html method with a basic parent node and one child
        child = LeafNode("span", "text")
        parent = ParentNode("div", [child])
        html = parent.to_html()
        self.assertEqual(html, "<div><span>text</span></div>")

    def test_to_html_with_props(self):
        # Test to_html method with props for ParentNode
        child = LeafNode("span", "text")
        parent = ParentNode("div", [child], {"class": "container"})
        html = parent.to_html()
        self.assertEqual(html, '<div class="container"><span>text</span></div>')

    def test_to_html_multiple_children(self):
        # Test to_html method with multiple children
        child1 = LeafNode("span", "text1")
        child2 = LeafNode("span", "text2")
        parent = ParentNode("div", [child1, child2])
        html = parent.to_html()
        self.assertEqual(html, "<div><span>text1</span><span>text2</span></div>")

    def test_equality_equal_objects(self):
        # Test equality method with equal ParentNode objects
        child1 = LeafNode("span", "text")
        parent1 = ParentNode("div", [child1])
        parent2 = ParentNode("div", [child1])
        self.assertTrue(parent1 == parent2)

    def test_equality_different_tag(self):
        # Test equality method with different tags
        child1 = LeafNode("span", "text")
        parent1 = ParentNode("div", [child1])
        parent2 = ParentNode("p", [child1])
        self.assertFalse(parent1 == parent2)

    def test_equality_different_children(self):
        # Test equality method with different children
        child1 = LeafNode("span", "text1")
        child2 = LeafNode("span", "text2")
        parent1 = ParentNode("div", [child1])
        parent2 = ParentNode("div", [child2])
        self.assertFalse(parent1 == parent2)

    def test_repr(self):
        # Test __repr__ method for ParentNode
        child = LeafNode("span", "text")
        parent = ParentNode("div", [child])
        self.assertEqual(repr(parent), "ParentNode(div, [LeafNode(span, text, None)], None)")