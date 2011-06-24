# -*- coding: utf8 -*-

from mediawiki_parser import wikitextParser
mediawikiParser = wikitextParser.wikitextParser

from unittest import TestCase


class LinkTests(TestCase):
    def test_simple_internal_link(self):
        source = '[[article]]'
        exp_result = "[simpleInternalLink:'article']"
        got_result = unicode(mediawikiParser.inline.parseTest(source).value)
        self.assertEquals(exp_result, got_result)

    def test_advanced_internal_link(self):
        source = '[[article|alternate]]'
        exp_result = "[advancedInternalLink:[templateName:'article'  @cleanInline@:[rawText:'alternate']]]"
        got_result = unicode(mediawikiParser.inline.parseTest(source).value)
        self.assertEquals(exp_result, got_result)

    def test_url(self):
        source = 'An URL: http://www.mozilla.org'
        exp_result = "[rawText:'An URL: '  url:'http://www.mozilla.org']"
        got_result = unicode(mediawikiParser.inline.parseTest(source).value)
        self.assertEquals(exp_result, got_result)

    def test_external_link(self):
        source = "[http://www.mozilla.org this is an ''external'' link]"
        exp_result = "[externalLink:[url:'http://www.mozilla.org'  @cleanInline@:[rawText:'this is an <em>external</em> link']]]"
        got_result = unicode(mediawikiParser.inline.parseTest(source).value)
        self.assertEquals(exp_result, got_result)

    def test_formatted_external_link(self):
        source = '<a href="http://www.mozilla.org">this is an \'\'external\'\' link</a>'
        exp_result = "[rawText:'<a href=\"'  url:'http://www.mozilla.org'  rawText:'\">this is an <em>external</em> link</a>']"
        got_result = unicode(mediawikiParser.inline.parseTest(source).value)
        self.assertEquals(exp_result, got_result)
