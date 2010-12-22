"""What will eventually become a MediaWiki lexer

Based on the work at http://www.mediawiki.org/wiki/Markup_spec/BNF

"""
from ply import lex
from ply.lex import LexError as PlyLexError, lex

from constants import html_entities


class LexError(PlyLexError):
    def __str__(self):
        return str(self.__unicode__())

    def __unicode__(self):
        return u'%s: %s' % (self.args[0], self.text)


class LexerBox(object):
    """A container to group token definitions, hold state, & afford subclassing

    Don't instantiate these; that's expensive. Instead, use the module-level
    instance in `lexer`.

    """
    def __init__(self):
        """Combine the regexes and such. This is expensive."""
        self.lexer = lex(module=self, debug=True)

    # Remember, when defining tokens, not to couple any HTML-output-specific
    # transformations to their t.values. That's for the parser to decide.
    
    # The secret to lexer/parser division is: lexer recognizes only terminals.
    
    # How does PLY tell what order tokens are defined in? Allegedly, it adds
    # the callable ones in definition order and then the string ones in
    # ascending length order. [Ed: It looks at each function obj to get
    # co_firstlineno. Thus, subclassing this might not work as well as I
    # thought. TODO: Reconsider how to extend.]

    # Fundamental elements
    # (http://www.mediawiki.org/wiki/Markup_spec/BNF/Fundamental_elements):

    def t_NEWLINE(self, t):
        r'(?:\r\n|\n\r|\r|\n)'
        return t

    #t_newlines: >=1 t_newline. In the BNF but possibly unneeded.
    #t_bol: beginning of line. Should be able to fold into individual regexes.
    #t_eol: same
    #t_space = r'[ ]'  # Brackets because PLY compiles regexes with re.VERBOSE
    #t_spaces = r'[ ]+'
    #t_space_tab = r'[\t ]'
    # Add the rest of these as needed. They might be overly formal noise.

    # def t_SPACE_TABS(self, t):
    #     r'[\t ]+'
    #     return t

    def t_HTML_ENTITY_HEX(self, t):
        r'&\#x(?P<HTML_ENTITY_HEX_NUM>[0-9a-fA-F]+);'
        t.value = unichr(int(t.lexer.lexmatch.group('HTML_ENTITY_HEX_NUM'), 16))
        return t

    def t_HTML_ENTITY_DEC(self, t):
        r'&\#(?P<HTML_ENTITY_DEC_NUM>[0-9]+);'
        # Group indexes reference the combined, master regex: hard to predict.
        t.value = unichr(int(t.lexer.lexmatch.group('HTML_ENTITY_DEC_NUM')))
        return t

    def t_HTML_ENTITY_SYM(self, t):
        r'&(?P<HTML_ENTITY_SYM_NAME>[a-zA-Z1-4]+);'
        sym = t.lexer.lexmatch.group('HTML_ENTITY_SYM_NAME')
        if sym in html_entities:
            t.value = unichr(html_entities[sym])
        else:
            t.type = 'text'
        return t

    # <url-path>		::= <url-char> [<url-path>]
    # <url-char>		::= LEGAL_URL_ENTITY  # Not only "abc" and "%23" but "%ey", all of which should be preserved verbatim.

    def t_error(self, t):
        raise LexError('Illegal character', t.value[0])
        #t.lexer.skip(1)

    # Everything after the t_ in anything that starts with t_:
    tokens = ([k[2:] for k in vars().keys() if k.startswith('t_') and k != 't_error'] +
              ['text'])

lexer = LexerBox().lexer
# TODO: Since we might have multiple threads, have the class build the lexer
# once and stash it in a class var. Then clone from it on construction of
# future instances.
