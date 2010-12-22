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

    # How does PLY tell what order tokens are defined in? Allegedly, it adds
    # the callable ones in definition order and then the string ones in
    # ascending length order. [Ed: It looks at each function obj to get
    # co_firstlineno. Thus, subclassing this might not work as well as I
    # thought. TODO: Reconsider how to extend.]

    # Fundamental elements
    # (http://www.mediawiki.org/wiki/Markup_spec/BNF/Fundamental_elements):

    t_newline = r'(?:\r\n|\n\r|\r|\n)'
    #t_newlines: >=1 t_newline. In the BNF but possibly unneeded.
    #t_bol: beginning of line. Should be able to fold into individual regexes.
    #t_eol: same
    #t_space = r'[ ]'  # Brackets because PLY compiles regexes with re.VERBOSE
    #t_spaces = r'[ ]+'
    #t_space_tab = r'[\t ]'
    t_space_tabs = r'[\t ]+'
    # Add the rest of these as needed. They might be overly formal noise.

    def t_html_entity_hex(self, t):
        r'&\#x(?P<html_entity_hex_num>[0-9a-fA-F]+);'
        t.value = unichr(int(t.lexer.lexmatch.group('html_entity_hex_num'), 16))
        return t

    def t_html_entity_dec(self, t):
        r'&\#(?P<html_entity_dec_num>[0-9]+);'
        # Group indexes reference the combined, master regex: hard to predict.
        t.value = unichr(int(t.lexer.lexmatch.group('html_entity_dec_num')))
        return t

    def t_html_entity_sym(self, t):
        r'&(?P<html_entity_sym_name>[a-zA-Z1-4]+);'
        sym = t.lexer.lexmatch.group('html_entity_sym_name')
        if sym in html_entities:
            t.value = unichr(html_entities[sym])
        else:
            t.type = 'text'
        return t

    def t_error(self, t):
        raise LexError('Illegal character', t.value[0])
        #t.lexer.skip(1)

    # Everything after the t_ in anything that starts with t_:
    tokens = ([k[2:] for k in vars().keys() if k.startswith('t_') and k != 't_error'] +
              ['text'])

lexer = LexerBox().lexer
# TODO: If we ever need more than one lexer, have the class build the lexer
# once and stash it in a class var. Then clone from it on construction of
# future instances.
