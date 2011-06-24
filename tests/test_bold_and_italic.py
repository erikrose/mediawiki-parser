# -*- coding: utf8 -*-

from mediawiki_parser.tests import ParserTestCase


class Bold_and_italic_tests(ParserTestCase):
    def test_italic(self):
        source = "Here, we have ''italic'' text."
        result = "[rawText:'Here, we have <em>italic</em> text.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_bold(self):
        source = "Here, we have '''bold''' text."
        result = "[rawText:'Here, we have <strong>bold</strong> text.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_bold_and_italic_case1(self):
        source = "Here, we have '''''bold and italic''''' text."
        result = "[rawText:'Here, we have <em><strong>bold and italic</strong></em> text.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_bold_italic_case2(self):
        source = "Here, we have ''italic only and '''bold and italic''''' text."
        result = "[rawText:'Here, we have <em>italic only and <strong>bold and italic</strong></em> text.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_bold_italic_case3(self):
        source = "Here, we have '''bold only and ''bold and italic''''' text."
        result = "[rawText:'Here, we have <strong>bold only and <em>bold and italic</em></strong> text.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_bold_italic_case4(self):
        source = "Here, we have '''''bold and italic''' and italic only''."
        result = "[rawText:'Here, we have <em><strong>bold and italic</strong> and italic only</em>.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_bold_italic_case5(self):
        source = "Here, we have '''''bold and italic'' and bold only'''."
        result = "[rawText:'Here, we have <strong><em>bold and italic</em> and bold only</strong>.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_bold_italic_case6(self):
        source = "Here, we have ''italic, '''bold and italic''' and italic only''."
        result = "[rawText:'Here, we have <em>italic, <strong>bold and italic</strong> and italic only</em>.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_bold_italic_case7(self):
        source = "Here, we have '''bold, ''bold and italic'' and bold only'''."
        result = "[rawText:'Here, we have <strong>bold, <em>bold and italic</em> and bold only</strong>.']"
        self.parsed_equal_string(source, result, 'inline')
