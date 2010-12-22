#!/usr/bin/env python

import unittest
from unittest import TestCase

from ply.lex import LexToken

from lexer import lexer


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


def lexed_eq(lexer, input, want):
    lexer.input(input)
    got = list(lexer)
    if want != got:
        raise AssertionError('%s != %s' % (got, want))


class LexerTests(TestCase):
    def test_newline(self):
        lexed_eq(lexer, '\r\r\n\n\r\n', [T('newline', '\r'),
                                         T('newline', '\r\n'),
                                         T('newline', '\n\r'),
                                         T('newline', '\n')])

if __name__ == '__main__':
    unittest.main()
