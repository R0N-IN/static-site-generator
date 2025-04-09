import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):

    def test_initialization(self):
        # Test the LeafNode initialization with a dictionary for props
        leaf = LeafNode("p", "Hello", {'class': 'text'})
        self.assertEqual(leaf.tag, "p")
        self.assertEqual(leaf.value, "Hello")
        self.assertEqual(leaf.props, {'class': 'text'})

    def test_to_html_with_tag_and_props(self):
        # Test to_html method with a tag and props
        leaf = LeafNode("p", "Hello", {'class': 'text'})
        html = leaf.to_html()
        self.assertEqual(html, '<p class="text">Hello</p>')

    def test_to_html_without_tag(self):
        # Test to_html method without a tag (i.e., when tag is None)
        leaf = LeafNode(None, "Hello", {})
        html = leaf.to_html()
        self.assertEqual(html, "Hello")

    def test_to_html_without_value(self):
        # Test to_html method when value is None (should raise ValueError)
        leaf = LeafNode("p", None, {})
        with self.assertRaises(ValueError):
            leaf.to_html()

    def test_equality_equal_objects(self):
        # Test equality method with equal LeafNode objects
        leaf1 = LeafNode("p", "Hello", {'class': 'text'})
        leaf2 = LeafNode("p", "Hello", {'class': 'text'})
        self.assertTrue(leaf1 == leaf2)

    def test_equality_different_tag(self):
        # Test equality method with different tags
        leaf1 = LeafNode("p", "Hello", {'class': 'text'})
        leaf2 = LeafNode("div", "Hello", {'class': 'text'})
        self.assertFalse(leaf1 == leaf2)

    def test_equality_different_value(self):
        # Test equality method with different values
        leaf1 = LeafNode("p", "Hello", {'class': 'text'})
        leaf2 = LeafNode("p", "Goodbye", {'class': 'text'})
        self.assertFalse(leaf1 == leaf2)

    def test_equality_different_props(self):
        # Test equality method with different props
        leaf1 = LeafNode("p", "Hello", {'class': 'text'})
        leaf2 = LeafNode("p", "Hello", {'class': 'other'})
        self.assertFalse(leaf1 == leaf2)

    def test_repr(self):
        # Test __repr__ method
        leaf = LeafNode("p", "Hello", {'class': 'text'})
        self.assertEqual(repr(leaf), "LeafNode(p, Hello, {'class': 'text'})")

if __name__ == "__main__":
    unittest.main()

        