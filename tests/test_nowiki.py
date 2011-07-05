# -*- coding: utf8 -*-

from mediawiki_parser.tests import ParserTestCase


class Nowiki_tests(ParserTestCase):
    def test_nowiki_section(self):
        source = '<nowiki>some [[text]] that should {{not}} be changed</nowiki>\n'
        result = "[paragraphs:[paragraph:[nowiki:'some [[text]] that should {{not}} be changed']]]"
        self.parsed_equal_string(source, result, None)

    def test_nested_nowiki(self):
        # This looks weird but is the actual behavior of MediaWiki
        source = '<nowiki>some [[text]] <nowiki>that should </nowiki>{{not}} be changed</nowiki>\n'
        result = "[paragraphs:[paragraph:[nowiki:'some [[text]] <nowiki>that should '  template:[page_name:'not']  rawText:' be changed'  tag_close:[tag_name:'nowiki']]]]"
        self.parsed_equal_string(source, result, None)

    def test_multiline_nowiki(self):
        source = """some <nowiki> [[text]] that

should {{not}} be </nowiki> changed
"""
        result = "[paragraphs:[paragraph:[rawText:'some '  nowiki:' [[text]] that should {{not}} be '  rawText:' changed']]]"
        self.parsed_equal_string(source, result, None)
