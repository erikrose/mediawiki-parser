# -*- coding: utf8 -*-

from mediawiki_parser.tests import ParserTestCase


class preformatted_paragraphsTests(ParserTestCase):
    def test_single_line_paragraph(self):
        source = " This is a preformatted paragraph.\n"
        result = """body:
   preformatted_lines:
      preformatted_line:
         @inline@:
            raw_text:This is a preformatted paragraph.
         EOL_KEEP:
"""
        self.parsed_equal_tree(source, result, None)

    def test_preformatted_and_normal_paragraphs(self):
        source = """ This is a preformatted paragraph.
Followed by a "normal" one.
"""
        result = """body:
   preformatted_lines:
      preformatted_line:
         @inline@:
            raw_text:This is a preformatted paragraph.
         EOL_KEEP:

   paragraphs:
      paragraph:
         raw_text:Followed by a "normal" one."""
        self.parsed_equal_tree(source, result, None)

    def test_multiline_paragraph(self):
        source = """ This is a multiline
 preformatted paragraph.
"""
        result = """body:
   preformatted_lines:
      preformatted_line:
         @inline@:
            raw_text:This is a multiline
         EOL_KEEP:

      preformatted_line:
         @inline@:
            raw_text:preformatted paragraph.
         EOL_KEEP:
"""
        self.parsed_equal_tree(source, result, None)

    def test_style_in_preformatted_paragraph(self):
        source = """ Styled text such as ''italic'', '''bold''', {{templates}} also work.
"""
        result = """body:
   preformatted_lines:
      preformatted_line:
         @inline@:
            raw_text:Styled text such as <em>italic</em>, <strong>bold</strong>, 
            internal_link:Template:templates
            raw_text: also work.
         EOL_KEEP:
"""
        self.parsed_equal_tree(source, result, None)

    def test_html_pre_paragraph(self):
        source = """<pre>
Preformatted paragraph.
</pre>
"""
        result = """body:
   preformatted_paragraph:
      preformatted_text:
         raw_text:Preformatted paragraph."""
        self.parsed_equal_tree(source, result, None)

    def test_formatted_html_pre_paragraph(self):
        # <pre> should act like <nowiki>
        source = "<pre>some [[text]] that should {{not}} be changed</pre>\n"
        result = "[paragraphs:[paragraph:[preformatted:'some [[text]] that should {{not}} be changed']]]"
        self.parsed_equal_string(source, result, None)

    def test_html_pre_in_paragraph(self):
        source = "Normal paragraph <pre>Preformatted one</pre> Normal one.\n"
        result = """body:
   paragraphs:
      paragraph:
         raw_text:Normal paragraph 
         preformatted:Preformatted one
         raw_text: Normal one."""
        self.parsed_equal_tree(source, result, None)

    def test_pre_paragraph_in_table(self):
        source = """{|
|-
! <pre>Text</pre>
|}
"""
        result = """body:
   table:
      table_line_break:
      table_line_header:
         @clean_inline@:
            raw_text: 
            preformatted:Text"""
        self.parsed_equal_tree(source, result, None)
