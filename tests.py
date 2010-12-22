#!/usr/bin/env python

import unittest
from unittest import TestCase

from ply.lex import LexToken

from lexer import lexer, LexError


class T(object):
    """LexToken-like class, initializable on construction

    Equality with LexTokens is based on the type and value attrs, though value
    comparison is skipped if T.value is None.

    """

    def __init__(self, type_, value=None):
        self.type_ = type_
        self.value = value

    def __eq__(self, other):
        """Compare type and, if it's specified, value."""
        return (self.type_ == other.type and
                (self.value is None or self.value == other.value))

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return 'T(%s, %s)' % (repr(self.type_), repr(self.value))

    __repr__ = __str__


def lexed_eq(input, want):
    lexer.input(input)
    got = list(lexer)
    if want != got:
        raise AssertionError('%s != %s' % (got, want))


class LexerTests(TestCase):
    def test_newline(self):
        lexed_eq('\r\r\n\n\r\n', [T('newline', '\r'),
                                  T('newline', '\r\n'),
                                  T('newline', '\n\r'),
                                  T('newline', '\n')])

    def test_space_tabs(self):
        lexed_eq(' ', [T('space_tabs', ' ')])
        lexed_eq('\t', [T('space_tabs', '\t')])

    def test_html_entity(self):
        lexed_eq('&#x2014;', [T('html_entity_hex', u'\u2014')])
        lexed_eq('&#8212;', [T('html_entity_dec', u'\u2014')])
        lexed_eq('&mdash;', [T('html_entity_sym', u'\u2014')])
        self.assertRaises(LexError, lexed_eq, '&badentity;', [])


if __name__ == '__main__':
    unittest.main()
