# -*- coding: utf8 -*-

from mediawiki_parser.tests import ParserTestCase


class ParagraphsTests(ParserTestCase):
    def test_single_line_paragraph(self):
        source = "This is a paragraph.\n"
        result = """body:
   paragraphs:
      paragraph:
         raw_text:This is a paragraph."""
        self.parsed_equal_tree(source, result, None)

    def test_multi_line_paragraph(self):
        source = """This is a paragraph.
With a newline in the middle.
"""
        result = """body:
   paragraphs:
      paragraph:
         paragraph_line:
            raw_text:This is a paragraph.
         paragraph_line:
            raw_text:With a newline in the middle."""
        self.parsed_equal_tree(source, result, None)

    def test_2_paragraphs(self):
        source = """This is a paragraph.

Followed by another one.
"""
        result = """body:
   paragraphs:
      paragraph:
         raw_text:This is a paragraph.
      paragraph:
         raw_text:Followed by another one."""
        self.parsed_equal_tree(source, result, None)

    def test_blank_line_in_paragraphs(self):
        source = """This is a paragraph.


Followed a blank line and another paragraph.
"""
        result = """body:
   paragraphs:
      paragraph:
         raw_text:This is a paragraph.
      blank_paragraph:
      paragraph:
         raw_text:Followed a blank line and another paragraph."""
        self.parsed_equal_tree(source, result, None)

    def test_styled_text_in_paragraph(self):
        source = """Styled text such as ''italic'', '''bold''', {{templates}} and {{{template parameters}}} also work.
"""
        result = """body:
   paragraphs:
      paragraph:
         raw_text:Styled text such as ''italic'', '''bold''', 
         internal_link:Template:templates
         raw_text: and 
         allowed_char:{
         allowed_char:{
         allowed_char:{
         raw_text:template parameters
         allowed_char:}
         allowed_char:}
         allowed_char:}
         raw_text: also work."""
        self.parsed_equal_tree(source, result, None)
