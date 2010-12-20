#!/usr/bin/env python
"""What will eventually become a MediaWiki parser.

Based on the work at http://www.mediawiki.org/wiki/Markup_spec/BNF

"""

from pyparsing import *
import string


def parsed_eq(expr, text, want):
    got = expr.parseString(text).asList()
    if got != want:
        raise AssertionError('%s != %s' % (got, want))


ParserElement.setDefaultWhitespaceChars('')  # Whitespace is significant.
ParserElement.enablePackrat()  # Enable memoizing.


# Fundamental elements (http://www.mediawiki.org/wiki/Markup_spec/BNF/Fundamental_elements):
# TODO: Put Group() around almost everything to shape the output into a parse tree. Assign setResultsName()s to everything so we can tell what kind of tokens they are.
newline = Literal('\r\n') | '\n\r' | '\r' | '\n'
newlines = Combine(OneOrMore(newline))
#newlines.verbose_stacktrace = True
bol = newline | StringStart()
eol = newline | StringEnd()

space = Literal(' ')
spaces = Combine(OneOrMore(space))
space_tab = (space | '\t').parseWithTabs()
space_tabs = OneOrMore(space_tab)

whitespace_char = (space_tab | newline).parseWithTabs()
whitespace = Combine(OneOrMore(whitespace_char) + Optional(StringEnd())).parseWithTabs()

hex_digit = oneOf(list(hexnums))
hex_number = Combine(OneOrMore(hex_digit))

decimal_digit = oneOf(list(nums))
decimal_number = Combine(OneOrMore(decimal_digit))

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
               ('&' + html_entity_chars + ';')).setResultsName('html_entity')

character = html_entity | whitespace_char | non_whitespace_char


# (Temporary?) unit tests:
parsed_eq(OneOrMore(newline), '\r\r\n\n\r\n', ['\r', '\r\n', '\n\r', '\n'])
parsed_eq(newlines, '\r\r\n\n\r\n', ['\r\r\n\n\r\n'])
parsed_eq(bol + 'hi', 'hi', ['hi'])
parsed_eq(bol + 'hi', '\nhi', ['\n', 'hi'])
parsed_eq('hi' + eol, 'hi', ['hi'])
parsed_eq('hi' + eol, 'hi\n', ['hi', '\n'])
parsed_eq(spaces, '  ', ['  '])
parsed_eq(space_tab, '\t', ['\t'])
parsed_eq(whitespace_char, '\t', ['\t'])
parsed_eq(whitespace, ' \t\r', [' \t\r'])
parsed_eq(whitespace, ' hi', [' '])  # no StringEnd
parsed_eq(hex_number, '123DECAFBAD', ['123DECAFBAD'])
parsed_eq(decimal_number, '0123', ['0123'])

p = character.parseString('&#xdeadbeef;')
assert p.getName() == 'html_entity'
    

print "All's well!"

# try:
#     p = newlines.parseString(str)
# except ParseException, e:
#     print repr(e.msg)
#     raise
# else:
#     print p
