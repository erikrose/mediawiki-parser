# -*- coding: utf8 -*-

from mediawiki_parser import wikitextParser
mediawikiParser = wikitextParser.wikitextParser

from unittest import TestCase


class NowikiTests(TestCase):
    def test_italic(self):
        test_suite_dict = {
                "Here, we have ''italic'' text.": "[rawText:'Here, we have <em>italic</em> text.']"
        }
        mediawikiParser.inline.testSuite(test_suite_dict)

    def test_bold(self):
        test_suite_dict = {
                "Here, we have '''bold''' text." : "[rawText:'Here, we have <strong>bold</strong> text.']"
        }
        mediawikiParser.inline.testSuite(test_suite_dict)

    def test_bold_and_italic_case1(self):
        test_suite_dict = {
                "Here, we have '''''bold and italic''''' text.": "[rawText:'Here, we have <em><strong>bold and italic</strong></em> text.']"
        }
        mediawikiParser.inline.testSuite(test_suite_dict)

    def test_bold_italic_case2(self):
        test_suite_dict = {
                "Here, we have ''italic only and '''bold and italic''''' text.": "[rawText:'Here, we have <em>italic only and <strong>bold and italic</strong></em> text.']"
        }
        mediawikiParser.inline.testSuite(test_suite_dict)

    def test_bold_italic_case3(self):
        test_suite_dict = {
                "Here, we have '''bold only and ''bold and italic''''' text.": "[rawText:'Here, we have <strong>bold only and <em>bold and italic</em></strong> text.']"
        }
        mediawikiParser.inline.testSuite(test_suite_dict)

    def test_bold_italic_case4(self):
        test_suite_dict = {
                "Here, we have '''''bold and italic''' and italic only''.": "[rawText:'Here, we have <em><strong>bold and italic</strong> and italic only</em>.']"
        }
        mediawikiParser.inline.testSuite(test_suite_dict)

    def test_bold_italic_case5(self):
        test_suite_dict = {
                "Here, we have '''''bold and italic'' and bold only'''.": "[rawText:'Here, we have <strong><em>bold and italic</em> and bold only</strong>.']"
        }
        mediawikiParser.inline.testSuite(test_suite_dict)

    def test_bold_italic_case6(self):
        test_suite_dict = {
                "Here, we have ''italic, '''bold and italic''' and italic only''.": "[rawText:'Here, we have <em>italic, <strong>bold and italic</strong> and italic only</em>.']"
        }
        mediawikiParser.inline.testSuite(test_suite_dict)

    def test_bold_italic_case7(self):
        test_suite_dict = {
                "Here, we have '''bold, ''bold and italic'' and bold only'''.": "[rawText:'Here, we have <strong>bold, <em>bold and italic</em> and bold only</strong>.']"
        }
        mediawikiParser.inline.testSuite(test_suite_dict)
