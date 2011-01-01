#!/usr/bin/env python
"""A parser that builds an abstract syntax tree from MediaWiki syntax"""

# TODO: Probably yacc.yacc(write_tables=0) to keep from doing FS writes.
# TODO: Return lightweight tuples or even chunks of CElementTree from parse rules. Then have a decoupled HTML writer walk them.

# Shift/reduce conflicts happen when there are 2 or more productions that could be chosen, like "abcd: A B C D" or "abcx: A B empty C X". There, the conflict happens as C is seen.

# Maybe use embedded rules (section 6.11) to keep track of apostrophe jungles?

# Perhaps we can best recover from things that look like they're going to be productions but aren't by catching them in the error procedure and then just printing them out verbatim.

from pprint import pformat

from ply.yacc import yacc

from mediawiki_parser.lexer import lexer


class ParserBox(object):
    def __init__(self, lexer=lexer):
        self.tokens = lexer.tokens
        self._lexer = lexer
        self._parser = yacc(module=self, debug=True)

    def p_inline(self, p):  # Called "inline_text" in the BNF
        """inline : inline inline_element
                  | inline_element"""
        if len(p) == 3:  # TODO: Split into separate rules for speed.
            p[0] = p[1] + Inline([p[2]])
        else:
            p[0] = Inline([p[1]])

    def p_inline_element(self, p):
        """inline_element : TEXT
                          | internal_link"""
        p[0] = p[1]

    def p_internal_link(self, p):
        'internal_link : INTERNAL_LINK_START TEXT INTERNAL_LINK_END'
        p[0] = Link(p[2])

    def parse(self, text):
        return self._parser.parse(text, lexer=self._lexer)

parser = ParserBox()


class Node(object):
    def __str__(self):
        return '%s(%s)' % (self.__class__.__name__, ', '.join('%s=%s' % (k, repr(v)) for k, v in self.__dict__.iteritems()))

    __repr__ = __str__

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class Link(Node):
    def __init__(self, text):
        self.text = text


class Inline(list):
    pass


if __name__ == '__main__':
    def repl():
        while True:
            try:
                input = raw_input('parser> ')
            except EOFError:
                break
            print parser.parse(input)
    repl()
