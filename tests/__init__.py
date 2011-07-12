# -*- coding: utf8 -*-
from unittest import TestCase


class ParserTestCase(TestCase):
    def _grammar(self, method_name):
        """Return a full or partial grammar.

        method_name -- If truthy, the attribute of the full grammar to return

        """
        from raw import parser
        return getattr(parser, method_name) if method_name else parser

    def parsed_equal_string(self, source, result, method_name):
        self.assertEquals(unicode(self._grammar(method_name).parseTest(source).value), result)

    def parsed_equal_tree(self, source, result, method_name):
        self.assertEquals(self._grammar(method_name).parseTest(source).treeView(), result)
