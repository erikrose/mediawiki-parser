""" preprocessor
<definition>
# Codes

    LF                      : '
'
    CR                      : '
'
    EOL                     : LF / CR
    TAB                     : "	"
    L_BRACKET               : "["
    R_BRACKET               : "\]"
    L_BRACE                 : "{"                                                                   : drop
    R_BRACE                 : "}"                                                                   : drop
    SPACE                   : " "                                                                   : drop
    SPACETAB                : SPACE / TAB                                                           : drop
    SPACETABEOL             : SPACE / TAB / EOL                                                     : drop
    PIPE                    : "|"                                                                   : drop
    BANG                    : "!"                                                                   : drop
    EQUAL                   : "="                                                                   : drop
    LT                      : "<"                                                                   : drop
    GT                      : ">"                                                                   : drop
    HASH                    : "#"                                                                   : drop
    DASH                    : "-"                                                                   : drop
    AMP                     : "&"                                                                   : drop
    SEMICOLON               : ";"                                                                   : drop
    TEMPLATE_BEGIN          : L_BRACE{2}                                                            : drop
    TEMPLATE_END            : R_BRACE{2}                                                            : drop
    PARAMETER_BEGIN         : L_BRACE{3}                                                            : drop
    PARAMETER_END           : R_BRACE{3}                                                            : drop

# Predefined tags

    NOWIKI_BEGIN            : "<nowiki>"
    NOWIKI_END              : "</nowiki>"
    PRE_BEGIN               : "<pre>"
    PRE_END                 : "</pre>"
    special_tag             : NOWIKI_BEGIN/NOWIKI_END/PRE_BEGIN/PRE_END

# Characters

    any_char                : [\x20..\xff] / '/'
    esc_char                : L_BRACKET/R_BRACKET/PIPE/L_BRACE/R_BRACE/LT/GT/AMP/SEMICOLON
    raw_char                : !esc_char any_char
    raw_text                : (raw_char / TAB)+                                                     : join

# HTML comments
# HTML comments are totally ignored and do not appear in the final text

    comment_content         : ((!(DASH{2} GT) [\x20..\xff])+ / SPACETABEOL)*
    html_comment            : LT BANG DASH{2} comment_content DASH{2} GT                            : drop

# Text

    page_name               : raw_char+                                                             : join

# Template parameters
# Those parameters should be substituted by their value when the current page is a template
# or by their optional default value in any case

    parameter_id            : raw_char+                                                             : join
    parameter_value         : inline?                                                               : keep
    optional_default_value  : (PIPE SPACETABEOL* parameter_value)? SPACETABEOL*                     : liftNode
    template_parameter      : PARAMETER_BEGIN parameter_id optional_default_value PARAMETER_END     : substitute_template_parameter

# Links

    LINK_PIPE               : PIPE                                                                  : restore
    internal_link           : L_BRACKET{2} inline (LINK_PIPE inline)* R_BRACKET{2}                  : join
    external_link           : L_BRACKET inline (SPACE inline)* R_BRACKET                            : join
    link                    : internal_link / external_link

# Templates

    value_content           : (inline / (!(SPACETABEOL* (TEMPLATE_END / PIPE)) (any_char / EOL)))*  : keep
    parameter_value         : value_content SPACETABEOL*
    optional_value          : parameter_value?
    parameter_equal         : SPACETABEOL* EQUAL SPACETABEOL*
    parameter_name          : (!(esc_char/parameter_equal) raw_char)+                               : join
    named_parameter         : parameter_name parameter_equal optional_value
    standalone_parameter    : value_content?                                                        : join
    parameter               : SPACETABEOL* PIPE SPACETABEOL* (named_parameter/standalone_parameter) : liftValue
    parameters              : parameter*
    template                : TEMPLATE_BEGIN page_name parameters SPACETABEOL* TEMPLATE_END         : substitute_template

# inline allows to have templates/links inside templates/links

    structure               : link / template / template_parameter
    inline                  : (structure / raw_text)+                                               : @
    numbered_entity         : AMP HASH [0..9]+ SEMICOLON                                            : substitute_numbered_entity
    named_entity            : AMP [a..zA..Z]+ SEMICOLON                                             : substitute_named_entity
    entity                  : named_entity / numbered_entity

# Pre and nowiki tags
# Preformatted acts like nowiki (disables wikitext parsing)
# We allow any char without parsing them as long as the tag is not closed

    pre_text                : (!PRE_END any_char)*                                                  : join
    preformatted            : PRE_BEGIN pre_text PRE_END                                            : liftValue
    eol_to_space            : EOL*                                                                  : replace_by_space
    nowiki_text             : (!NOWIKI_END (any_char/eol_to_space))*                                : join
    nowiki                  : NOWIKI_BEGIN nowiki_text NOWIKI_END                                   : liftValue

# Text types

    styled_text             : template / template_parameter / entity
    not_styled_text         : html_comment / preformatted / nowiki
    allowed_char            : esc_char{1}                                                           : restore liftValue
    allowed_text            : raw_text / allowed_char
    wikitext                : (not_styled_text / styled_text / allowed_text / EOL)+                 : join

"""

from pijnu.library import *


def make_parser(actions=None):
    """Return a parser.

    The parser's toolset functions are (optionally) augmented (or overridden)
    by a map of additional ones passed in.

    """
    if actions is None:
        actions = {}

    # Start off with the imported pijnu library functions:
    toolset = globals().copy()

    parser = Parser()
    state = parser.state

### title: preprocessor ###
    
    
    def toolset_from_grammar():
        """Return a map of toolset functions hard-coded into the grammar."""
    ###   <toolset>
        def replace_by_space(node):
            node.value = ' '
        
    
        return locals().copy()
    
    toolset.update(toolset_from_grammar())
    toolset.update(actions)
    
    ###   <definition>
    # recursive pattern(s)
    inline = Recursive(name='inline')
    # Codes
    
    LF = Char('\n', expression="'\n'", name='LF')
    CR = Char('\n', expression="'\n'", name='CR')
    EOL = Choice([LF, CR], expression='LF / CR', name='EOL')
    TAB = Word('\t', expression='"\t"', name='TAB')
    L_BRACKET = Word('[', expression='"["', name='L_BRACKET')
    R_BRACKET = Word(']', expression='"\\]"', name='R_BRACKET')
    L_BRACE = Word('{', expression='"{"', name='L_BRACE')(toolset['drop'])
    R_BRACE = Word('}', expression='"}"', name='R_BRACE')(toolset['drop'])
    SPACE = Word(' ', expression='" "', name='SPACE')(toolset['drop'])
    SPACETAB = Choice([SPACE, TAB], expression='SPACE / TAB', name='SPACETAB')(toolset['drop'])
    SPACETABEOL = Choice([SPACE, TAB, EOL], expression='SPACE / TAB / EOL', name='SPACETABEOL')(toolset['drop'])
    PIPE = Word('|', expression='"|"', name='PIPE')(toolset['drop'])
    BANG = Word('!', expression='"!"', name='BANG')(toolset['drop'])
    EQUAL = Word('=', expression='"="', name='EQUAL')(toolset['drop'])
    LT = Word('<', expression='"<"', name='LT')(toolset['drop'])
    GT = Word('>', expression='">"', name='GT')(toolset['drop'])
    HASH = Word('#', expression='"#"', name='HASH')(toolset['drop'])
    DASH = Word('-', expression='"-"', name='DASH')(toolset['drop'])
    AMP = Word('&', expression='"&"', name='AMP')(toolset['drop'])
    SEMICOLON = Word(';', expression='";"', name='SEMICOLON')(toolset['drop'])
    TEMPLATE_BEGIN = Repetition(L_BRACE, numMin=2, numMax=2, expression='L_BRACE{2}', name='TEMPLATE_BEGIN')(toolset['drop'])
    TEMPLATE_END = Repetition(R_BRACE, numMin=2, numMax=2, expression='R_BRACE{2}', name='TEMPLATE_END')(toolset['drop'])
    PARAMETER_BEGIN = Repetition(L_BRACE, numMin=3, numMax=3, expression='L_BRACE{3}', name='PARAMETER_BEGIN')(toolset['drop'])
    PARAMETER_END = Repetition(R_BRACE, numMin=3, numMax=3, expression='R_BRACE{3}', name='PARAMETER_END')(toolset['drop'])
    
    # Predefined tags
    
    NOWIKI_BEGIN = Word('<nowiki>', expression='"<nowiki>"', name='NOWIKI_BEGIN')
    NOWIKI_END = Word('</nowiki>', expression='"</nowiki>"', name='NOWIKI_END')
    PRE_BEGIN = Word('<pre>', expression='"<pre>"', name='PRE_BEGIN')
    PRE_END = Word('</pre>', expression='"</pre>"', name='PRE_END')
    special_tag = Choice([NOWIKI_BEGIN, NOWIKI_END, PRE_BEGIN, PRE_END], expression='NOWIKI_BEGIN/NOWIKI_END/PRE_BEGIN/PRE_END', name='special_tag')
    
    # Characters
    
    any_char = Choice([Klass(u' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff', expression='[\\x20..\\xff]'), Char('/', expression="'/'")], expression="[\\x20..\\xff] / '/'", name='any_char')
    esc_char = Choice([L_BRACKET, R_BRACKET, PIPE, L_BRACE, R_BRACE, LT, GT, AMP, SEMICOLON], expression='L_BRACKET/R_BRACKET/PIPE/L_BRACE/R_BRACE/LT/GT/AMP/SEMICOLON', name='esc_char')
    raw_char = Sequence([NextNot(esc_char, expression='!esc_char'), any_char], expression='!esc_char any_char', name='raw_char')
    raw_text = Repetition(Choice([raw_char, TAB], expression='raw_char / TAB'), numMin=1, numMax=False, expression='(raw_char / TAB)+', name='raw_text')(toolset['join'])
    
    # HTML comments
    # HTML comments are totally ignored and do not appear in the final text
    
    comment_content = Repetition(Choice([Repetition(Sequence([NextNot(Sequence([Repetition(DASH, numMin=2, numMax=2, expression='DASH{2}'), GT], expression='DASH{2} GT'), expression='!(DASH{2} GT)'), Klass(u' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff', expression='[\\x20..\\xff]')], expression='!(DASH{2} GT) [\\x20..\\xff]'), numMin=1, numMax=False, expression='(!(DASH{2} GT) [\\x20..\\xff])+'), SPACETABEOL], expression='(!(DASH{2} GT) [\\x20..\\xff])+ / SPACETABEOL'), numMin=False, numMax=False, expression='((!(DASH{2} GT) [\\x20..\\xff])+ / SPACETABEOL)*', name='comment_content')
    html_comment = Sequence([LT, BANG, Repetition(DASH, numMin=2, numMax=2, expression='DASH{2}'), comment_content, Repetition(DASH, numMin=2, numMax=2, expression='DASH{2}'), GT], expression='LT BANG DASH{2} comment_content DASH{2} GT', name='html_comment')(toolset['drop'])
    
    # Text
    
    page_name = Repetition(raw_char, numMin=1, numMax=False, expression='raw_char+', name='page_name')(toolset['join'])
    
    # Template parameters
    # Those parameters should be substituted by their value when the current page is a template
    # or by their optional default value in any case
    
    parameter_id = Repetition(raw_char, numMin=1, numMax=False, expression='raw_char+', name='parameter_id')(toolset['join'])
    parameter_value = Option(inline, expression='inline?', name='parameter_value')(toolset['keep'])
    optional_default_value = Sequence([Option(Sequence([PIPE, Repetition(SPACETABEOL, numMin=False, numMax=False, expression='SPACETABEOL*'), parameter_value], expression='PIPE SPACETABEOL* parameter_value'), expression='(PIPE SPACETABEOL* parameter_value)?'), Repetition(SPACETABEOL, numMin=False, numMax=False, expression='SPACETABEOL*')], expression='(PIPE SPACETABEOL* parameter_value)? SPACETABEOL*', name='optional_default_value')(toolset['liftNode'])
    template_parameter = Sequence([PARAMETER_BEGIN, parameter_id, optional_default_value, PARAMETER_END], expression='PARAMETER_BEGIN parameter_id optional_default_value PARAMETER_END', name='template_parameter')(toolset['substitute_template_parameter'])
    
    # Links
    
    LINK_PIPE = Clone(PIPE, expression='PIPE', name='LINK_PIPE')(toolset['restore'])
    internal_link = Sequence([Repetition(L_BRACKET, numMin=2, numMax=2, expression='L_BRACKET{2}'), inline, Repetition(Sequence([LINK_PIPE, inline], expression='LINK_PIPE inline'), numMin=False, numMax=False, expression='(LINK_PIPE inline)*'), Repetition(R_BRACKET, numMin=2, numMax=2, expression='R_BRACKET{2}')], expression='L_BRACKET{2} inline (LINK_PIPE inline)* R_BRACKET{2}', name='internal_link')(toolset['join'])
    external_link = Sequence([L_BRACKET, inline, Repetition(Sequence([SPACE, inline], expression='SPACE inline'), numMin=False, numMax=False, expression='(SPACE inline)*'), R_BRACKET], expression='L_BRACKET inline (SPACE inline)* R_BRACKET', name='external_link')(toolset['join'])
    link = Choice([internal_link, external_link], expression='internal_link / external_link', name='link')
    
    # Templates
    
    value_content = Repetition(Choice([inline, Sequence([NextNot(Sequence([Repetition(SPACETABEOL, numMin=False, numMax=False, expression='SPACETABEOL*'), Choice([TEMPLATE_END, PIPE], expression='TEMPLATE_END / PIPE')], expression='SPACETABEOL* (TEMPLATE_END / PIPE)'), expression='!(SPACETABEOL* (TEMPLATE_END / PIPE))'), Choice([any_char, EOL], expression='any_char / EOL')], expression='!(SPACETABEOL* (TEMPLATE_END / PIPE)) (any_char / EOL)')], expression='inline / (!(SPACETABEOL* (TEMPLATE_END / PIPE)) (any_char / EOL))'), numMin=False, numMax=False, expression='(inline / (!(SPACETABEOL* (TEMPLATE_END / PIPE)) (any_char / EOL)))*', name='value_content')(toolset['keep'])
    parameter_value = Sequence([value_content, Repetition(SPACETABEOL, numMin=False, numMax=False, expression='SPACETABEOL*')], expression='value_content SPACETABEOL*', name='parameter_value')
    optional_value = Option(parameter_value, expression='parameter_value?', name='optional_value')
    parameter_equal = Sequence([Repetition(SPACETABEOL, numMin=False, numMax=False, expression='SPACETABEOL*'), EQUAL, Repetition(SPACETABEOL, numMin=False, numMax=False, expression='SPACETABEOL*')], expression='SPACETABEOL* EQUAL SPACETABEOL*', name='parameter_equal')
    parameter_name = Repetition(Sequence([NextNot(Choice([esc_char, parameter_equal], expression='esc_char/parameter_equal'), expression='!(esc_char/parameter_equal)'), raw_char], expression='!(esc_char/parameter_equal) raw_char'), numMin=1, numMax=False, expression='(!(esc_char/parameter_equal) raw_char)+', name='parameter_name')(toolset['join'])
    named_parameter = Sequence([parameter_name, parameter_equal, optional_value], expression='parameter_name parameter_equal optional_value', name='named_parameter')
    standalone_parameter = Option(value_content, expression='value_content?', name='standalone_parameter')(toolset['join'])
    parameter = Sequence([Repetition(SPACETABEOL, numMin=False, numMax=False, expression='SPACETABEOL*'), PIPE, Repetition(SPACETABEOL, numMin=False, numMax=False, expression='SPACETABEOL*'), Choice([named_parameter, standalone_parameter], expression='named_parameter/standalone_parameter')], expression='SPACETABEOL* PIPE SPACETABEOL* (named_parameter/standalone_parameter)', name='parameter')(toolset['liftValue'])
    parameters = Repetition(parameter, numMin=False, numMax=False, expression='parameter*', name='parameters')
    template = Sequence([TEMPLATE_BEGIN, page_name, parameters, Repetition(SPACETABEOL, numMin=False, numMax=False, expression='SPACETABEOL*'), TEMPLATE_END], expression='TEMPLATE_BEGIN page_name parameters SPACETABEOL* TEMPLATE_END', name='template')(toolset['substitute_template'])
    
    # inline allows to have templates/links inside templates/links
    
    structure = Choice([link, template, template_parameter], expression='link / template / template_parameter', name='structure')
    inline **= Repetition(Choice([structure, raw_text], expression='structure / raw_text'), numMin=1, numMax=False, expression='(structure / raw_text)+', name='inline')
    numbered_entity = Sequence([AMP, HASH, Repetition(Klass(u'0123456789', expression='[0..9]'), numMin=1, numMax=False, expression='[0..9]+'), SEMICOLON], expression='AMP HASH [0..9]+ SEMICOLON', name='numbered_entity')(toolset['substitute_numbered_entity'])
    named_entity = Sequence([AMP, Repetition(Klass(u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', expression='[a..zA..Z]'), numMin=1, numMax=False, expression='[a..zA..Z]+'), SEMICOLON], expression='AMP [a..zA..Z]+ SEMICOLON', name='named_entity')(toolset['substitute_named_entity'])
    entity = Choice([named_entity, numbered_entity], expression='named_entity / numbered_entity', name='entity')
    
    # Pre and nowiki tags
    # Preformatted acts like nowiki (disables wikitext parsing)
    # We allow any char without parsing them as long as the tag is not closed
    
    pre_text = Repetition(Sequence([NextNot(PRE_END, expression='!PRE_END'), any_char], expression='!PRE_END any_char'), numMin=False, numMax=False, expression='(!PRE_END any_char)*', name='pre_text')(toolset['join'])
    preformatted = Sequence([PRE_BEGIN, pre_text, PRE_END], expression='PRE_BEGIN pre_text PRE_END', name='preformatted')(toolset['liftValue'])
    eol_to_space = Repetition(EOL, numMin=False, numMax=False, expression='EOL*', name='eol_to_space')(toolset['replace_by_space'])
    nowiki_text = Repetition(Sequence([NextNot(NOWIKI_END, expression='!NOWIKI_END'), Choice([any_char, eol_to_space], expression='any_char/eol_to_space')], expression='!NOWIKI_END (any_char/eol_to_space)'), numMin=False, numMax=False, expression='(!NOWIKI_END (any_char/eol_to_space))*', name='nowiki_text')(toolset['join'])
    nowiki = Sequence([NOWIKI_BEGIN, nowiki_text, NOWIKI_END], expression='NOWIKI_BEGIN nowiki_text NOWIKI_END', name='nowiki')(toolset['liftValue'])
    
    # Text types
    
    styled_text = Choice([template, template_parameter, entity], expression='template / template_parameter / entity', name='styled_text')
    not_styled_text = Choice([html_comment, preformatted, nowiki], expression='html_comment / preformatted / nowiki', name='not_styled_text')
    allowed_char = Repetition(esc_char, numMin=1, numMax=1, expression='esc_char{1}', name='allowed_char')(toolset['restore'], toolset['liftValue'])
    allowed_text = Choice([raw_text, allowed_char], expression='raw_text / allowed_char', name='allowed_text')
    wikitext = Repetition(Choice([not_styled_text, styled_text, allowed_text, EOL], expression='not_styled_text / styled_text / allowed_text / EOL'), numMin=1, numMax=False, expression='(not_styled_text / styled_text / allowed_text / EOL)+', name='wikitext')(toolset['join'])

    symbols = locals().copy()
    symbols.update(actions)
    parser._recordPatterns(symbols)
    parser._setTopPattern("wikitext")
    parser.grammarTitle = "preprocessor"
    parser.filename = "preprocessorParser.py"

    return parser
