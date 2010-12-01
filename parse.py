#!/usr/bin/env python

from pyparsing import *
import string


def parsed_eq(expr, text, want):
    got = list(expr.parseString(text))
    if got != want:
        raise AssertionError('%s != %s' % (got, want))


ParserElement.enablePackrat()  # Enable memoizing.

bold = Literal("'''")
italic = Literal("''")
char = oneOf(list(string.printable))
# TODO: Optimize by turning into something like...
# text = Word(string.printable)
inline = bold | italic | char  # in order of precedence: see docs at MatchFirst
stuff = ZeroOrMore(inline)

nice_char = oneOf(['a', 'b', 'c'])
bingy = Group(Literal('!') + Combine(OneOrMore(nice_char)) + Literal('@'))
stuff = OneOrMore(bingy)

# Real MediaWiki syntax:
## Fundamental elements:
newline = (Literal('\r\n') | Literal('\n\r') | Literal('\r') | Literal('\n')).leaveWhitespace()
newlines = OneOrMore(newline)
#newlines.verbose_stacktrace = True
parsed_eq(newlines, '\r\r\n\n\r\n', ['\r', '\r\n', '\n\r', '\n'])

space = Literal(' ').leaveWhitespace()
spaces = OneOrMore(space)
parsed_eq(spaces, '  ', [' ', ' '])
space_tab = (space | Literal('\t').leaveWhitespace()).leaveWhitespace().parseWithTabs()
parsed_eq(space_tab, '\t', ['\t'])
space_tabs = OneOrMore(space_tab)

whitespace_char = (space_tab | newline).leaveWhitespace().parseWithTabs()
parsed_eq(whitespace_char, '\t', ['\t'])
whitespace = (OneOrMore(whitespace_char) | StringEnd()).leaveWhitespace().parseWithTabs()
parsed_eq(whitespace, ' \t\r', [' ', '\t', '\r'])

# try:
#     p = newlines.parseString(str)
# except ParseException, e:
#     print repr(e.msg)
#     raise
# else:
#     print p
