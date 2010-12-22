"""What will eventually become a MediaWiki lexer

Based on the work at http://www.mediawiki.org/wiki/Markup_spec/BNF

"""
from ply import lex


class LexerBox(object):
    """A container to group token definitions, hold state, & afford subclassing

    Don't instantiate these; that's expensive. Instead, use the module-level
    instance in `lexer`.

    """
    def __init__(self):
        """Generate the parsing tables and such. This is expensive."""
        self.lexer = lex.lex(module=self)

    # Fundamental elements
    # (http://www.mediawiki.org/wiki/Markup_spec/BNF/Fundamental_elements):

    def t_newline(self, t):
        r'(?:\r\n|\n\r|\r|\n)'
        return t

    #def t_newlines(t): >=1 t_newline. In the BNF but possibly unneeded.

    def t_error(self, t):
        print "Illegal character: '%s'" % t.value[0]
        t.lexer.skip(1)

    # Everything after the t_ in anything that starts with t_:
    tokens = [k[2:] for k in vars().keys() if k.startswith('t_') and k != 't_error']

lexer = LexerBox().lexer
# TODO: If we ever need more than one lexer, have the class build the lexer
# once and stash it in a class var. Then clone from it on construction of
# future instances.
