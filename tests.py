#!/usr/bin/env python

import unittest
from unittest import TestCase

from ply.lex import LexToken

from mediawiki_parser.lexer import lexer, LexError, Token as T
from mediawiki_parser.parser import parser, Link, Inline


def lexed_eq(input, want):
    """Assert lexing `input` yields `want`."""
    lexer.input(input)
    got = list(lexer)
    if want != got:
        raise AssertionError('%s != %s' % (got, want))


def parsed_eq(input, want):
    """Assert parsing `input` yields `want`."""
    got = parser.parse(input)
    if want != got:
        raise AssertionError('%s != %s' % (got, want))


def html_eq(input, want):
    """Assert the lexed, parsed, HTML-formatted input string equals `want`.

    Lets differences in linebreaks slide.

    """


class LexerTests(TestCase):
    def test_newline(self):
        lexed_eq('\r\r\n\n\r\n', [T('NEWLINE', '\r'),
                                  T('NEWLINE', '\r\n'),
                                  T('NEWLINE', '\n\r'),
                                  T('NEWLINE', '\n')])

    # def test_space_tabs(self):
    #     lexed_eq(' ', [T('SPACE_TABS', ' ')])
    #     lexed_eq('\t', [T('SPACE_TABS', '\t')])

    def test_html_entity(self):
        lexed_eq('&#x2014;', [T('TEXT', u'\u2014')])
        lexed_eq('&#8212;', [T('TEXT', u'\u2014')])
        lexed_eq('&mdash;', [T('TEXT', u'\u2014')])
        lexed_eq('&badentity;', [T('TEXT', '&badentity;')])

    def test_nowiki(self):
        lexed_eq("<nowiki>''not bold''</nowiki>", [T('TEXT', "''not bold''")])

        # HTML entities inside <nowiki> should be resolved.
        lexed_eq("<nowiki>&#8212;</nowiki>", [T('TEXT', u'\u2014')])

        lexed_eq('</nowiki>', [T('TEXT', '</nowiki>')])
        
        # Junk inside the opening tag should be tolerated:
        lexed_eq("<nowiki dudes and froods>>''cool''</nowiki>",
                 [T('TEXT', ">''cool''")])

        # <nowiki>s aren't nestable. Uncomment when bold is implemented.
        # lexed_eq("<nowiki><nowiki></nowiki>''hey''</nowiki>",
        #          [T('TEXT', '<nowiki>'),
        #           T('BOLD'),
        #           T('TEXT', 'hey'),
        #           T('BOLD_END'),
        #           T('TEXT', '</nowiki>')])

    def test_text(self):
        lexed_eq('hi', [T('TEXT', 'hi')])

    def test_heading(self):
        lexed_eq('======', [T('H2'), T('TEXT', '=='), T('H2_END')])
        lexed_eq('==', [T('TEXT', '==')])  # Headings must contain something.
        lexed_eq('====== h6 ======', [T('H6'), T('TEXT', ' h6 '), T('H6_END')])  # maintain whitespace
        lexed_eq('=h1=   ', [T('H1'), T('TEXT', 'h1'), T('H1_END')])  # strip trailing whitespace
        lexed_eq('=&amp;=', [T('H1'), T('TEXT', '&'), T('H1_END')])  # recognize contained lexemes

    def test_hr(self):
        lexed_eq('----one', [T('HR'), T('TEXT', 'one')])
        lexed_eq('-------one', [T('HR'), T('TEXT', 'one')])
        lexed_eq('one----two', [T('TEXT', 'one----two')])

    def test_combination(self):
        lexed_eq('===Llamas===\n'
                 'Llamas are cute.\n'
                 '----\n'
                 'And poetic.',
                 [T('H3'), T('TEXT', 'Llamas'), T('H3_END'), T('NEWLINE'),
                  T('TEXT', 'Llamas are cute.'), T('NEWLINE'),
                  T('HR'), T('NEWLINE'),
                  T('TEXT', 'And poetic.')])


class ParserTests(TestCase):
    def test_text(self):
        parsed_eq('Hi', Inline([u'Hi']))

    def test_internal_link(self):
        parsed_eq('[[Booga]]', Inline([Link('Booga')]))
        parsed_eq('[[this [[thing]]]]', Inline([u'[[this ', Link('thing'), u']]']))

    def test_inline(self):
        """Make sure lists of inline elements parse."""
        parsed_eq('The[[Booga]]Loo', Inline([u'The', Link('Booga'), u'Loo']))


class IntegrationTests(TestCase):
    """Tests of the whole stack, from lexer to HTML formatter"""

    def test_h1(self):
        html_eq('= h1 = trailer', '<p>= h1 = = there = boo</p>')
        html_eq(' = h1 =', '<pre>= h1 =</pre>')
        html_eq('= h1 ==',  # An H1 containing a trailing equal sign
                '<h1> <span class="mw-headline" id="h1_.3D"> h1 =</span></h1>')

# Some challenging test cases:
# <ref>[http://www.susanscott.net/Oceanwatch2002/mar1-02.html Seaweed also plays a role in the formation of sand<!-- Bot generated title -->]</ref>, from wikipedia:Sand
# [[File:Suesswasserstachelroche.jpg|thumb|A [[stingray]] about to bury itself in sand]]
# In MW, [[clay [[this [[thing]]]]]] links "thing". py-wikimarkup links the whole thing.
# [[LimBo\n]] isn't a link, but [[LimBo|and\n]] is.
# [[L'''i'''mB'''o|a'''''n''d]] is not a link; neither bold nor italics seems to be allowed in page names.
# [[LimBo|a''n''d]] is a link with an italic n.
# [[LimBo]]ohai9 uses "LimBoohai" as the linked text. (See "extra-description" on the Links page of the BNF.)
# [[Limbo|and]]ohai9 gives "andohai" as the linked text.


if __name__ == '__main__':
    unittest.main()
