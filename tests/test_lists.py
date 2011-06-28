# -*- coding: utf8 -*-

from mediawiki_parser.tests import ParserTestCase


class Lists_tests(ParserTestCase):
    def test_1_bullet_list(self):
        source = '* text\n'
        result = "[list:[bulletListLeaf:[rawText:' text']]]"
        self.parsed_equal_string(source, result, None)

    def test_1_bullet_list(self):
        source = '** other text\n'
        result = "[list:[@bulletSubList@:[bulletListLeaf:[rawText:' other text']]]]"
        self.parsed_equal_string(source, result, None)

    def test_1_bullet_list(self):
        source = '*** other text\n'
        result = "[list:[@bulletSubList@:[@bulletSubList@:[bulletListLeaf:[rawText:' other text']]]]]"
        self.parsed_equal_string(source, result, None)

    def test_1_bullet_list(self):
        source = '# text\n'
        result = "[list:[numberListLeaf:[rawText:' text']]]"
        self.parsed_equal_string(source, result, None)

    def test_1_bullet_list(self):
        source = "## ''more text''\n"
        result = "[list:[@numberSubList@:[numberListLeaf:[rawText:' <em>more text</em>']]]]"
        self.parsed_equal_string(source, result, None)

    def test_1_bullet_list(self):
        source = "### ''other text''\n"
        result = "[list:[@numberSubList@:[@numberSubList@:[numberListLeaf:[rawText:' <em>other text</em>']]]]]"
        self.parsed_equal_string(source, result, None)

    def test_1_bullet_list(self):
        source = ": '''more text'''\n"
        result = "[list:[colonListLeaf:[rawText:' <strong>more text</strong>']]]"
        self.parsed_equal_string(source, result, None)

    def test_1_bullet_list(self):
        source = ":::: '''more text'''\n"
        result = "[list:[@colonSubList@:[@colonSubList@:[@colonSubList@:[colonListLeaf:[rawText:' <strong>more text</strong>']]]]]]"
        self.parsed_equal_string(source, result, None)

    def test_1_bullet_list(self):
        source = '; still more [[text]]\n'
        result = "[list:[semiColonListLeaf:[rawText:' still more '  internal_link:'text']]]"
        self.parsed_equal_string(source, result, None)

    def test_1_bullet_list(self):
        source = ';; still more [[text]]\n'
        result = "[list:[@semiColonSubList@:[semiColonListLeaf:[rawText:' still more '  internal_link:'text']]]]"
        self.parsed_equal_string(source, result, None)

    def test_1_bullet_list(self):
        source = ':* more complicated case\n'
        result = "[list:[@colonSubList@:[bulletListLeaf:[rawText:' more complicated case']]]]"
        self.parsed_equal_string(source, result, None)

    def test_1_bullet_list(self):
        source = ';* same as previous line\n'
        result = "[list:[@semiColonSubList@:[bulletListLeaf:[rawText:' same as previous line']]]]"
        self.parsed_equal_string(source, result, None)

    def test_1_bullet_list(self):
        source = '::** another complicated case\n'
        result = "[list:[@colonSubList@:[@colonSubList@:[@bulletSubList@:[bulletListLeaf:[rawText:' another complicated case']]]]]]"
        self.parsed_equal_string(source, result, None)

    def test_1_bullet_list(self):
        source = "*:*;#*: this is '''correct''' syntax!\n"
        result = "[list:[@bulletSubList@:[@colonSubList@:[@bulletSubList@:[@semiColonSubList@:[@numberSubList@:[@bulletSubList@:[colonListLeaf:[rawText:' this is <strong>correct</strong> syntax!']]]]]]]]]"
        self.parsed_equal_string(source, result, None)

    def test_1_bullet_list(self):
        source = """* This example...
** shows the shape...
*** of the resulting ...
** AST
"""
        result = """body:
   list:
      bulletListLeaf:
         rawText: This example...
      @bulletSubList@:
         bulletListLeaf:
            rawText: shows the shape...
      @bulletSubList@:
         @bulletSubList@:
            bulletListLeaf:
               rawText: of the resulting ...
      @bulletSubList@:
         bulletListLeaf:
            rawText: AST"""
        self.parsed_equal_tree(source, result, None)
