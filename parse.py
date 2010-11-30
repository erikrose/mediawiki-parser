#!/usr/bin/env python

from pyparsing import *
import string

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
newline = (Literal('\r\n') | Literal('\n\r') | Literal('\r') | Literal('\n')).leaveWhitespace()
newlines_f = Forward()
newlines = (newline + Optional(newlines_f)).leaveWhitespace()
newlines_f << newlines

newlines.verbose_stacktrace = True
str = "\r\n\r\n\n"
print repr(str)
try:
    p = newlines.parseString(str)
except ParseException, e:
    print repr(e.msg)
    raise
else:
    print p
