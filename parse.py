#!/usr/bin/env python

from pyparsing import *
import string

ParserElement.enablePackrat()  # Enable memoizing.

bold = Literal("'''")
italic = Literal("''")
char = oneOf(list(string.printable))
# TODO: Optimize by turning into something like...
# text = Word(string.printable)
inline = bold | italic | char  # in order of precedence
stuff = ZeroOrMore(inline)

p = stuff.parseString("'''boo hoohoo''")
print p
