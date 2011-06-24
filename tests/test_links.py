# -*- coding: utf8 -*-

from mediawiki_parser.tests import ParserTestCase


class Links_tests(ParserTestCase):
    def test_simple_internal_link(self):
        source = '[[article]]'
        result = "[simpleInternalLink:'article']"
        self.parsed_equal_string(source, result, 'inline')

    def test_advanced_internal_link(self):
        source = '[[article|alternate]]'
        result = "[advancedInternalLink:[templateName:'article'  @cleanInline@:[rawText:'alternate']]]"
        self.parsed_equal_string(source, result, 'inline')

    def test_url(self):
        source = 'An URL: http://www.mozilla.org'
        result = "[rawText:'An URL: '  url:'http://www.mozilla.org']"
        self.parsed_equal_string(source, result, 'inline')

    def test_external_link(self):
        source = "[http://www.mozilla.org this is an ''external'' link]"
        result = "[externalLink:[url:'http://www.mozilla.org'  @cleanInline@:[rawText:'this is an <em>external</em> link']]]"
        self.parsed_equal_string(source, result, 'inline')

    def test_formatted_external_link(self):
        source = '<a href="http://www.mozilla.org">this is an \'\'external\'\' link</a>'
        result = "[rawText:'<a href=\"'  url:'http://www.mozilla.org'  rawText:'\">this is an <em>external</em> link</a>']"
        self.parsed_equal_string(source, result, 'inline')
