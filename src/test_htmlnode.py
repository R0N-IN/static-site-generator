import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):

    def test_eq(self):
        node = HTMLNode("h1","this is a value", [], {})
        node2 = HTMLNode("h1","this is a value", [], {})
        self.assertEqual(node, node2)
  
    def test_neq(self): 
        node = HTMLNode("h1", "This is a different value", [], {})
        node2 = HTMLNode("h1","this is a value", [], {})
        self.assertNotEqual(node, node2)
   
    def test_eq_tag(self):
        node = HTMLNode("a","This is a value", [], {})
        node2 = HTMLNode("a","This is a value", [], {})
        self.assertEqual(node, node2)
   
    def test_neq_tag(self):
        node = HTMLNode("p", "This is a value", [], {})
        node2 = HTMLNode("h1", "This is a value", [], {})
        self.assertNotEqual(node, node2)    
    
    def test_eq_value(self):
        node = HTMLNode("h1", "This is a value", [], {})
        node2 = HTMLNode("h1", "This is a value", [], {})
        self.assertEqual(node,node2)
    
    def test_neq_value(self):
        node = HTMLNode("h1", "This isn't a different value", [], {})
        node2 = HTMLNode("h1", "This is a different value", [], {})
        self.assertNotEqual(node, node2)
   
    def test_eq_children(self):
        node = HTMLNode("h1", "This is a value", [HTMLNode("p","This is a child", [], {})], {})
        node2 = HTMLNode("h1", "This is a value", [HTMLNode("p","This is a child", [], {})], {})
        self.assertEqual(node, node2)
   
    def test_neq_children(self):
        node = HTMLNode("h1", "This is a value", [HTMLNode("p","This is a child", [], {})], {})
        node2 = HTMLNode("h1", "This is a value", [HTMLNode("p","This is a different child", [], {})], {})
        self.assertNotEqual(node, node2)
   
    def test_eq_props(self):
        node = HTMLNode("h1", "This is a value", [], {"class":"header"})
        node2 = HTMLNode("h1", "This is a value", [], {"class":"header"})
        self.assertEqual(node, node2)
   
    def test_neq_props(self):
        node = HTMLNode("h1", "This is a value", [], {"class":"header"})    
        node2 = HTMLNode("h1", "This is a value", [], {"class":"footer"})
        self.assertNotEqual(node, node2)
    
    def test_neq_props2(self):
        node = HTMLNode("h1", "This is a value", [], {"class":"header"})
        node2 = HTMLNode("h1", "This is a value", [], {})
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()