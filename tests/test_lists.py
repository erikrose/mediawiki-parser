# -*- coding: utf8 -*-

from mediawiki_parser.tests import ParserTestCase


class ListsTests(ParserTestCase):
    def test_1_bullet_list(self):
        source = '* text\n'
        result = "[list:[bullet_list_leaf:[raw_text:' text']]]"
        self.parsed_equal_string(source, result, None)

    def test_2_bullet_list(self):
        source = '** other text\n'
        result = "[list:[@bullet_sub_list@:[bullet_list_leaf:[raw_text:' other text']]]]"
        self.parsed_equal_string(source, result, None)

    def test_3_bullet_list(self):
        source = '*** other text\n'
        result = "[list:[@bullet_sub_list@:[@bullet_sub_list@:[bullet_list_leaf:[raw_text:' other text']]]]]"
        self.parsed_equal_string(source, result, None)

    def test_1_hash_list(self):
        source = '# text\n'
        result = "[list:[number_list_leaf:[raw_text:' text']]]"
        self.parsed_equal_string(source, result, None)

    def test_2_hash_list(self):
        source = "## more text\n"
        result = "[list:[@number_sub_list@:[number_list_leaf:[raw_text:' more text']]]]"
        self.parsed_equal_string(source, result, None)

    def test_3_hash_list(self):
        source = "### ''other text''\n"
        result = "[list:[@number_sub_list@:[@number_sub_list@:[number_list_leaf:[raw_text:' \'\'other text\'\'']]]]]"
        self.parsed_equal_string(source, result, None)

    def test_1_colon_list(self):
        source = ": more text\n"
        result = "[list:[colon_list_leaf:[raw_text:' more text']]]"
        self.parsed_equal_string(source, result, None)

    def test_4_colon_list(self):
        source = ":::: more {{text}}!\n"
        result = "[list:[@colon_sub_list@:[@colon_sub_list@:[@colon_sub_list@:[colon_list_leaf:[raw_text:' more words!']]]]]]"
        templates = {'text': 'words'}
        self.parsed_equal_string(source, result, None, templates)

    def test_1_semicolon_list(self):
        source = '; still more [[text]]\n'
        result = "[list:[semi_colon_list_leaf:[raw_text:' still more '  internal_link:'text']]]"
        self.parsed_equal_string(source, result, None)

    def test_2_semicolon_list(self):
        source = ';; still more [[text]]\n'
        result = "[list:[@semi_colon_sub_list@:[semi_colon_list_leaf:[raw_text:' still more '  internal_link:'text']]]]"
        self.parsed_equal_string(source, result, None)

    def test_1_colon_1_bullet_list(self):
        source = ':* more complicated case\n'
        result = "[list:[@colon_sub_list@:[bullet_list_leaf:[raw_text:' more complicated case']]]]"
        self.parsed_equal_string(source, result, None)

    def test_1_semicolon_1_bullet_list(self):
        source = ';* same as previous line\n'
        result = "[list:[@semi_colon_sub_list@:[bullet_list_leaf:[raw_text:' same as previous line']]]]"
        self.parsed_equal_string(source, result, None)

    def test_2_semicolon_2_bullet_list(self):
        source = '::** another complicated case\n'
        result = "[list:[@colon_sub_list@:[@colon_sub_list@:[@bullet_sub_list@:[bullet_list_leaf:[raw_text:' another complicated case']]]]]]"
        self.parsed_equal_string(source, result, None)

    def test_composed_list(self):
        source = "*:*;#*: this is {{correct}} syntax!\n"
        result = "[list:[@bullet_sub_list@:[@colon_sub_list@:[@bullet_sub_list@:[@semi_colon_sub_list@:[@number_sub_list@:[@bullet_sub_list@:[colon_list_leaf:[raw_text:' this is '  internal_link:'Template:correct'  raw_text:' syntax!']]]]]]]]]"
        self.parsed_equal_string(source, result, None)

    def test_multiline_bullet_list(self):
        source = """* This example...
** shows the shape...
*** of the resulting ...
** AST
"""
        result = """body:
   list:
      bullet_list_leaf:
         raw_text: This example...
      @bullet_sub_list@:
         bullet_list_leaf:
            raw_text: shows the shape...
      @bullet_sub_list@:
         @bullet_sub_list@:
            bullet_list_leaf:
               raw_text: of the resulting ...
      @bullet_sub_list@:
         bullet_list_leaf:
            raw_text: AST"""
        self.parsed_equal_tree(source, result, None)

    def test_list_with_template_produces_single_list(self):
        source = """* This example...
{{template}}
*it...
"""
        result = """body:
   list:
      bullet_list_leaf:
         raw_text: This example...
      bullet_list_leaf:
         raw_text: checks
      bullet_list_leaf:
         raw_text:it..."""
        templates = {'template': '* checks'}
        self.parsed_equal_tree(source, result, None, templates)
