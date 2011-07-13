# -*- coding: utf8 -*-
from unittest import TestCase


def setup_module():
    from pijnu import makeParser
    mediawikiGrammar = file("mediawiki.pijnu").read()
    mediawikiParser = makeParser(mediawikiGrammar)

class ParserTestCase(TestCase):
    def _grammar(self, method_name):
        """Return a full or partial grammar.

        method_name -- If truthy, the attribute of the full grammar to return

        """
        from mediawiki_parser import raw
        parser = raw.make_parser()
        return getattr(parser, method_name) if method_name else parser

    def parsed_equal_string(self, source, result, method_name):
        self.assertEquals(unicode(self._grammar(method_name).parseTest(source).value), result)

    def parsed_equal_tree(self, source, result, method_name):
        self.assertEquals(self._grammar(method_name).parseTest(source).treeView(), result)
