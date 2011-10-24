# -*- coding: utf8 -*-

from mediawiki_parser.tests import ParserTestCase


class CommentsTests(ParserTestCase):
    def test_comment_before_title(self):
        source = '<!-- comment -->=Title 1=\n'
        result = "[title1:[raw_text:'Title 1']]"
        self.parsed_equal_string(source, result, None)

    def test_comment_before_preformatted_paragraph(self):
        source = "<!-- comment --> This is a preformatted paragraph.\n"
        result = """body:
   preformatted_lines:
      preformatted_line:
         preformatted_inline:
            raw_text:This is a preformatted paragraph.
         EOL_KEEP:
"""
        self.parsed_equal_tree(source, result, None)

    def test_comment_before_list(self):
        source = '<!--comment\n-->* text\n'
        result = "[list:[bullet_list_leaf:[raw_text:' text']]]"
        self.parsed_equal_string(source, result, None)

    def test_comment_inside_list(self):
        source = '*<!--comment---->** other text\n'
        result = "[list:[@bullet_sub_list@:[@bullet_sub_list@:[bullet_list_leaf:[raw_text:' other text']]]]]"
        self.parsed_equal_string(source, result, None)

    def test_comment_inside_paragraph(self):
        source = "This is a<!-- this is an HTML \t\n comment --> paragraph.\n"
        result = """body:
   paragraphs:
      paragraph:
         raw_text:This is a paragraph."""
        self.parsed_equal_tree(source, result, None)

    def test_empty_comment(self):
        source = 'an <!----> empty comment'
        result = "[raw_text:'an  empty comment']"
        self.parsed_equal_string(source, result, 'inline')

    def test_special_chars_in_comment(self):
        source = u'a <!--\n\t你好--> comment'
        result = "[raw_text:'a  comment']"
        self.parsed_equal_string(source, result, 'inline')
