# -*- coding: utf8 -*-

from mediawiki_parser import wikitextParser
mediawikiParser = wikitextParser.wikitextParser

from unittest import TestCase


class LinkTests(TestCase):
    def test_simple_internal_link(self):
        test_suite_dict = {
                '[[article]]': "[simpleInternalLink:'article']"
        }
        mediawikiParser.inline.testSuite(test_suite_dict)

    def test_advanced_internal_link(self):
        test_suite_dict = {
                '[[article|alternate]]': "[advancedInternalLink:[templateName:'article'  @cleanInline@:[rawText:'alternate']]]"
        }
        mediawikiParser.inline.testSuite(test_suite_dict)

    def test_url(self):
        test_suite_dict = {
                'An URL: http://www.mozilla.org': "[rawText:'An URL: '  url:'http://www.mozilla.org']"
        }
        mediawikiParser.inline.testSuite(test_suite_dict)

    def test_external_link(self):
        test_suite_dict = {
                "[http://www.mozilla.org this is an ''external'' link]": "[externalLink:[url:'http://www.mozilla.org'  @cleanInline@:[rawText:'this is an <em>external</em> link']]]"
        }
        mediawikiParser.inline.testSuite(test_suite_dict)

    def test_formatted_external_link(self):
        test_suite_dict = {
                '<a href="http://www.mozilla.org">this is an \'\'external\'\' link</a>': "[rawText:'<a href=\"'  url:'http://www.mozilla.org'  rawText:'\">this is an <em>external</em> link</a>']"
        }
        mediawikiParser.inline.testSuite(test_suite_dict)
