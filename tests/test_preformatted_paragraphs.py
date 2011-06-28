# -*- coding: utf8 -*-

from mediawiki_parser.tests import ParserTestCase


class Paragraphs_tests(ParserTestCase):
    def test_single_line_paragraph(self):
        source = " This is a preformatted paragraph.\n"
        result = """body:
   preformattedLines:
      preformattedLine:
         rawText:This is a preformatted paragraph."""
        self.parsed_equal_tree(source, result, None)

    def test_preformatted_and_normal_paragraphs(self):
        source = """ This is a preformatted paragraph.
Followed by a "normal" one.
"""
        result = """body:
   preformattedLines:
      preformattedLine:
         rawText:This is a preformatted paragraph.
   paragraphs:
      paragraph:
         rawText:Followed by a "normal" one."""
        self.parsed_equal_tree(source, result, None)

    def test_multiline_paragraph(self):
        source = """ This is a multiline
 preformatted paragraph.
"""
        result = """body:
   preformattedLines:
      preformattedLine:
         rawText:This is a multiline
      preformattedLine:
         rawText:preformatted paragraph."""
        self.parsed_equal_tree(source, result, None)

    def test_style_in_paragraph(self):
        source = """ Styled text such as ''italic'', '''bold''', {{templates}} also work.
"""
        result = """body:
   preformattedLines:
      preformattedLine:
         rawText:Styled text such as <em>italic</em>, <strong>bold</strong>, 
         template:
            page_name:templates
         rawText: also work."""
        self.parsed_equal_tree(source, result, None)

    def test_html_pre_paragraph(self):
        source = """<pre>
Preformatted paragraph.
</pre>
"""
        result = """body:
   preformattedParagraph:
      preformattedText:
         rawText:Preformatted paragraph."""
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
         rawText:Normal paragraph 
         preformatted:Preformatted one
         rawText: Normal one."""
        self.parsed_equal_tree(source, result, None)

    def test_pre_paragraph_in_table(self):
        source = """{|
|-
! <pre>Text</pre>
|}
"""
        result = """body:
   @wikiTable@:
      <?>:

      <?>:
         wikiTableLine:
            wikiTableLineBreak:
         wikiTableLine:
            wikiTableLineHeader:
               @cleanInline@:
                  rawText: 
                  preformatted:Text"""
        self.parsed_equal_tree(source, result, None)
