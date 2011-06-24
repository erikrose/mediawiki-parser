# -*- coding: utf8 -*-

from mediawiki_parser import wikitextParser
mediawikiParser = wikitextParser.wikitextParser

from unittest import TestCase


class ParserTestCase(TestCase):
    def parsed_equal_string(self, source, result, method_name):
        if method_name is not None:
            grammar = getattr(mediawikiParser, method_name)
        else:
            grammar = mediawikiParser
        self.assertEquals(unicode(grammar.parseTest(source).value), result)

    def parsed_equal_tree(self, source, result, method_name):
        if method_name is not None:
            grammar = getattr(mediawikiParser, method_name)
        else:
            grammar = mediawikiParser
        self.assertEquals(grammar.parseTest(source).treeView(), result)
