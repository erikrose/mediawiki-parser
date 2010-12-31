#!/usr/bin/env python
"""What will eventually become a MediaWiki lexer"""

import re
import readline  # Make raw_input() cool.

from ply.lex import LexError as PlyLexError, lex

from constants import html_entities


class LexError(PlyLexError):
    def __str__(self):
        return str(self.__unicode__())

    def __unicode__(self):
        return u'%s: %s' % (self.args[0], self.text)


class Token(object):
    """LexToken-like class, initializable on construction

    Equality with LexTokens is based on the type and value attrs, though value
    comparison is skipped if T.value is None.

    """

    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __eq__(self, other):
        """Compare type and, if it's specified, value."""
        return (self.type == other.type and
                (self.value is None or self.value == other.value))

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return 'T(%s, %s)' % (repr(self.type), repr(self.value))

    __repr__ = __str__


class LexerBox(object):
    """A container to group token definitions, hold state, & afford subclassing

    Don't instantiate these; that's expensive. Instead, use the module-level
    instance in `lexer`.

    """
    states = [('nowiki', 'exclusive'),
              ('heading', 'exclusive')]

    def __init__(self):
        """Combine the regexes and such. This is expensive."""
        self.lexer = lex(module=self, debug=True, reflags=re.M)
        self.heading_level = 0  # number of =s in the start token of the heading we're currently scanning

    # Remember, when defining tokens, not to couple any HTML-output-specific
    # transformations to their t.values. That's for the formatter to decide.

    # The secret to lexer/parser division is: lexer recognizes only terminals
    # (or else makes recursive calls to itself).

    # Any line that does not start with one of the following is not a special
    # block: " " | "{|" | "#" | ";" | ":" | "*" | "=".
    # (http://www.mediawiki.org/wiki/Markup_spec/BNF/Article#Article)

    # TODO: Would using __slots__ in LexToken speed things up? token()
    # instantiates a lot of them.

    # How does PLY tell what order tokens are defined in? Allegedly, it adds
    # the callable ones in definition order and then the string ones in
    # ascending length order. [Ed: It looks at each function obj to get
    # co_firstlineno. Thus, subclassing this might not work as well as I
    # thought. TODO: Reconsider how to extend.]

    def t_heading_INITIAL_NOWIKI(self, t):
        r'<[nN][oO][wW][iI][kK][iI](?:\s[^>]*)?>'
        t.lexer.push_state('nowiki')  # Use stack in case inside a table or something.
        # TODO: Optimize this state by making a special text token that'll chew
        # up anything that's not </nowiki>.
        return None

    def t_nowiki_heading_NOWIKI_END(self, t):
        r'</[nN][oO][wW][iI][kK][iI]>'
        t.lexer.pop_state()
        return None

    def t_HEADING_START(self, t):
        r'^(?P<HEADING_LEVEL>={1,6})(?=.+?(?P=HEADING_LEVEL)\s*$)'
        # Hoping the non-greedy .+? makes this a bit more efficient
        level = len(t.lexer.lexmatch.group('HEADING_LEVEL'))
        t.type = 'H%i' % level
        # t.value doesn't matter.
        self.heading_level = level
        t.lexer.push_state('heading')
        return t

    def t_heading_HEADING_END(self, t):
        r'=+\s*$'  # Swallows trailing whitespace like MediaWiki
        # If we mistakenly match too early and catch more =s than needed in a
        # heading like = hi ==, return one of the =s as a text token, and
        # resume lexing at the next = to try again. It was either this or else
        # face a profusion of states, one for each heading level (or
        # dynamically add a regex to the master regex, which would be a cool
        # feature for it to support). Headings that end in = should be a rare
        # case, thankfully.
        matched_level = len(t.value.rstrip())
        if matched_level > self.heading_level:
            t.type = 'TEXT'
            t.value = '='
            t.lexer.lexpos -= (matched_level - 1)
        else:
            t.type = 'H%i_END' % self.heading_level
            # t.value doesn't matter.
            self.heading_level = 0
            t.lexer.pop_state()
        return t

    def t_HR(self, t):
        r'^----+'
        # t.value doesn't matter.
        return t

    def t_NEWLINE(self, t):
        r'(?:\r\n|\n\r|\r|\n)'
        return t

    def t_ANY_HTML_ENTITY_HEX(self, t):
        r'&\#x(?P<HTML_ENTITY_HEX_NUM>[0-9a-fA-F]+);'
        t.value = unichr(int(t.lexer.lexmatch.group('HTML_ENTITY_HEX_NUM'), 16))
        t.type = 'TEXT'
        return t

    def t_ANY_HTML_ENTITY_DEC(self, t):
        r'&\#(?P<HTML_ENTITY_DEC_NUM>[0-9]+);'
        # Group indexes reference the combined, master regex: hard to predict.
        t.value = unichr(int(t.lexer.lexmatch.group('HTML_ENTITY_DEC_NUM')))
        t.type = 'TEXT'
        return t

    def t_ANY_HTML_ENTITY_SYM(self, t):
        r'&(?P<HTML_ENTITY_SYM_NAME>[a-zA-Z1-4]+);'
        sym = t.lexer.lexmatch.group('HTML_ENTITY_SYM_NAME')
        if sym in html_entities:
            t.value = unichr(html_entities[sym])
        t.type = 'TEXT'
        return t

    def t_ANY_HARMLESS_TEXT(self, t):
        r'[a-zA-Z0-9]+'
        # Runs of stuff that can't possibly be part of another token. An
        # optimization to avoid hitting t_ANY_TEXT
        # TODO: Harmless Unicode chars are missing, so Japanese will go slow.
        t.type = 'TEXT'
        return t

    def t_ANY_TEXT(self, t):  # probably scarily inefficient
        r'.'
        return t

    # <url-path>		::= <url-char> [<url-path>]
    # <url-char>		::= LEGAL_URL_ENTITY  # Not only "abc" and "%23" but "%ey", all of which should be preserved verbatim.

    def t_ANY_error(self, t):
        raise LexError('Illegal character', t.value[0])
        #t.lexer.skip(1)

    def __iter__(self):
        return merged_text_tokens(iter(self.lexer))

    def input(self, text):
        return self.lexer.input(text)

    tokens = ['NEWLINE', 'TEXT', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H1_END', 'H2_END', 'H3_END', 'H4_END', 'H5_END', 'H6_END', 'HR']

lexer = LexerBox()
# TODO: Since we might have multiple threads, have the class build the lexer
# once and stash it in a class var. Then clone from it on construction of
# future instances.


def merged_text_tokens(tokens):
    """Merge adjacent TEXT tokens in the given iterable of LexTokens."""
    # I hope to make this unnecessary with clever definitions of tokens somehow.
    acc = []
    for t in tokens:
        if t.type == 'TEXT':
            acc.append(t.value)
        else:
            if acc:
                yield Token('TEXT', ''.join(acc))
                acc = []
            yield t
    if acc:  # in case last token is TEXT
        yield Token('TEXT', ''.join(acc))


if __name__ == '__main__':
    def repl():
        while True:
            try:
                input = raw_input('lexer> ')
            except EOFError:
                break
            try:
                lexer.input(input)
                print list(lexer)
            except LexError, e:
                print e
    repl()
