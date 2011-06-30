# -*- coding: utf8 -*-

from mediawiki_parser.tests import ParserTestCase


class Paragraphs_tests(ParserTestCase):
    def test_single_line_paragraph(self):
        source = "This is a paragraph.\n"
        result = """body:
   paragraphs:
      paragraph:
         rawText:This is a paragraph."""
        self.parsed_equal_tree(source, result, None)

    def test_multi_line_paragraph(self):
        source = """This is a paragraph.
With a newline in the middle.
"""
        result = """body:
   paragraphs:
      paragraph:
         paragraph_line:
            rawText:This is a paragraph.
         paragraph_line:
            rawText:With a newline in the middle."""
        self.parsed_equal_tree(source, result, None)

    def test_2_paragraphs(self):
        source = """This is a paragraph.

Followed by another one.
"""
        result = """body:
   paragraphs:
      paragraph:
         rawText:This is a paragraph.
      paragraph:
         rawText:Followed by another one."""
        self.parsed_equal_tree(source, result, None)

    def test_blank_line_in_paragraphs(self):
        source = """This is a paragraph.


Followed a blank line and another paragraph.
"""
        result = """body:
   paragraphs:
      paragraph:
         rawText:This is a paragraph.
      blank_paragraph:
      paragraph:
         rawText:Followed a blank line and another paragraph."""
        self.parsed_equal_tree(source, result, None)

    def test_styled_text_in_paragraph(self):
        source = """Styled text such as ''italic'', '''bold''', {{templates}} also work.
"""
        result = """body:
   paragraphs:
      paragraph:
         rawText:Styled text such as <em>italic</em>, <strong>bold</strong>, 
         template:
            page_name:templates
         rawText: also work."""
        self.parsed_equal_tree(source, result, None)
