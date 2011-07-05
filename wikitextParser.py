""" wikitext
<definition>
# Codes

    LF                      : '
'
    CR                      : '
'
    EOL                     : LF / CR                                                               : drop
    L_BRACKET               : "["                                                                   : drop
    R_BRACKET               : "\]"                                                                  : drop
    L_BRACE                 : "{"                                                                   : drop
    R_BRACE                 : "}"                                                                   : drop
    SPACE                   : " "                                                                   : drop
    TAB                     : "	"                                                                   : drop
    SPACETAB                : SPACE / TAB                                                           : drop
    SPACETABEOL             : SPACE / TAB / EOL                                                     : drop
    AMP                     : "&"                                                                   : drop
    PIPE                    : "|"                                                                   : drop
    BANG                    : "!"                                                                   : drop
    EQUAL                   : "="                                                                   : drop
    BULLET                  : "*"                                                                   : drop
    HASH                    : "#"                                                                   : drop
    COLON                   : ":"                                                                   : drop
    LT                      : "<"                                                                   : drop
    GT                      : ">"                                                                   : drop
    SLASH                   : "/"                                                                   : drop
    SEMICOLON               : ";"                                                                   : drop
    DASH                    : "-"                                                                   : drop
    TABLE_BEGIN             : "{|"                                                                  : drop
    TABLE_END               : "|}"                                                                  : drop
    TABLE_NEWLINE           : "|-"                                                                  : drop
    TABLE_TITLE             : "|+"                                                                  : drop
    QUOTE                   : "\""                                                                  : drop
    APOSTROPHE              : "\'"                                                                  : drop
    TITLE6_BEGIN            : EQUAL{6}                                                              : drop
    TITLE5_BEGIN            : EQUAL{5}                                                              : drop
    TITLE4_BEGIN            : EQUAL{4}                                                              : drop
    TITLE3_BEGIN            : EQUAL{3}                                                              : drop
    TITLE2_BEGIN            : EQUAL{2}                                                              : drop
    TITLE1_BEGIN            : EQUAL{1}                                                              : drop
    TITLE6_END              : EQUAL{6} SPACETAB* EOL                                                : drop
    TITLE5_END              : EQUAL{5} SPACETAB* EOL                                                : drop
    TITLE4_END              : EQUAL{4} SPACETAB* EOL                                                : drop
    TITLE3_END              : EQUAL{3} SPACETAB* EOL                                                : drop
    TITLE2_END              : EQUAL{2} SPACETAB* EOL                                                : drop
    TITLE1_END              : EQUAL{1} SPACETAB* EOL                                                : drop
    TEMPLATE_BEGIN          : L_BRACE{2}                                                            : drop
    TEMPLATE_END            : R_BRACE{2}                                                            : drop
    PARAMETER_BEGIN         : L_BRACE{3}                                                            : drop
    PARAMETER_END           : R_BRACE{3}                                                            : drop
    LINK_BEGIN              : L_BRACKET{2}                                                          : drop
    LINK_END                : R_BRACKET{2}                                                          : drop

# Protocols

    HTTPS                   : "https://"                                                            : liftValue
    HTTP                    : "http://"                                                             : liftValue
    FTP                     : "ftp://"                                                              : liftValue
    protocol                : HTTPS / HTTP / FTP                                                    : liftValue

# Predefined tags

    NOWIKI_BEGIN            : "<nowiki>"                                                            : drop
    NOWIKI_END              : "</nowiki>"                                                           : drop
    PRE_BEGIN               : "<pre>"                                                               : drop
    PRE_END                 : "</pre>"                                                              : drop
    special_tag             : NOWIKI_BEGIN/NOWIKI_END/PRE_BEGIN/PRE_END

# Characters

    escChar                 : L_BRACKET/R_BRACKET/protocol/PIPE/L_BRACE/R_BRACE/LT/GT/SLASH/AMP/SEMICOLON
    titleEnd                : TITLE6_END/TITLE5_END/TITLE4_END/TITLE3_END/TITLE2_END/TITLE1_END
    escSeq                  : special_tag / escChar / titleEnd
    rawChar                 : !escSeq [\x20..\xff]
    rawText                 : rawChar+                                                              : join parse_all_quotes
    alpha_num               : [a..zA..Z0..9]
    alpha_num_text          : alpha_num+                                                            : join
    anyChar                 : [\x20..\xff]
    anyText                 : anyChar+                                                              : join

# HTML tags

    value_quote             : QUOTE ((!(GT/QUOTE) anyChar) / TAB)+ QUOTE                            : join
    value_apostrophe        : APOSTROPHE ((!(GT/APOSTROPHE) anyChar) / TAB)+ APOSTROPHE             : join
    value_noquote           : (!(GT/SPACETAB/SLASH) rawChar)+                                       : join
    attribute_value         : (EQUAL (value_quote / value_apostrophe / value_noquote))?             : liftNode
    attribute_name          : (!(EQUAL/SLASH/SPACETAB) rawChar)+                                    : join
    tag_name                : (!(SPACE/SLASH) rawChar)+                                             : join
    optional_attribute      : SPACETABEOL+ attribute_name attribute_value
    optional_attributes     : optional_attribute*
    tag_open                : LT tag_name optional_attributes SPACETABEOL* GT
    tag_close               : LT SLASH tag_name GT
    tag_autoclose           : LT tag_name optional_attributes SPACETABEOL* SLASH GT
    tag                     : tag_autoclose / tag_open / tag_close

# HTML entities

    entity                  : AMP alpha_num_text SEMICOLON                                          : liftValue

# HTML comments

    # HTML comments are totally ignored and do not appear in the final text
    comment_content         : ((!(DASH{2} GT) [\x20..\xff])+ / SPACETABEOL)*
    html_comment            : LT BANG DASH{2} comment_content DASH{2} GT                            : drop
    optional_comment        : html_comment*

# Text

    page_name               : rawChar+                                                              : join
# TODO: allow IPv6 addresses (http://[::1]/etc)
    address                 : (!(QUOTE/R_BRACKET) [\x21..\xff])+                                    : liftValue
    url                     : protocol address                                                      : join

# Links

    allowed_in_link         : (!(R_BRACKET/PIPE) escChar)+                                          : restore join
    link_text               : (cleanInline / allowed_in_link)*                                      : liftValue
    link_argument           : PIPE link_text                                                        : liftValue
    link_arguments          : link_argument*
    internal_link           : LINK_BEGIN page_name link_arguments LINK_END                          : liftValue
    optional_link_text      : SPACETAB+ link_text                                                   : liftValue
    external_link           : L_BRACKET url optional_link_text? R_BRACKET 
    link                    : internal_link / external_link

# Templates

    value                   : EQUAL cleanInline                                                     : liftValue
    optional_value          : value*                                                                : liftValue
    parameter_name          : (!EQUAL rawChar)+                                                     : join
    parameter_with_value    : parameter_name optional_value                                         : liftValue
    parameter               : SPACETABEOL* PIPE SPACETABEOL* (parameter_with_value / cleanInline)   : liftValue
    parameters              : parameter*
    template                : TEMPLATE_BEGIN page_name parameters SPACETABEOL* TEMPLATE_END

# Template parameters

    # Those parameters should be substituted by their value when the current page is a template or by their optional default value in any case
    template_parameter_id   : (!(R_BRACE/PIPE) anyChar)+                                            : join
    default_value           : (!R_BRACE anyChar)+                                                   : join
    optional_default_value  : (PIPE default_value)?                                                 : liftNode
    template_parameter      : PARAMETER_BEGIN template_parameter_id optional_default_value PARAMETER_END

# Pre and nowiki tags

    # Preformatted acts like nowiki (disables wikitext parsing)
    pre_text                : (!PRE_END anyChar)*                                                   : join
    preformatted            : PRE_BEGIN pre_text PRE_END                                            : liftValue
    # We allow any char without parsing them as long as the tag is not closed
    eol_to_space            : EOL*                                                                  : replace_by_space
    nowiki_text             : (!NOWIKI_END (anyChar/eol_to_space))*                                 : join
    nowiki                  : NOWIKI_BEGIN nowiki_text NOWIKI_END                                   : liftValue

# Text types

    styled_text             : link / url / template_parameter / template / html_comment / tag / entity
    not_styled_text         : preformatted / nowiki
    allowedChar             : escChar{1}                                                            : restore liftValue
    allowedText             : rawText / allowedChar
    cleanInline             : (not_styled_text / styled_text / rawText)+                            : @
    inline                  : (not_styled_text / styled_text / allowedText)+                        : @

# Paragraphs

    special_line_begin      : SPACE/EQUAL/BULLET/HASH/COLON/DASH{4}/TABLE_BEGIN/SEMICOLON
    paragraph_line          : !special_line_begin inline EOL                                        : liftValue
    blank_paragraph         : EOL{2}                                                                : drop keep
    paragraph               : paragraph_line+                                                       : liftValue
    paragraphs              : (blank_paragraph/EOL/paragraph)+

# Titles

    title6                  : TITLE6_BEGIN inline TITLE6_END                                        : liftValue
    title5                  : TITLE5_BEGIN inline TITLE5_END                                        : liftValue
    title4                  : TITLE4_BEGIN inline TITLE4_END                                        : liftValue
    title3                  : TITLE3_BEGIN inline TITLE3_END                                        : liftValue
    title2                  : TITLE2_BEGIN inline TITLE2_END                                        : liftValue
    title1                  : TITLE1_BEGIN inline TITLE1_END                                        : liftValue
    title                   : title6 / title5 / title4 / title3 / title2 / title1

# Lists

    listChar                : BULLET / HASH / COLON / SEMICOLON
    listLeafContent         : !listChar inline EOL                                                  : liftValue

    bulletListLeaf          : BULLET optional_comment listLeafContent                               : liftValue
    bulletSubList           : BULLET optional_comment listItem                                      : @

    numberListLeaf          : HASH optional_comment listLeafContent                                 : liftValue
    numberSubList           : HASH optional_comment listItem                                        : @

    colonListLeaf           : COLON optional_comment listLeafContent                                : liftValue
    colonSubList            : COLON optional_comment listItem                                       : @

    semiColonListLeaf       : SEMICOLON optional_comment listLeafContent                            : liftValue
    semiColonSubList        : SEMICOLON optional_comment listItem                                   : @

    listLeaf                : semiColonListLeaf / colonListLeaf / numberListLeaf / bulletListLeaf   : @
    subList                 : semiColonSubList / colonSubList / numberSubList / bulletSubList       : @
    listItem                : subList / listLeaf                                                    : @
    list                    : listItem+

# Preformatted

    EOL_or_not              : EOL{0..1}                                                             : drop
    preformattedLine        : SPACE inline EOL                                                      : liftValue
    preformattedLines       : preformattedLine+
    preformattedText        : inline EOL_or_not                                                     : liftValue
    preformattedParagraph   : PRE_BEGIN EOL preformattedText PRE_END EOL
    preformattedGroup       : preformattedParagraph / preformattedLines

# Special lines

    horizontal_rule         : DASH{4} DASH* inline* EOL                                             : liftValue keep

    # This should never happen
    invalid_line            : anyText EOL                                                           : liftValue

# Tables

    HTML_value_quote        : QUOTE ((!(GT/QUOTE) anyChar) / TAB)+ QUOTE                            : join
    HTML_value_apostrophe   : APOSTROPHE ((!(GT/APOSTROPHE) anyChar) / TAB)+ APOSTROPHE             : join
    HTML_value_noquote      : (!(GT/SPACETAB/SLASH) rawChar)+                                       : join
    HTML_value              : HTML_value_quote / HTML_value_apostrophe / HTML_value_noquote
    HTML_name               : (!(EQUAL/SLASH/SPACETAB) rawChar)+                                    : join
    HTML_attribute          : SPACETAB* HTML_name EQUAL HTML_value SPACETAB*
    HTML_attributes         : HTML_attribute*
    wikiTableParametersPipe : (SPACETAB* HTML_attribute+ SPACETAB* PIPE !PIPE)?                     : liftNode
    wikiTableParameters     : (HTML_attribute / cleanInline)+                                       : liftValue
    wikiTableParameter      : wikiTableParametersPipe{0..1}                                         : liftValue
    wikiTableCellContent    : cleanInline*
    wikiTableFirstCell      : wikiTableParameter wikiTableCellContent                               : liftNode
    wikiTableOtherCell      : (PIPE{2} wikiTableFirstCell)*                                         : liftValue liftNode
    wikiTableLineCells      : PIPE wikiTableFirstCell wikiTableOtherCell EOL                        : liftValue
    wikiTableLineHeader     : BANG wikiTableFirstCell wikiTableOtherCell EOL                        : liftValue
    wikiTableEmptyCell      : PIPE EOL                                                              : keep
    wikiTableParamLineBreak : TABLE_NEWLINE wikiTableParameters* EOL                                : keep liftValue
    wikiTableLineBreak      : TABLE_NEWLINE EOL                                                     : keep
    wikiTableTitle          : TABLE_TITLE wikiTableParameter wikiTableCellContent EOL               : liftValue
    wikiTableSpecialLine    : wikiTableTitle / wikiTableLineBreak / wikiTableParamLineBreak
    wikiTableNormalLine     : wikiTableLineCells / wikiTableLineHeader / wikiTableEmptyCell
    wikiTableLine           : !TABLE_END (wikiTableSpecialLine / wikiTableNormalLine)               : liftNode
    wikiTableContent        : (wikiTableLine / wikiTable / EOL)*                                    : liftNode
    wikiTableBegin          : TABLE_BEGIN wikiTableParameters*                                      : liftValue
    wikiTable               : wikiTableBegin SPACETABEOL* wikiTableContent TABLE_END EOL            : @ liftValue

# Top pattern

    body                    : optional_comment (list / horizontal_rule / preformattedGroup / title / wikiTable / EOL / paragraphs / invalid_line / EOL)+ : liftValue

"""



from pijnu.library import *

wikitextParser = Parser()
state = wikitextParser.state



### title: wikitext ###


###   <toolset>
def parse_all_quotes(node):
    from apostrophes import parseQuotes
    node.value = parseQuotes(node.value)

def replace_by_space(node):
    node.value = ' '

###   <definition>
# recursive pattern(s)
wikiTable = Recursive(name='wikiTable')
listItem = Recursive(name='listItem')
subList = Recursive(name='subList')
listLeaf = Recursive(name='listLeaf')
semiColonSubList = Recursive(name='semiColonSubList')
colonSubList = Recursive(name='colonSubList')
numberSubList = Recursive(name='numberSubList')
bulletSubList = Recursive(name='bulletSubList')
inline = Recursive(name='inline')
cleanInline = Recursive(name='cleanInline')
# Codes

LF = Char('\n', expression="'\n'", name='LF')
CR = Char('\n', expression="'\n'", name='CR')
EOL = Choice([LF, CR], expression='LF / CR', name='EOL')(drop)
L_BRACKET = Word('[', expression='"["', name='L_BRACKET')(drop)
R_BRACKET = Word(']', expression='"\\]"', name='R_BRACKET')(drop)
L_BRACE = Word('{', expression='"{"', name='L_BRACE')(drop)
R_BRACE = Word('}', expression='"}"', name='R_BRACE')(drop)
SPACE = Word(' ', expression='" "', name='SPACE')(drop)
TAB = Word('\t', expression='"\t"', name='TAB')(drop)
SPACETAB = Choice([SPACE, TAB], expression='SPACE / TAB', name='SPACETAB')(drop)
SPACETABEOL = Choice([SPACE, TAB, EOL], expression='SPACE / TAB / EOL', name='SPACETABEOL')(drop)
AMP = Word('&', expression='"&"', name='AMP')(drop)
PIPE = Word('|', expression='"|"', name='PIPE')(drop)
BANG = Word('!', expression='"!"', name='BANG')(drop)
EQUAL = Word('=', expression='"="', name='EQUAL')(drop)
BULLET = Word('*', expression='"*"', name='BULLET')(drop)
HASH = Word('#', expression='"#"', name='HASH')(drop)
COLON = Word(':', expression='":"', name='COLON')(drop)
LT = Word('<', expression='"<"', name='LT')(drop)
GT = Word('>', expression='">"', name='GT')(drop)
SLASH = Word('/', expression='"/"', name='SLASH')(drop)
SEMICOLON = Word(';', expression='";"', name='SEMICOLON')(drop)
DASH = Word('-', expression='"-"', name='DASH')(drop)
TABLE_BEGIN = Word('{|', expression='"{|"', name='TABLE_BEGIN')(drop)
TABLE_END = Word('|}', expression='"|}"', name='TABLE_END')(drop)
TABLE_NEWLINE = Word('|-', expression='"|-"', name='TABLE_NEWLINE')(drop)
TABLE_TITLE = Word('|+', expression='"|+"', name='TABLE_TITLE')(drop)
QUOTE = Word('"', expression='"\\""', name='QUOTE')(drop)
APOSTROPHE = Word("'", expression='"\\\'"', name='APOSTROPHE')(drop)
TITLE6_BEGIN = Repetition(EQUAL, numMin=6, numMax=6, expression='EQUAL{6}', name='TITLE6_BEGIN')(drop)
TITLE5_BEGIN = Repetition(EQUAL, numMin=5, numMax=5, expression='EQUAL{5}', name='TITLE5_BEGIN')(drop)
TITLE4_BEGIN = Repetition(EQUAL, numMin=4, numMax=4, expression='EQUAL{4}', name='TITLE4_BEGIN')(drop)
TITLE3_BEGIN = Repetition(EQUAL, numMin=3, numMax=3, expression='EQUAL{3}', name='TITLE3_BEGIN')(drop)
TITLE2_BEGIN = Repetition(EQUAL, numMin=2, numMax=2, expression='EQUAL{2}', name='TITLE2_BEGIN')(drop)
TITLE1_BEGIN = Repetition(EQUAL, numMin=1, numMax=1, expression='EQUAL{1}', name='TITLE1_BEGIN')(drop)
TITLE6_END = Sequence([Repetition(EQUAL, numMin=6, numMax=6, expression='EQUAL{6}'), Repetition(SPACETAB, numMin=False, numMax=False, expression='SPACETAB*'), EOL], expression='EQUAL{6} SPACETAB* EOL', name='TITLE6_END')(drop)
TITLE5_END = Sequence([Repetition(EQUAL, numMin=5, numMax=5, expression='EQUAL{5}'), Repetition(SPACETAB, numMin=False, numMax=False, expression='SPACETAB*'), EOL], expression='EQUAL{5} SPACETAB* EOL', name='TITLE5_END')(drop)
TITLE4_END = Sequence([Repetition(EQUAL, numMin=4, numMax=4, expression='EQUAL{4}'), Repetition(SPACETAB, numMin=False, numMax=False, expression='SPACETAB*'), EOL], expression='EQUAL{4} SPACETAB* EOL', name='TITLE4_END')(drop)
TITLE3_END = Sequence([Repetition(EQUAL, numMin=3, numMax=3, expression='EQUAL{3}'), Repetition(SPACETAB, numMin=False, numMax=False, expression='SPACETAB*'), EOL], expression='EQUAL{3} SPACETAB* EOL', name='TITLE3_END')(drop)
TITLE2_END = Sequence([Repetition(EQUAL, numMin=2, numMax=2, expression='EQUAL{2}'), Repetition(SPACETAB, numMin=False, numMax=False, expression='SPACETAB*'), EOL], expression='EQUAL{2} SPACETAB* EOL', name='TITLE2_END')(drop)
TITLE1_END = Sequence([Repetition(EQUAL, numMin=1, numMax=1, expression='EQUAL{1}'), Repetition(SPACETAB, numMin=False, numMax=False, expression='SPACETAB*'), EOL], expression='EQUAL{1} SPACETAB* EOL', name='TITLE1_END')(drop)
TEMPLATE_BEGIN = Repetition(L_BRACE, numMin=2, numMax=2, expression='L_BRACE{2}', name='TEMPLATE_BEGIN')(drop)
TEMPLATE_END = Repetition(R_BRACE, numMin=2, numMax=2, expression='R_BRACE{2}', name='TEMPLATE_END')(drop)
PARAMETER_BEGIN = Repetition(L_BRACE, numMin=3, numMax=3, expression='L_BRACE{3}', name='PARAMETER_BEGIN')(drop)
PARAMETER_END = Repetition(R_BRACE, numMin=3, numMax=3, expression='R_BRACE{3}', name='PARAMETER_END')(drop)
LINK_BEGIN = Repetition(L_BRACKET, numMin=2, numMax=2, expression='L_BRACKET{2}', name='LINK_BEGIN')(drop)
LINK_END = Repetition(R_BRACKET, numMin=2, numMax=2, expression='R_BRACKET{2}', name='LINK_END')(drop)

# Protocols

HTTPS = Word('https://', expression='"https://"', name='HTTPS')(liftValue)
HTTP = Word('http://', expression='"http://"', name='HTTP')(liftValue)
FTP = Word('ftp://', expression='"ftp://"', name='FTP')(liftValue)
protocol = Choice([HTTPS, HTTP, FTP], expression='HTTPS / HTTP / FTP', name='protocol')(liftValue)

# Predefined tags

NOWIKI_BEGIN = Word('<nowiki>', expression='"<nowiki>"', name='NOWIKI_BEGIN')(drop)
NOWIKI_END = Word('</nowiki>', expression='"</nowiki>"', name='NOWIKI_END')(drop)
PRE_BEGIN = Word('<pre>', expression='"<pre>"', name='PRE_BEGIN')(drop)
PRE_END = Word('</pre>', expression='"</pre>"', name='PRE_END')(drop)
special_tag = Choice([NOWIKI_BEGIN, NOWIKI_END, PRE_BEGIN, PRE_END], expression='NOWIKI_BEGIN/NOWIKI_END/PRE_BEGIN/PRE_END', name='special_tag')

# Characters

escChar = Choice([L_BRACKET, R_BRACKET, protocol, PIPE, L_BRACE, R_BRACE, LT, GT, SLASH, AMP, SEMICOLON], expression='L_BRACKET/R_BRACKET/protocol/PIPE/L_BRACE/R_BRACE/LT/GT/SLASH/AMP/SEMICOLON', name='escChar')
titleEnd = Choice([TITLE6_END, TITLE5_END, TITLE4_END, TITLE3_END, TITLE2_END, TITLE1_END], expression='TITLE6_END/TITLE5_END/TITLE4_END/TITLE3_END/TITLE2_END/TITLE1_END', name='titleEnd')
escSeq = Choice([special_tag, escChar, titleEnd], expression='special_tag / escChar / titleEnd', name='escSeq')
rawChar = Sequence([NextNot(escSeq, expression='!escSeq'), Klass(u' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff', expression='[\\x20..\\xff]')], expression='!escSeq [\\x20..\\xff]', name='rawChar')
rawText = Repetition(rawChar, numMin=1, numMax=False, expression='rawChar+', name='rawText')(join, parse_all_quotes)
alpha_num = Klass(u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', expression='[a..zA..Z0..9]', name='alpha_num')
alpha_num_text = Repetition(alpha_num, numMin=1, numMax=False, expression='alpha_num+', name='alpha_num_text')(join)
anyChar = Klass(u' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff', expression='[\\x20..\\xff]', name='anyChar')
anyText = Repetition(anyChar, numMin=1, numMax=False, expression='anyChar+', name='anyText')(join)

# HTML tags

value_quote = Sequence([QUOTE, Repetition(Choice([Sequence([NextNot(Choice([GT, QUOTE], expression='GT/QUOTE'), expression='!(GT/QUOTE)'), anyChar], expression='!(GT/QUOTE) anyChar'), TAB], expression='(!(GT/QUOTE) anyChar) / TAB'), numMin=1, numMax=False, expression='((!(GT/QUOTE) anyChar) / TAB)+'), QUOTE], expression='QUOTE ((!(GT/QUOTE) anyChar) / TAB)+ QUOTE', name='value_quote')(join)
value_apostrophe = Sequence([APOSTROPHE, Repetition(Choice([Sequence([NextNot(Choice([GT, APOSTROPHE], expression='GT/APOSTROPHE'), expression='!(GT/APOSTROPHE)'), anyChar], expression='!(GT/APOSTROPHE) anyChar'), TAB], expression='(!(GT/APOSTROPHE) anyChar) / TAB'), numMin=1, numMax=False, expression='((!(GT/APOSTROPHE) anyChar) / TAB)+'), APOSTROPHE], expression='APOSTROPHE ((!(GT/APOSTROPHE) anyChar) / TAB)+ APOSTROPHE', name='value_apostrophe')(join)
value_noquote = Repetition(Sequence([NextNot(Choice([GT, SPACETAB, SLASH], expression='GT/SPACETAB/SLASH'), expression='!(GT/SPACETAB/SLASH)'), rawChar], expression='!(GT/SPACETAB/SLASH) rawChar'), numMin=1, numMax=False, expression='(!(GT/SPACETAB/SLASH) rawChar)+', name='value_noquote')(join)
attribute_value = Option(Sequence([EQUAL, Choice([value_quote, value_apostrophe, value_noquote], expression='value_quote / value_apostrophe / value_noquote')], expression='EQUAL (value_quote / value_apostrophe / value_noquote)'), expression='(EQUAL (value_quote / value_apostrophe / value_noquote))?', name='attribute_value')(liftNode)
attribute_name = Repetition(Sequence([NextNot(Choice([EQUAL, SLASH, SPACETAB], expression='EQUAL/SLASH/SPACETAB'), expression='!(EQUAL/SLASH/SPACETAB)'), rawChar], expression='!(EQUAL/SLASH/SPACETAB) rawChar'), numMin=1, numMax=False, expression='(!(EQUAL/SLASH/SPACETAB) rawChar)+', name='attribute_name')(join)
tag_name = Repetition(Sequence([NextNot(Choice([SPACE, SLASH], expression='SPACE/SLASH'), expression='!(SPACE/SLASH)'), rawChar], expression='!(SPACE/SLASH) rawChar'), numMin=1, numMax=False, expression='(!(SPACE/SLASH) rawChar)+', name='tag_name')(join)
optional_attribute = Sequence([Repetition(SPACETABEOL, numMin=1, numMax=False, expression='SPACETABEOL+'), attribute_name, attribute_value], expression='SPACETABEOL+ attribute_name attribute_value', name='optional_attribute')
optional_attributes = Repetition(optional_attribute, numMin=False, numMax=False, expression='optional_attribute*', name='optional_attributes')
tag_open = Sequence([LT, tag_name, optional_attributes, Repetition(SPACETABEOL, numMin=False, numMax=False, expression='SPACETABEOL*'), GT], expression='LT tag_name optional_attributes SPACETABEOL* GT', name='tag_open')
tag_close = Sequence([LT, SLASH, tag_name, GT], expression='LT SLASH tag_name GT', name='tag_close')
tag_autoclose = Sequence([LT, tag_name, optional_attributes, Repetition(SPACETABEOL, numMin=False, numMax=False, expression='SPACETABEOL*'), SLASH, GT], expression='LT tag_name optional_attributes SPACETABEOL* SLASH GT', name='tag_autoclose')
tag = Choice([tag_autoclose, tag_open, tag_close], expression='tag_autoclose / tag_open / tag_close', name='tag')

# HTML entities

entity = Sequence([AMP, alpha_num_text, SEMICOLON], expression='AMP alpha_num_text SEMICOLON', name='entity')(liftValue)

# HTML comments

    # HTML comments are totally ignored and do not appear in the final text
comment_content = Repetition(Choice([Repetition(Sequence([NextNot(Sequence([Repetition(DASH, numMin=2, numMax=2, expression='DASH{2}'), GT], expression='DASH{2} GT'), expression='!(DASH{2} GT)'), Klass(u' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff', expression='[\\x20..\\xff]')], expression='!(DASH{2} GT) [\\x20..\\xff]'), numMin=1, numMax=False, expression='(!(DASH{2} GT) [\\x20..\\xff])+'), SPACETABEOL], expression='(!(DASH{2} GT) [\\x20..\\xff])+ / SPACETABEOL'), numMin=False, numMax=False, expression='((!(DASH{2} GT) [\\x20..\\xff])+ / SPACETABEOL)*', name='comment_content')
html_comment = Sequence([LT, BANG, Repetition(DASH, numMin=2, numMax=2, expression='DASH{2}'), comment_content, Repetition(DASH, numMin=2, numMax=2, expression='DASH{2}'), GT], expression='LT BANG DASH{2} comment_content DASH{2} GT', name='html_comment')(drop)
optional_comment = Repetition(html_comment, numMin=False, numMax=False, expression='html_comment*', name='optional_comment')

# Text

page_name = Repetition(rawChar, numMin=1, numMax=False, expression='rawChar+', name='page_name')(join)
# TODO: allow IPv6 addresses (http://[::1]/etc)
address = Repetition(Sequence([NextNot(Choice([QUOTE, R_BRACKET], expression='QUOTE/R_BRACKET'), expression='!(QUOTE/R_BRACKET)'), Klass(u'!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff', expression='[\\x21..\\xff]')], expression='!(QUOTE/R_BRACKET) [\\x21..\\xff]'), numMin=1, numMax=False, expression='(!(QUOTE/R_BRACKET) [\\x21..\\xff])+', name='address')(liftValue)
url = Sequence([protocol, address], expression='protocol address', name='url')(join)

# Links

allowed_in_link = Repetition(Sequence([NextNot(Choice([R_BRACKET, PIPE], expression='R_BRACKET/PIPE'), expression='!(R_BRACKET/PIPE)'), escChar], expression='!(R_BRACKET/PIPE) escChar'), numMin=1, numMax=False, expression='(!(R_BRACKET/PIPE) escChar)+', name='allowed_in_link')(restore, join)
link_text = Repetition(Choice([cleanInline, allowed_in_link], expression='cleanInline / allowed_in_link'), numMin=False, numMax=False, expression='(cleanInline / allowed_in_link)*', name='link_text')(liftValue)
link_argument = Sequence([PIPE, link_text], expression='PIPE link_text', name='link_argument')(liftValue)
link_arguments = Repetition(link_argument, numMin=False, numMax=False, expression='link_argument*', name='link_arguments')
internal_link = Sequence([LINK_BEGIN, page_name, link_arguments, LINK_END], expression='LINK_BEGIN page_name link_arguments LINK_END', name='internal_link')(liftValue)
optional_link_text = Sequence([Repetition(SPACETAB, numMin=1, numMax=False, expression='SPACETAB+'), link_text], expression='SPACETAB+ link_text', name='optional_link_text')(liftValue)
external_link = Sequence([L_BRACKET, url, Option(optional_link_text, expression='optional_link_text?'), R_BRACKET], expression='L_BRACKET url optional_link_text? R_BRACKET', name='external_link')
link = Choice([internal_link, external_link], expression='internal_link / external_link', name='link')

# Templates

value = Sequence([EQUAL, cleanInline], expression='EQUAL cleanInline', name='value')(liftValue)
optional_value = Repetition(value, numMin=False, numMax=False, expression='value*', name='optional_value')(liftValue)
parameter_name = Repetition(Sequence([NextNot(EQUAL, expression='!EQUAL'), rawChar], expression='!EQUAL rawChar'), numMin=1, numMax=False, expression='(!EQUAL rawChar)+', name='parameter_name')(join)
parameter_with_value = Sequence([parameter_name, optional_value], expression='parameter_name optional_value', name='parameter_with_value')(liftValue)
parameter = Sequence([Repetition(SPACETABEOL, numMin=False, numMax=False, expression='SPACETABEOL*'), PIPE, Repetition(SPACETABEOL, numMin=False, numMax=False, expression='SPACETABEOL*'), Choice([parameter_with_value, cleanInline], expression='parameter_with_value / cleanInline')], expression='SPACETABEOL* PIPE SPACETABEOL* (parameter_with_value / cleanInline)', name='parameter')(liftValue)
parameters = Repetition(parameter, numMin=False, numMax=False, expression='parameter*', name='parameters')
template = Sequence([TEMPLATE_BEGIN, page_name, parameters, Repetition(SPACETABEOL, numMin=False, numMax=False, expression='SPACETABEOL*'), TEMPLATE_END], expression='TEMPLATE_BEGIN page_name parameters SPACETABEOL* TEMPLATE_END', name='template')

# Template parameters

    # Those parameters should be substituted by their value when the current page is a template or by their optional default value in any case
template_parameter_id = Repetition(Sequence([NextNot(Choice([R_BRACE, PIPE], expression='R_BRACE/PIPE'), expression='!(R_BRACE/PIPE)'), anyChar], expression='!(R_BRACE/PIPE) anyChar'), numMin=1, numMax=False, expression='(!(R_BRACE/PIPE) anyChar)+', name='template_parameter_id')(join)
default_value = Repetition(Sequence([NextNot(R_BRACE, expression='!R_BRACE'), anyChar], expression='!R_BRACE anyChar'), numMin=1, numMax=False, expression='(!R_BRACE anyChar)+', name='default_value')(join)
optional_default_value = Option(Sequence([PIPE, default_value], expression='PIPE default_value'), expression='(PIPE default_value)?', name='optional_default_value')(liftNode)
template_parameter = Sequence([PARAMETER_BEGIN, template_parameter_id, optional_default_value, PARAMETER_END], expression='PARAMETER_BEGIN template_parameter_id optional_default_value PARAMETER_END', name='template_parameter')

# Pre and nowiki tags

    # Preformatted acts like nowiki (disables wikitext parsing)
pre_text = Repetition(Sequence([NextNot(PRE_END, expression='!PRE_END'), anyChar], expression='!PRE_END anyChar'), numMin=False, numMax=False, expression='(!PRE_END anyChar)*', name='pre_text')(join)
preformatted = Sequence([PRE_BEGIN, pre_text, PRE_END], expression='PRE_BEGIN pre_text PRE_END', name='preformatted')(liftValue)
    # We allow any char without parsing them as long as the tag is not closed
eol_to_space = Repetition(EOL, numMin=False, numMax=False, expression='EOL*', name='eol_to_space')(replace_by_space)
nowiki_text = Repetition(Sequence([NextNot(NOWIKI_END, expression='!NOWIKI_END'), Choice([anyChar, eol_to_space], expression='anyChar/eol_to_space')], expression='!NOWIKI_END (anyChar/eol_to_space)'), numMin=False, numMax=False, expression='(!NOWIKI_END (anyChar/eol_to_space))*', name='nowiki_text')(join)
nowiki = Sequence([NOWIKI_BEGIN, nowiki_text, NOWIKI_END], expression='NOWIKI_BEGIN nowiki_text NOWIKI_END', name='nowiki')(liftValue)

# Text types

styled_text = Choice([link, url, template_parameter, template, html_comment, tag, entity], expression='link / url / template_parameter / template / html_comment / tag / entity', name='styled_text')
not_styled_text = Choice([preformatted, nowiki], expression='preformatted / nowiki', name='not_styled_text')
allowedChar = Repetition(escChar, numMin=1, numMax=1, expression='escChar{1}', name='allowedChar')(restore, liftValue)
allowedText = Choice([rawText, allowedChar], expression='rawText / allowedChar', name='allowedText')
cleanInline **= Repetition(Choice([not_styled_text, styled_text, rawText], expression='not_styled_text / styled_text / rawText'), numMin=1, numMax=False, expression='(not_styled_text / styled_text / rawText)+', name='cleanInline')
inline **= Repetition(Choice([not_styled_text, styled_text, allowedText], expression='not_styled_text / styled_text / allowedText'), numMin=1, numMax=False, expression='(not_styled_text / styled_text / allowedText)+', name='inline')

# Paragraphs

special_line_begin = Choice([SPACE, EQUAL, BULLET, HASH, COLON, Repetition(DASH, numMin=4, numMax=4, expression='DASH{4}'), TABLE_BEGIN, SEMICOLON], expression='SPACE/EQUAL/BULLET/HASH/COLON/DASH{4}/TABLE_BEGIN/SEMICOLON', name='special_line_begin')
paragraph_line = Sequence([NextNot(special_line_begin, expression='!special_line_begin'), inline, EOL], expression='!special_line_begin inline EOL', name='paragraph_line')(liftValue)
blank_paragraph = Repetition(EOL, numMin=2, numMax=2, expression='EOL{2}', name='blank_paragraph')(drop, keep)
paragraph = Repetition(paragraph_line, numMin=1, numMax=False, expression='paragraph_line+', name='paragraph')(liftValue)
paragraphs = Repetition(Choice([blank_paragraph, EOL, paragraph], expression='blank_paragraph/EOL/paragraph'), numMin=1, numMax=False, expression='(blank_paragraph/EOL/paragraph)+', name='paragraphs')

# Titles

title6 = Sequence([TITLE6_BEGIN, inline, TITLE6_END], expression='TITLE6_BEGIN inline TITLE6_END', name='title6')(liftValue)
title5 = Sequence([TITLE5_BEGIN, inline, TITLE5_END], expression='TITLE5_BEGIN inline TITLE5_END', name='title5')(liftValue)
title4 = Sequence([TITLE4_BEGIN, inline, TITLE4_END], expression='TITLE4_BEGIN inline TITLE4_END', name='title4')(liftValue)
title3 = Sequence([TITLE3_BEGIN, inline, TITLE3_END], expression='TITLE3_BEGIN inline TITLE3_END', name='title3')(liftValue)
title2 = Sequence([TITLE2_BEGIN, inline, TITLE2_END], expression='TITLE2_BEGIN inline TITLE2_END', name='title2')(liftValue)
title1 = Sequence([TITLE1_BEGIN, inline, TITLE1_END], expression='TITLE1_BEGIN inline TITLE1_END', name='title1')(liftValue)
title = Choice([title6, title5, title4, title3, title2, title1], expression='title6 / title5 / title4 / title3 / title2 / title1', name='title')

# Lists

listChar = Choice([BULLET, HASH, COLON, SEMICOLON], expression='BULLET / HASH / COLON / SEMICOLON', name='listChar')
listLeafContent = Sequence([NextNot(listChar, expression='!listChar'), inline, EOL], expression='!listChar inline EOL', name='listLeafContent')(liftValue)

bulletListLeaf = Sequence([BULLET, optional_comment, listLeafContent], expression='BULLET optional_comment listLeafContent', name='bulletListLeaf')(liftValue)
bulletSubList **= Sequence([BULLET, optional_comment, listItem], expression='BULLET optional_comment listItem', name='bulletSubList')

numberListLeaf = Sequence([HASH, optional_comment, listLeafContent], expression='HASH optional_comment listLeafContent', name='numberListLeaf')(liftValue)
numberSubList **= Sequence([HASH, optional_comment, listItem], expression='HASH optional_comment listItem', name='numberSubList')

colonListLeaf = Sequence([COLON, optional_comment, listLeafContent], expression='COLON optional_comment listLeafContent', name='colonListLeaf')(liftValue)
colonSubList **= Sequence([COLON, optional_comment, listItem], expression='COLON optional_comment listItem', name='colonSubList')

semiColonListLeaf = Sequence([SEMICOLON, optional_comment, listLeafContent], expression='SEMICOLON optional_comment listLeafContent', name='semiColonListLeaf')(liftValue)
semiColonSubList **= Sequence([SEMICOLON, optional_comment, listItem], expression='SEMICOLON optional_comment listItem', name='semiColonSubList')

listLeaf **= Choice([semiColonListLeaf, colonListLeaf, numberListLeaf, bulletListLeaf], expression='semiColonListLeaf / colonListLeaf / numberListLeaf / bulletListLeaf', name='listLeaf')
subList **= Choice([semiColonSubList, colonSubList, numberSubList, bulletSubList], expression='semiColonSubList / colonSubList / numberSubList / bulletSubList', name='subList')
listItem **= Choice([subList, listLeaf], expression='subList / listLeaf', name='listItem')
list = Repetition(listItem, numMin=1, numMax=False, expression='listItem+', name='list')

# Preformatted

EOL_or_not = Repetition(EOL, numMin=0, numMax=1, expression='EOL{0..1}', name='EOL_or_not')(drop)
preformattedLine = Sequence([SPACE, inline, EOL], expression='SPACE inline EOL', name='preformattedLine')(liftValue)
preformattedLines = Repetition(preformattedLine, numMin=1, numMax=False, expression='preformattedLine+', name='preformattedLines')
preformattedText = Sequence([inline, EOL_or_not], expression='inline EOL_or_not', name='preformattedText')(liftValue)
preformattedParagraph = Sequence([PRE_BEGIN, EOL, preformattedText, PRE_END, EOL], expression='PRE_BEGIN EOL preformattedText PRE_END EOL', name='preformattedParagraph')
preformattedGroup = Choice([preformattedParagraph, preformattedLines], expression='preformattedParagraph / preformattedLines', name='preformattedGroup')

# Special lines

horizontal_rule = Sequence([Repetition(DASH, numMin=4, numMax=4, expression='DASH{4}'), Repetition(DASH, numMin=False, numMax=False, expression='DASH*'), Repetition(inline, numMin=False, numMax=False, expression='inline*'), EOL], expression='DASH{4} DASH* inline* EOL', name='horizontal_rule')(liftValue, keep)

    # This should never happen
invalid_line = Sequence([anyText, EOL], expression='anyText EOL', name='invalid_line')(liftValue)

# Tables

HTML_value_quote = Sequence([QUOTE, Repetition(Choice([Sequence([NextNot(Choice([GT, QUOTE], expression='GT/QUOTE'), expression='!(GT/QUOTE)'), anyChar], expression='!(GT/QUOTE) anyChar'), TAB], expression='(!(GT/QUOTE) anyChar) / TAB'), numMin=1, numMax=False, expression='((!(GT/QUOTE) anyChar) / TAB)+'), QUOTE], expression='QUOTE ((!(GT/QUOTE) anyChar) / TAB)+ QUOTE', name='HTML_value_quote')(join)
HTML_value_apostrophe = Sequence([APOSTROPHE, Repetition(Choice([Sequence([NextNot(Choice([GT, APOSTROPHE], expression='GT/APOSTROPHE'), expression='!(GT/APOSTROPHE)'), anyChar], expression='!(GT/APOSTROPHE) anyChar'), TAB], expression='(!(GT/APOSTROPHE) anyChar) / TAB'), numMin=1, numMax=False, expression='((!(GT/APOSTROPHE) anyChar) / TAB)+'), APOSTROPHE], expression='APOSTROPHE ((!(GT/APOSTROPHE) anyChar) / TAB)+ APOSTROPHE', name='HTML_value_apostrophe')(join)
HTML_value_noquote = Repetition(Sequence([NextNot(Choice([GT, SPACETAB, SLASH], expression='GT/SPACETAB/SLASH'), expression='!(GT/SPACETAB/SLASH)'), rawChar], expression='!(GT/SPACETAB/SLASH) rawChar'), numMin=1, numMax=False, expression='(!(GT/SPACETAB/SLASH) rawChar)+', name='HTML_value_noquote')(join)
HTML_value = Choice([HTML_value_quote, HTML_value_apostrophe, HTML_value_noquote], expression='HTML_value_quote / HTML_value_apostrophe / HTML_value_noquote', name='HTML_value')
HTML_name = Repetition(Sequence([NextNot(Choice([EQUAL, SLASH, SPACETAB], expression='EQUAL/SLASH/SPACETAB'), expression='!(EQUAL/SLASH/SPACETAB)'), rawChar], expression='!(EQUAL/SLASH/SPACETAB) rawChar'), numMin=1, numMax=False, expression='(!(EQUAL/SLASH/SPACETAB) rawChar)+', name='HTML_name')(join)
HTML_attribute = Sequence([Repetition(SPACETAB, numMin=False, numMax=False, expression='SPACETAB*'), HTML_name, EQUAL, HTML_value, Repetition(SPACETAB, numMin=False, numMax=False, expression='SPACETAB*')], expression='SPACETAB* HTML_name EQUAL HTML_value SPACETAB*', name='HTML_attribute')
HTML_attributes = Repetition(HTML_attribute, numMin=False, numMax=False, expression='HTML_attribute*', name='HTML_attributes')
wikiTableParametersPipe = Option(Sequence([Repetition(SPACETAB, numMin=False, numMax=False, expression='SPACETAB*'), Repetition(HTML_attribute, numMin=1, numMax=False, expression='HTML_attribute+'), Repetition(SPACETAB, numMin=False, numMax=False, expression='SPACETAB*'), PIPE, NextNot(PIPE, expression='!PIPE')], expression='SPACETAB* HTML_attribute+ SPACETAB* PIPE !PIPE'), expression='(SPACETAB* HTML_attribute+ SPACETAB* PIPE !PIPE)?', name='wikiTableParametersPipe')(liftNode)
wikiTableParameters = Repetition(Choice([HTML_attribute, cleanInline], expression='HTML_attribute / cleanInline'), numMin=1, numMax=False, expression='(HTML_attribute / cleanInline)+', name='wikiTableParameters')(liftValue)
wikiTableParameter = Repetition(wikiTableParametersPipe, numMin=0, numMax=1, expression='wikiTableParametersPipe{0..1}', name='wikiTableParameter')(liftValue)
wikiTableCellContent = Repetition(cleanInline, numMin=False, numMax=False, expression='cleanInline*', name='wikiTableCellContent')
wikiTableFirstCell = Sequence([wikiTableParameter, wikiTableCellContent], expression='wikiTableParameter wikiTableCellContent', name='wikiTableFirstCell')(liftNode)
wikiTableOtherCell = Repetition(Sequence([Repetition(PIPE, numMin=2, numMax=2, expression='PIPE{2}'), wikiTableFirstCell], expression='PIPE{2} wikiTableFirstCell'), numMin=False, numMax=False, expression='(PIPE{2} wikiTableFirstCell)*', name='wikiTableOtherCell')(liftValue, liftNode)
wikiTableLineCells = Sequence([PIPE, wikiTableFirstCell, wikiTableOtherCell, EOL], expression='PIPE wikiTableFirstCell wikiTableOtherCell EOL', name='wikiTableLineCells')(liftValue)
wikiTableLineHeader = Sequence([BANG, wikiTableFirstCell, wikiTableOtherCell, EOL], expression='BANG wikiTableFirstCell wikiTableOtherCell EOL', name='wikiTableLineHeader')(liftValue)
wikiTableEmptyCell = Sequence([PIPE, EOL], expression='PIPE EOL', name='wikiTableEmptyCell')(keep)
wikiTableParamLineBreak = Sequence([TABLE_NEWLINE, Repetition(wikiTableParameters, numMin=False, numMax=False, expression='wikiTableParameters*'), EOL], expression='TABLE_NEWLINE wikiTableParameters* EOL', name='wikiTableParamLineBreak')(keep, liftValue)
wikiTableLineBreak = Sequence([TABLE_NEWLINE, EOL], expression='TABLE_NEWLINE EOL', name='wikiTableLineBreak')(keep)
wikiTableTitle = Sequence([TABLE_TITLE, wikiTableParameter, wikiTableCellContent, EOL], expression='TABLE_TITLE wikiTableParameter wikiTableCellContent EOL', name='wikiTableTitle')(liftValue)
wikiTableSpecialLine = Choice([wikiTableTitle, wikiTableLineBreak, wikiTableParamLineBreak], expression='wikiTableTitle / wikiTableLineBreak / wikiTableParamLineBreak', name='wikiTableSpecialLine')
wikiTableNormalLine = Choice([wikiTableLineCells, wikiTableLineHeader, wikiTableEmptyCell], expression='wikiTableLineCells / wikiTableLineHeader / wikiTableEmptyCell', name='wikiTableNormalLine')
wikiTableLine = Sequence([NextNot(TABLE_END, expression='!TABLE_END'), Choice([wikiTableSpecialLine, wikiTableNormalLine], expression='wikiTableSpecialLine / wikiTableNormalLine')], expression='!TABLE_END (wikiTableSpecialLine / wikiTableNormalLine)', name='wikiTableLine')(liftNode)
wikiTableContent = Repetition(Choice([wikiTableLine, wikiTable, EOL], expression='wikiTableLine / wikiTable / EOL'), numMin=False, numMax=False, expression='(wikiTableLine / wikiTable / EOL)*', name='wikiTableContent')(liftNode)
wikiTableBegin = Sequence([TABLE_BEGIN, Repetition(wikiTableParameters, numMin=False, numMax=False, expression='wikiTableParameters*')], expression='TABLE_BEGIN wikiTableParameters*', name='wikiTableBegin')(liftValue)
wikiTable **= Sequence([wikiTableBegin, Repetition(SPACETABEOL, numMin=False, numMax=False, expression='SPACETABEOL*'), wikiTableContent, TABLE_END, EOL], expression='wikiTableBegin SPACETABEOL* wikiTableContent TABLE_END EOL', name='wikiTable')(liftValue)

# Top pattern

body = Sequence([optional_comment, Repetition(Choice([list, horizontal_rule, preformattedGroup, title, wikiTable, EOL, paragraphs, invalid_line, EOL], expression='list / horizontal_rule / preformattedGroup / title / wikiTable / EOL / paragraphs / invalid_line / EOL'), numMin=1, numMax=False, expression='(list / horizontal_rule / preformattedGroup / title / wikiTable / EOL / paragraphs / invalid_line / EOL)+')], expression='optional_comment (list / horizontal_rule / preformattedGroup / title / wikiTable / EOL / paragraphs / invalid_line / EOL)+', name='body')(liftValue)



wikitextParser._recordPatterns(vars())
wikitextParser._setTopPattern("body")
wikitextParser.grammarTitle = "wikitext"
wikitextParser.filename = "wikitextParser.py"
