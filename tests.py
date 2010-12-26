#!/usr/bin/env python

import unittest
from unittest import TestCase

from ply.lex import LexToken

from lexer import lexer, LexError, Token as T


def lexed_eq(input, want):
    """Assert lexing `input` yields `want`."""
    lexer.input(input)
    got = list(lexer)
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

        # <nowiki>s aren't nestable. Uncomment when bold is implemented.
        # lexed_eq("<nowiki><nowiki></nowiki>''hey''</nowiki>",
        #          [T('TEXT', '<nowiki>'),
        #           T('BOLD'),
        #           T('TEXT', 'hey'),
        #           T('BOLD_END'),
        #           T('TEXT', '</nowiki>')])

    def test_text(self):
        lexed_eq('hi', [T('TEXT', 'hi')])


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

if __name__ == '__main__':
    unittest.main()
