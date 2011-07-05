# -*- coding: utf8 -*-

from mediawiki_parser.tests import ParserTestCase


class Rules_tests(ParserTestCase):
    def test_simple_rule(self):
        source = '----\n'
        result = "[horizontal_rule:'']"
        self.parsed_equal_string(source, result, None)

    def test_rule_too_short(self):
        # In this case, it is a paragraph!
        source = '---\n'
        result = "[paragraphs:[paragraph:[rawText:'---']]]"
        self.parsed_equal_string(source, result, None)

    def test_rule_too_long(self):
        # In this case, it is a paragraph!
        source = '----\n'
        result = "[horizontal_rule:'']"
        self.parsed_equal_string(source, result, None)

    def test_inline_after_rule(self):
        # In this case, it is a paragraph!
        source = '------ {{template|arg=[[link]]}}\n'
        result = "[horizontal_rule:[@inline@:[rawText:' '  template:[page_name:'template'  parameters:[parameter:[parameter_name:'arg'  optional_value:[internal_link:'link']]]]]]]"
        self.parsed_equal_string(source, result, None)
