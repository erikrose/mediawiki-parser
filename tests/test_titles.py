# -*- coding: utf8 -*-

from mediawiki_parser import wikitextParser
mediawikiParser = wikitextParser.wikitextParser

from unittest import TestCase


class NowikiTests(TestCase):
    def test_title1(self):
        test_suite_dict = {
                '=Title 1=\n': "[title1:[rawText:'Title 1']]"
        }
        mediawikiParser.testSuite(test_suite_dict)

    def test_title2(self):
        test_suite_dict = {
                '== Title 2 ==\n': "[title2:[rawText:' Title 2 ']]"
        }
        mediawikiParser.testSuite(test_suite_dict)

    def test_title3_extra_spacetab(self):
        # Ignore extra spaces and tabs
        test_suite_dict = {
                '===Title 3===                    \n': "[title3:[rawText:'Title 3']]"
        }
        mediawikiParser.testSuite(test_suite_dict)

    def test_title4(self):
        # Ignore extra spaces and tabs
        test_suite_dict = {
                '==== Title 4 ====\n': "[title4:[rawText:' Title 4 ']]"
        }
        mediawikiParser.testSuite(test_suite_dict)

    def test_title5(self):
        test_suite_dict = {
                '===== Title 5 =====\n': "[title5:[rawText:' Title 5 ']]"
        }
        mediawikiParser.testSuite(test_suite_dict)

    def test_title6(self):
        test_suite_dict = {
                '====== Title 6 ======\n': "[title6:[rawText:' Title 6 ']]"
        }
        mediawikiParser.testSuite(test_suite_dict)

    def test_title7(self):
        # Max level is 6; keep extra equals
        test_suite_dict = {
                '======= Title 6 =======\n': "[title6:[rawText:'= Title 6 =']]"
        }
        mediawikiParser.testSuite(test_suite_dict)

    def test_link_in_title(self):
        # Max level is 6; keep extra equals
        test_suite_dict = {
                '= [[a link]] =\n': "[title1:[rawText:' '  simpleInternalLink:'a link'  rawText:' ']]"
        }
        mediawikiParser.testSuite(test_suite_dict)

    def test_italic_in_title(self):
        test_suite_dict = {
                "== ''italic text'' ==\n": "[title2:[rawText:' <em>italic text</em> ']]"
        }
        mediawikiParser.testSuite(test_suite_dict)

    def test_bold_in_title(self):
        test_suite_dict = {
                "=== '''bold text''' ===\n": "[title3:[rawText:' <strong>bold text</strong> ']]"
        }
        mediawikiParser.testSuite(test_suite_dict)

    def test_formatted_link_in_title(self):
        test_suite_dict = {
                "==== ''[[Title 4|formatted link]]'' ====\n": "[title4:[rawText:' <em></em>'  advancedInternalLink:[templateName:'Title 4'  @cleanInline@:[rawText:'formatted link']]  rawText:'<em> </em>']]"
        }
        mediawikiParser.testSuite(test_suite_dict)

    def test_simple_template_in_title(self):
        test_suite_dict = {
                '===== {{Title 5}} =====\n': "[title5:[rawText:' '  simpleTemplate:'Title 5'  rawText:' ']]"
        }
        mediawikiParser.testSuite(test_suite_dict)

    def test_braces_in_title(self):
        test_suite_dict = {
                '====== { Title 6} ======\n': "[title6:[rawText:' '  allowedChar:'{'  rawText:' Title 6'  allowedChar:'}'  rawText:' ']]"
        }
        mediawikiParser.testSuite(test_suite_dict)

    def test_equal_in_title(self):
        test_suite_dict = {
                '== Title = title ==\n': "[title2:[rawText:' Title = title ']]"
        }
        mediawikiParser.testSuite(test_suite_dict)

    def test_more_equal_in_title(self):
        test_suite_dict = {
                '== Title == title ==\n': "[title2:[rawText:' Title == title ']]"
        }
        mediawikiParser.testSuite(test_suite_dict)
