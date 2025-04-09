import unittest
from create_page import *


class TestCreatePage(unittest.TestCase):
    ###
    ###
    ##Tests for extract_title 

        def test_extract_title(self):
            md = "# Title of the Document\n\nThis is the content."
            title = extract_title(md)
            self.assertEqual(title, "Title of the Document")
            
        def test_no_title(self):
            md = "This is the content without a title."
            with self.assertRaises(Exception):       
                extract_title(md)

        def test_empty_string(self):
            md = ""
            with self.assertRaises(Exception):       
                extract_title(md)

        def test_title_with_special_characters(self):
            md = "# Title with special characters: @#$%^&*\n\nContent here."
            title = extract_title(md)
            self.assertEqual(title, "Title with special characters: @#$%^&*")

        def test_title_with_newline(self):
            md = "# Title\n\nThis is the content."
            title = extract_title(md)
            self.assertEqual(title, "Title")

        def test_multiple_titles(self):
            md = "# First Title\n# Second Title\n\nContent here."
            title = extract_title(md)
            self.assertEqual(title, "First Title")

        def test_title_with_leading_spaces(self):
            md = "   # Title with leading spaces\n\nContent here."
            title = extract_title(md)
            self.assertEqual(title, "Title with leading spaces")

        def test_title_with_trailing_spaces(self):
            md = "# Title with trailing spaces   \n\nContent here."
            title = extract_title(md)
            self.assertEqual(title, "Title with trailing spaces")


if __name__ == "__main__":
    unittest.main()