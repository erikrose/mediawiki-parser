#!/usr/bin/env python
"""What will eventually become a MediaWiki parser.

Based on the work at http://www.mediawiki.org/wiki/Markup_spec/BNF

"""

from pyparsing import *
import string


def parsed_eq(expr, text, want):
    got = list(expr.parseString(text))
    if got != want:
        raise AssertionError('%s != %s' % (got, want))


ParserElement.setDefaultWhitespaceChars('')  # Whitespace is significant.
ParserElement.enablePackrat()  # Enable memoizing.

bold = Literal("'''")
italic = Literal("''")
char = oneOf(list(string.printable))
# TODO: Optimize by turning into something like...
# text = Word(string.printable)
inline = bold | italic | char  # in order of precedence: see docs at MatchFirst
stuff = ZeroOrMore(inline)

nice_char = oneOf(['a', 'b', 'c'])
bingy = Group('!' + Combine(OneOrMore(nice_char)) + '@')
stuff = OneOrMore(bingy)

# Real MediaWiki syntax:
## Fundamental elements:
newline = (Literal('\r\n') | '\n\r' | '\r' | '\n')
parsed_eq(OneOrMore(newline), '\r\r\n\n\r\n', ['\r', '\r\n', '\n\r', '\n'])
newlines = Combine(OneOrMore(newline))
#newlines.verbose_stacktrace = True
parsed_eq(newlines, '\r\r\n\n\r\n', ['\r\r\n\n\r\n'])
bol = newline | StringStart()
parsed_eq(bol + 'hi', 'hi', ['hi'])
parsed_eq(bol + 'hi', '\nhi', ['\n', 'hi'])
eol = newline | StringEnd()
parsed_eq('hi' + eol, 'hi', ['hi'])
parsed_eq('hi' + eol, 'hi\n', ['hi', '\n'])

space = Literal(' ')
spaces = Combine(OneOrMore(space))
parsed_eq(spaces, '  ', ['  '])
space_tab = (space | '\t').parseWithTabs()
parsed_eq(space_tab, '\t', ['\t'])
space_tabs = OneOrMore(space_tab)

whitespace_char = (space_tab | newline).parseWithTabs()
parsed_eq(whitespace_char, '\t', ['\t'])
whitespace = Combine(OneOrMore(whitespace_char) + Optional(StringEnd())).parseWithTabs()
parsed_eq(whitespace, ' \t\r', [' \t\r'])
parsed_eq(whitespace, ' hi', [' '])  # no StringEnd

hex_digit = oneOf(list(hexnums))
hex_number = Combine(OneOrMore(hex_digit))
parsed_eq(hex_number, '123DECAFBAD', ['123DECAFBAD'])

decimal_digit = oneOf(list(nums))
decimal_number = Combine(OneOrMore(decimal_digit))
parsed_eq(decimal_number, '0123', ['0123'])

underscore = Literal('_')
html_unsafe_symbol = oneOf(list('<>&'))  # TODO: on output, escape
symbol = Regex('[^0-9a-zA-Z]')  # inferred from inadequate description
lcase_letter = Regex('[a-z]')
ucase_letter = Regex('[A-Z]')
letter = Regex('[a-zA-Z]')
non_whitespace_char = letter | decimal_digit | symbol  # Optimize all such combinations; they'd probably benefit from being collapsed into single regex alternations.

html_entity_char = letter | decimal_digit
html_entity_chars = OneOrMore(html_entity_char)
html_entity = (('&#x' + hex_number + ';') |
               ('&#' + decimal_number + ';') |
               ('&' + html_entity_chars + ';')).setParseAction(lambda toks: 'yeah%s' % toks).setResultsName('html_entity')

character = html_entity | whitespace_char | non_whitespace_char
#parsed_eq(character, '&#xdeadbeef', ['yeahdeadbeef'])  # NEXT: Make this work, just to understand setParseAction.
print "All's well!"

# try:
#     p = newlines.parseString(str)
# except ParseException, e:
#     print repr(e.msg)
#     raise
# else:
#     print p
