# -*- coding: utf8 -*-

from mediawiki_parser.tests import ParserTestCase


class Nowiki_tests(ParserTestCase):
    def test_nowiki_section(self):
        source = '<nowiki>some [[text]] that should {{not}} be changed</nowiki>\n'
        result = "[paragraphs:[paragraph:[nowiki:'some [[text]] that should {{not}} be changed']]]"
        self.parsed_equal_string(source, result, None)
