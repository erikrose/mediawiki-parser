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

    t_html_entity_hex = r'&\#x[0-9a-fA-F]+;'
    t_html_entity_dec = r'&\#[0-9]+;'
    t_html_entity_sym = r'&(?:' + '|'.join(html_entities.keys()) + ');'
    # ^ Optimize by using a hash table? By putting common entities first?

    def t_error(self, t):
        raise LexError('Illegal character', t.value[0])
        #t.lexer.skip(1)

    # Everything after the t_ in anything that starts with t_:
    tokens = [k[2:] for k in vars().keys() if k.startswith('t_') and k != 't_error']

lexer = LexerBox().lexer
# TODO: If we ever need more than one lexer, have the class build the lexer
# once and stash it in a class var. Then clone from it on construction of
# future instances.
