# -*- coding: utf8 -*-

from mediawiki_parser.tests import ParserTestCase


class NowikiTests(ParserTestCase):
    def test_nowiki_section(self):
        source = '<nowiki>some [[text]] that should {{not}} be changed</nowiki>\n'
        result = "[paragraphs:[paragraph:[nowiki:'some [[text]] that should {{not}} be changed']]]"
        self.parsed_equal_string(source, result, None)

    def test_nested_nowiki(self):
        # This looks weird but is the actual behavior of MediaWiki
        source = '<nowiki>some [[text]] <nowiki>that should </nowiki>{{not}} be changed</nowiki>\n'
        result = "[paragraphs:[paragraph:[nowiki:'some [[text]] <nowiki>that should '  internal_link:'Template:not'  raw_text:' be changed'  tag_close:[tag_name:'nowiki']]]]"
        self.parsed_equal_string(source, result, None)

    def test_multiline_nowiki(self):
        source = """some <nowiki> [[text]] that

should {{not}} be </nowiki> changed
"""
        result = "[paragraphs:[paragraph:[raw_text:'some '  nowiki:' [[text]] that should {{not}} be '  raw_text:' changed']]]"
        self.parsed_equal_string(source, result, None)
