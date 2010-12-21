#!/usr/bin/env python

from pyparsing import *


# Spike to prove we can get a parse tree out of PyParsing:
letters = Regex('[a-zA-Z]+').setName('letters').setDebug()
bold_toggle = Literal("'''").setName('bold_toggle').setDebug()
italic_toggle = Literal("''").setName('italic_toggle').setDebug()
text_with_formatting = Forward()
italic_span = Forward()
bold_span = Group(bold_toggle + OneOrMore(italic_span | letters) + bold_toggle).setName('bold_span').setDebug()
italic_span << Group(italic_toggle + OneOrMore(bold_span | letters) + italic_toggle).setName('italic_span').setDebug()
text_with_formatting << OneOrMore(bold_span | italic_span | letters).setName('text_with_formatting').setDebug()
text_with_formatting.verbose_stacktrace = True

#                                       12345678901234567890123
print text_with_formatting.parseString("'''bdasl''hide''seek'''")  # This doesn't.

# Next: traverse the tree. Make sure that doesn't hurt.
