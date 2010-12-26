#!/usr/bin/env python
"""What will eventually become a MediaWiki lexer

Based on the work at http://www.mediawiki.org/wiki/Markup_spec/BNF

"""
import readline  # Make raw_input() cool.

from ply import lex
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
    states = [('nowiki', 'exclusive')]
    
    def __init__(self):
        """Combine the regexes and such. This is expensive."""
        self.lexer = lex(module=self, debug=True)

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

    def t_NOWIKI(self, t):
        r'<[nN][oO][wW][iI][kK][iI]>'
        t.lexer.push_state('nowiki')  # Use stack in case inside a table or something.
        # TODO: Optimize this state by making a special text token that'll chew
        # up anything that's not </nowiki>.
        return None

    def t_nowiki_NOWIKI_END(self, t):
        r'</[nN][oO][wW][iI][kK][iI]>'
        t.lexer.pop_state()
        return None

    # def t_HEADING(self, t):
    #     r'^(?P<HEADING_LEVEL>={1,6})(.+)\g<HEADING_LEVEL>\s*'  # TODO: Or do we just match the terminals and let the parser sort out the pairing of === spans? H2 :: =={text}=={whitespace}. Or do we match ^== and then throw the lexer into a 'header' state which tries to .... Can't just match the whole line in one regex, because then the lexer never gets a chance to parse the text of the header normally and resolve the entities.
    #   # Swallows trailing whitespace like MediaWiki
    #   t.type = 

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

    tokens = ['NEWLINE', 'TEXT']

lexer = LexerBox()
# TODO: Since we might have multiple threads, have the class build the lexer
# once and stash it in a class var. Then clone from it on construction of
# future instances.


def merged_text_tokens(tokens):
    """Merge adjacent TEXT tokens in the given iterable of LexTokens."""
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
