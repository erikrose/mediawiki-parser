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
newlines = Combine(OneOrMore(newline)).leaveWhitespace()
#newlines.verbose_stacktrace = True
parsed_eq(OneOrMore(newline), '\r\r\n\n\r\n', ['\r', '\r\n', '\n\r', '\n'])
parsed_eq(newlines, '\r\r\n\n\r\n', ['\r\r\n\n\r\n'])

space = Literal(' ').leaveWhitespace()
spaces = Combine(OneOrMore(space)).leaveWhitespace()
parsed_eq(spaces, '  ', ['  '])
space_tab = (space | Literal('\t').leaveWhitespace()).leaveWhitespace().parseWithTabs()
parsed_eq(space_tab, '\t', ['\t'])
space_tabs = OneOrMore(space_tab)

whitespace_char = (space_tab | newline).leaveWhitespace().parseWithTabs()
parsed_eq(whitespace_char, '\t', ['\t'])
whitespace = Combine(OneOrMore(whitespace_char) + Optional(StringEnd())).leaveWhitespace().parseWithTabs()
parsed_eq(whitespace, ' \t\r', [' \t\r'])
parsed_eq(whitespace, ' hi', [' '])  # no StringEnd

hex_digit = oneOf(list(hexnums))
hex_number = Combine(OneOrMore(hex_digit))
parsed_eq(hex_number, '123DECAFBAD', ['123DECAFBAD'])

decimal_digit = oneOf(list(nums))
decimal_number = Combine(OneOrMore(decimal_digit))
parsed_eq(decimal_number, '0123', ['0123'])
# try:
#     p = newlines.parseString(str)
# except ParseException, e:
#     print repr(e.msg)
#     raise
# else:
#     print p
