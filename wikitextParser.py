""" wikitext
<definition>
# codes
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
    PIPE                    : "|"                                                                   : drop
    BANG                    : "!"                                                                   : drop
    EQUAL                   : "="                                                                   : drop
    BULLET                  : "*"                                                                   : drop
    HASH                    : "#"                                                                   : drop
    COLON                   : ":"                                                                   : drop
    SEMICOLON               : ";"                                                                   : drop
    DASH                    : "-"                                                                   : drop
    TABLE_BEGIN             : "{|"                                                                  : drop
    TABLE_END               : "|}"                                                                  : drop
    TABLE_NEWLINE           : "|-"                                                                  : drop
    TABLE_TITLE             : "|+"                                                                  : drop
    QUOTE                   : "\""                                                                  : drop
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
    LINK_BEGIN              : L_BRACKET{2}                                                          : drop
    LINK_END                : R_BRACKET{2}                                                          : drop

    HTTP                    : "http://"                                                             : liftValue
    FTP                     : "ftp://"                                                              : liftValue
    protocole               : HTTP / FTP                                                            : liftValue

# tags
    NOWIKI_BEGIN            : "<nowiki>"                                                            : drop
    NOWIKI_END              : "</nowiki>"                                                           : drop
    BOLD_BEGIN              : "<b>" / "<strong>"                                                    : drop
    BOLD_END                : "</b>" / "</strong>"                                                  : drop
    ITALIC_BEGIN            : "<i>" / "<em>"                                                        : drop
    ITALIC_END              : "</i>" / "</em>"                                                      : drop
    PRE_BEGIN               : "<pre>"                                                               : drop
    PRE_END                 : "</pre>"                                                              : drop
    tag                     : NOWIKI_BEGIN/NOWIKI_END/BOLD_BEGIN/BOLD_END/ITALIC_BEGIN/ITALIC_END/PRE_BEGIN/PRE_END

    titleEnd                : TITLE6_END/TITLE5_END/TITLE4_END/TITLE3_END/TITLE2_END/TITLE1_END

# character expression
    escChar                 : L_BRACKET/R_BRACKET/protocole/PIPE/L_BRACE/R_BRACE
    escSeq                  : escChar / tag / titleEnd
    rawChar                 : !escSeq [\x20..\xff]
    rawText                 : rawChar+                                                              : join parseAllQuotes
    anyChar                 : [\x20..\xff]
    anyText                 : anyChar+                                                              : join

# text
    pageName                : rawChar+                                                              : join
    templateName            : rawChar+                                                              : join
    address                 : (!(SPACE/QUOTE) [\x21..\xff])+                                        : liftValue
    url                     : protocole address                                                     : join
    boldText                : BOLD_BEGIN inline BOLD_END                                            : liftValue
    italicText              : ITALIC_BEGIN inline ITALIC_END                                        : liftValue
    value                   : EQUAL cleanInline                                                     : liftValue
    optionalValue           : value*                                                                : liftValue
    parameterName           : (!EQUAL rawChar)+                                                     : join
    parameterWithValue      : parameterName optionalValue                                           : liftValue
    parameter               : PIPE SPACETAB* (parameterWithValue / cleanInline)                     : liftValue
    ignoredInParameters     : EOL/SPACE                                                             : drop
    parameters              : (parameter/ignoredInParameters)+
    simpleInternalLink      : LINK_BEGIN templateName LINK_END                                      : liftValue
    advancedInternalLink    : LINK_BEGIN templateName PIPE cleanInline LINK_END                     : liftValue
    internalLink            : simpleInternalLink / advancedInternalLink                             : liftValue
    externalLink            : L_BRACKET url SPACE cleanInline R_BRACKET                             : liftValue
    link                    : internalLink / externalLink
    simpleTemplate          : TEMPLATE_BEGIN pageName TEMPLATE_END                                  : liftValue
    advancedTemplate        : TEMPLATE_BEGIN pageName parameters TEMPLATE_END                       : liftValue
    template                : simpleTemplate / advancedTemplate
    preformatted            : PRE_BEGIN inline PRE_END                                              : liftValue
    styledText              : boldText / italicText / link / url / template / preformatted
    ignoredInNowiki         : (!(NOWIKI_END) [\x20..\xff])+                                         : join
    nowiki                  : NOWIKI_BEGIN ignoredInNowiki+ NOWIKI_END                              : liftValue
    allowedChar             : escChar{1}                                                            : restore liftValue
    allowedText             : rawText / allowedChar
    cleanInline             : (styledText / nowiki / rawText)+                                      : @
    inline                  : (styledText / nowiki / allowedText)+                                  : @

# line types
    specialLineBegin        : SPACE/EQUAL/BULLET/HASH/COLON/DASH/TABLE_BEGIN/SEMICOLON

    title6                  : TITLE6_BEGIN inline TITLE6_END                                        : liftValue
    title5                  : TITLE5_BEGIN inline TITLE5_END                                        : liftValue
    title4                  : TITLE4_BEGIN inline TITLE4_END                                        : liftValue
    title3                  : TITLE3_BEGIN inline TITLE3_END                                        : liftValue
    title2                  : TITLE2_BEGIN inline TITLE2_END                                        : liftValue
    title1                  : TITLE1_BEGIN inline TITLE1_END                                        : liftValue
    title                   : title6 / title5 / title4 / title3 / title2 / title1

    paragraphLine           : !specialLineBegin inline EOL                                          : liftValue
    blankParagraph          : EOL{2}                                                                : setNullValue
    paragraph               : paragraphLine+                                                        : liftValue
    paragraphs              : (blankParagraph/EOL/paragraph)+


    listChar                : BULLET / HASH / COLON / SEMICOLON
    listLeafContent         : !listChar inline EOL                                                  : liftValue

    bulletListLeaf          : BULLET listLeafContent                                                : liftValue
    bulletSubList           : BULLET listItem                                                       : @

    numberListLeaf          : HASH listLeafContent                                                  : liftValue
    numberSubList           : HASH listItem                                                         : @

    colonListLeaf           : COLON listLeafContent                                                 : liftValue
    colonSubList            : COLON listItem                                                        : @

    semiColonListLeaf       : SEMICOLON listLeafContent                                             : liftValue
    semiColonSubList        : SEMICOLON listItem                                                    : @

    listLeaf                : semiColonListLeaf / colonListLeaf / numberListLeaf / bulletListLeaf   : @
    subList                 : semiColonSubList / colonSubList / numberSubList / bulletSubList       : @
    listItem                : subList / listLeaf                                                    : @
    list                    : listItem+


    EOL_or_not              : EOL{0..1}                                                             : drop
    preformattedLine        : SPACE inline EOL                                                      : liftValue
    preformattedLines       : preformattedLine+
    preformattedText        : inline EOL_or_not                                                     : liftValue
    preformattedParagraph   : PRE_BEGIN EOL preformattedText PRE_END EOL
    preformattedGroup       : preformattedParagraph / preformattedLines

    horizontalRule          : DASH{4} DASH* inline EOL                                              : liftValue

    invalidLine             : anyText EOL                                                           : liftValue

    CSS_chars               : !(PIPE/BANG/L_BRACE) anyChar
    CSS_text                : CSS_chars+                                                            : join
    CSS_attributes          : CSS_text+ PIPE !PIPE                                                  : liftValue
    wikiTableParameters     : (CSS_text / cleanInline)+                                             : liftValue
    wikiTableFirstCell      : CSS_attributes{0..1} cleanInline*                                     : liftValue
    wikiTableOtherCell      : PIPE{2} wikiTableFirstCell                                            : liftValue
    wikiTableLineCells      : PIPE wikiTableFirstCell wikiTableOtherCell* EOL                       : liftValue
    wikiTableLineHeader     : BANG wikiTableFirstCell wikiTableOtherCell* EOL                       : liftValue
    wikiTableEmptyCell      : PIPE EOL                                                              : setNullValue
    wikiTableParamLineBreak : TABLE_NEWLINE wikiTableParameters* EOL                                : liftValue
    wikiTableLineBreak      : TABLE_NEWLINE EOL                                                     : setNullValue
    wikiTableTitle          : TABLE_TITLE CSS_attributes{0..1} inline* EOL                          : liftValue
    wikiTableSpecialLine    : wikiTableTitle / wikiTableLineBreak / wikiTableParamLineBreak
    wikiTableNormalLine     : wikiTableLineCells / wikiTableLineHeader / wikiTableEmptyCell
    wikiTableLine           : !TABLE_END (wikiTableSpecialLine / wikiTableNormalLine)
    wikiTableContent        : wikiTableLine / wikiTable / EOL
    wikiTableBegin          : TABLE_BEGIN wikiTableParameters*                                      : liftValue
    wikiTable               : wikiTableBegin EOL* wikiTableContent* TABLE_END EOL                   : @ liftValue

    body                    : (list / horizontalRule / preformattedGroup / title / wikiTable / EOL / paragraphs / invalidLine / EOL)+

"""



from pijnu.library import *

wikitextParser = Parser()
state = wikitextParser.state



### title: wikitext ###


###   <toolset>
def setNullValue(node):
    node.value = ''
def parseAllQuotes(node):
    from apostrophes import parseQuotes
    node.value = parseQuotes(node.value)

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
# codes
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
PIPE = Word('|', expression='"|"', name='PIPE')(drop)
BANG = Word('!', expression='"!"', name='BANG')(drop)
EQUAL = Word('=', expression='"="', name='EQUAL')(drop)
BULLET = Word('*', expression='"*"', name='BULLET')(drop)
HASH = Word('#', expression='"#"', name='HASH')(drop)
COLON = Word(':', expression='":"', name='COLON')(drop)
SEMICOLON = Word(';', expression='";"', name='SEMICOLON')(drop)
DASH = Word('-', expression='"-"', name='DASH')(drop)
TABLE_BEGIN = Word('{|', expression='"{|"', name='TABLE_BEGIN')(drop)
TABLE_END = Word('|}', expression='"|}"', name='TABLE_END')(drop)
TABLE_NEWLINE = Word('|-', expression='"|-"', name='TABLE_NEWLINE')(drop)
TABLE_TITLE = Word('|+', expression='"|+"', name='TABLE_TITLE')(drop)
QUOTE = Word('"', expression='"\\""', name='QUOTE')(drop)
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
LINK_BEGIN = Repetition(L_BRACKET, numMin=2, numMax=2, expression='L_BRACKET{2}', name='LINK_BEGIN')(drop)
LINK_END = Repetition(R_BRACKET, numMin=2, numMax=2, expression='R_BRACKET{2}', name='LINK_END')(drop)

HTTP = Word('http://', expression='"http://"', name='HTTP')(liftValue)
FTP = Word('ftp://', expression='"ftp://"', name='FTP')(liftValue)
protocole = Choice([HTTP, FTP], expression='HTTP / FTP', name='protocole')(liftValue)

# tags
NOWIKI_BEGIN = Word('<nowiki>', expression='"<nowiki>"', name='NOWIKI_BEGIN')(drop)
NOWIKI_END = Word('</nowiki>', expression='"</nowiki>"', name='NOWIKI_END')(drop)
BOLD_BEGIN = Choice([Word('<b>', expression='"<b>"'), Word('<strong>', expression='"<strong>"')], expression='"<b>" / "<strong>"', name='BOLD_BEGIN')(drop)
BOLD_END = Choice([Word('</b>', expression='"</b>"'), Word('</strong>', expression='"</strong>"')], expression='"</b>" / "</strong>"', name='BOLD_END')(drop)
ITALIC_BEGIN = Choice([Word('<i>', expression='"<i>"'), Word('<em>', expression='"<em>"')], expression='"<i>" / "<em>"', name='ITALIC_BEGIN')(drop)
ITALIC_END = Choice([Word('</i>', expression='"</i>"'), Word('</em>', expression='"</em>"')], expression='"</i>" / "</em>"', name='ITALIC_END')(drop)
PRE_BEGIN = Word('<pre>', expression='"<pre>"', name='PRE_BEGIN')(drop)
PRE_END = Word('</pre>', expression='"</pre>"', name='PRE_END')(drop)
tag = Choice([NOWIKI_BEGIN, NOWIKI_END, BOLD_BEGIN, BOLD_END, ITALIC_BEGIN, ITALIC_END, PRE_BEGIN, PRE_END], expression='NOWIKI_BEGIN/NOWIKI_END/BOLD_BEGIN/BOLD_END/ITALIC_BEGIN/ITALIC_END/PRE_BEGIN/PRE_END', name='tag')

titleEnd = Choice([TITLE6_END, TITLE5_END, TITLE4_END, TITLE3_END, TITLE2_END, TITLE1_END], expression='TITLE6_END/TITLE5_END/TITLE4_END/TITLE3_END/TITLE2_END/TITLE1_END', name='titleEnd')

# character expression
escChar = Choice([L_BRACKET, R_BRACKET, protocole, PIPE, L_BRACE, R_BRACE], expression='L_BRACKET/R_BRACKET/protocole/PIPE/L_BRACE/R_BRACE', name='escChar')
escSeq = Choice([escChar, tag, titleEnd], expression='escChar / tag / titleEnd', name='escSeq')
rawChar = Sequence([NextNot(escSeq, expression='!escSeq'), Klass(u' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff', expression='[\\x20..\\xff]')], expression='!escSeq [\\x20..\\xff]', name='rawChar')
rawText = Repetition(rawChar, numMin=1, numMax=False, expression='rawChar+', name='rawText')(join, parseAllQuotes)
anyChar = Klass(u' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff', expression='[\\x20..\\xff]', name='anyChar')
anyText = Repetition(anyChar, numMin=1, numMax=False, expression='anyChar+', name='anyText')(join)

# text
pageName = Repetition(rawChar, numMin=1, numMax=False, expression='rawChar+', name='pageName')(join)
templateName = Repetition(rawChar, numMin=1, numMax=False, expression='rawChar+', name='templateName')(join)
address = Repetition(Sequence([NextNot(Choice([SPACE, QUOTE], expression='SPACE/QUOTE'), expression='!(SPACE/QUOTE)'), Klass(u'!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff', expression='[\\x21..\\xff]')], expression='!(SPACE/QUOTE) [\\x21..\\xff]'), numMin=1, numMax=False, expression='(!(SPACE/QUOTE) [\\x21..\\xff])+', name='address')(liftValue)
url = Sequence([protocole, address], expression='protocole address', name='url')(join)
boldText = Sequence([BOLD_BEGIN, inline, BOLD_END], expression='BOLD_BEGIN inline BOLD_END', name='boldText')(liftValue)
italicText = Sequence([ITALIC_BEGIN, inline, ITALIC_END], expression='ITALIC_BEGIN inline ITALIC_END', name='italicText')(liftValue)
value = Sequence([EQUAL, cleanInline], expression='EQUAL cleanInline', name='value')(liftValue)
optionalValue = Repetition(value, numMin=False, numMax=False, expression='value*', name='optionalValue')(liftValue)
parameterName = Repetition(Sequence([NextNot(EQUAL, expression='!EQUAL'), rawChar], expression='!EQUAL rawChar'), numMin=1, numMax=False, expression='(!EQUAL rawChar)+', name='parameterName')(join)
parameterWithValue = Sequence([parameterName, optionalValue], expression='parameterName optionalValue', name='parameterWithValue')(liftValue)
parameter = Sequence([PIPE, Repetition(SPACETAB, numMin=False, numMax=False, expression='SPACETAB*'), Choice([parameterWithValue, cleanInline], expression='parameterWithValue / cleanInline')], expression='PIPE SPACETAB* (parameterWithValue / cleanInline)', name='parameter')(liftValue)
ignoredInParameters = Choice([EOL, SPACE], expression='EOL/SPACE', name='ignoredInParameters')(drop)
parameters = Repetition(Choice([parameter, ignoredInParameters], expression='parameter/ignoredInParameters'), numMin=1, numMax=False, expression='(parameter/ignoredInParameters)+', name='parameters')
simpleInternalLink = Sequence([LINK_BEGIN, templateName, LINK_END], expression='LINK_BEGIN templateName LINK_END', name='simpleInternalLink')(liftValue)
advancedInternalLink = Sequence([LINK_BEGIN, templateName, PIPE, cleanInline, LINK_END], expression='LINK_BEGIN templateName PIPE cleanInline LINK_END', name='advancedInternalLink')(liftValue)
internalLink = Choice([simpleInternalLink, advancedInternalLink], expression='simpleInternalLink / advancedInternalLink', name='internalLink')(liftValue)
externalLink = Sequence([L_BRACKET, url, SPACE, cleanInline, R_BRACKET], expression='L_BRACKET url SPACE cleanInline R_BRACKET', name='externalLink')(liftValue)
link = Choice([internalLink, externalLink], expression='internalLink / externalLink', name='link')
simpleTemplate = Sequence([TEMPLATE_BEGIN, pageName, TEMPLATE_END], expression='TEMPLATE_BEGIN pageName TEMPLATE_END', name='simpleTemplate')(liftValue)
advancedTemplate = Sequence([TEMPLATE_BEGIN, pageName, parameters, TEMPLATE_END], expression='TEMPLATE_BEGIN pageName parameters TEMPLATE_END', name='advancedTemplate')(liftValue)
template = Choice([simpleTemplate, advancedTemplate], expression='simpleTemplate / advancedTemplate', name='template')
preformatted = Sequence([PRE_BEGIN, inline, PRE_END], expression='PRE_BEGIN inline PRE_END', name='preformatted')(liftValue)
styledText = Choice([boldText, italicText, link, url, template, preformatted], expression='boldText / italicText / link / url / template / preformatted', name='styledText')
ignoredInNowiki = Repetition(Sequence([NextNot(NOWIKI_END, expression='!(NOWIKI_END)'), Klass(u' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff', expression='[\\x20..\\xff]')], expression='!(NOWIKI_END) [\\x20..\\xff]'), numMin=1, numMax=False, expression='(!(NOWIKI_END) [\\x20..\\xff])+', name='ignoredInNowiki')(join)
nowiki = Sequence([NOWIKI_BEGIN, Repetition(ignoredInNowiki, numMin=1, numMax=False, expression='ignoredInNowiki+'), NOWIKI_END], expression='NOWIKI_BEGIN ignoredInNowiki+ NOWIKI_END', name='nowiki')(liftValue)
allowedChar = Repetition(escChar, numMin=1, numMax=1, expression='escChar{1}', name='allowedChar')(restore, liftValue)
allowedText = Choice([rawText, allowedChar], expression='rawText / allowedChar', name='allowedText')
cleanInline **= Repetition(Choice([styledText, nowiki, rawText], expression='styledText / nowiki / rawText'), numMin=1, numMax=False, expression='(styledText / nowiki / rawText)+', name='cleanInline')
inline **= Repetition(Choice([styledText, nowiki, allowedText], expression='styledText / nowiki / allowedText'), numMin=1, numMax=False, expression='(styledText / nowiki / allowedText)+', name='inline')

# line types
specialLineBegin = Choice([SPACE, EQUAL, BULLET, HASH, COLON, DASH, TABLE_BEGIN, SEMICOLON], expression='SPACE/EQUAL/BULLET/HASH/COLON/DASH/TABLE_BEGIN/SEMICOLON', name='specialLineBegin')

title6 = Sequence([TITLE6_BEGIN, inline, TITLE6_END], expression='TITLE6_BEGIN inline TITLE6_END', name='title6')(liftValue)
title5 = Sequence([TITLE5_BEGIN, inline, TITLE5_END], expression='TITLE5_BEGIN inline TITLE5_END', name='title5')(liftValue)
title4 = Sequence([TITLE4_BEGIN, inline, TITLE4_END], expression='TITLE4_BEGIN inline TITLE4_END', name='title4')(liftValue)
title3 = Sequence([TITLE3_BEGIN, inline, TITLE3_END], expression='TITLE3_BEGIN inline TITLE3_END', name='title3')(liftValue)
title2 = Sequence([TITLE2_BEGIN, inline, TITLE2_END], expression='TITLE2_BEGIN inline TITLE2_END', name='title2')(liftValue)
title1 = Sequence([TITLE1_BEGIN, inline, TITLE1_END], expression='TITLE1_BEGIN inline TITLE1_END', name='title1')(liftValue)
title = Choice([title6, title5, title4, title3, title2, title1], expression='title6 / title5 / title4 / title3 / title2 / title1', name='title')

paragraphLine = Sequence([NextNot(specialLineBegin, expression='!specialLineBegin'), inline, EOL], expression='!specialLineBegin inline EOL', name='paragraphLine')(liftValue)
blankParagraph = Repetition(EOL, numMin=2, numMax=2, expression='EOL{2}', name='blankParagraph')(setNullValue)
paragraph = Repetition(paragraphLine, numMin=1, numMax=False, expression='paragraphLine+', name='paragraph')(liftValue)
paragraphs = Repetition(Choice([blankParagraph, EOL, paragraph], expression='blankParagraph/EOL/paragraph'), numMin=1, numMax=False, expression='(blankParagraph/EOL/paragraph)+', name='paragraphs')


listChar = Choice([BULLET, HASH, COLON, SEMICOLON], expression='BULLET / HASH / COLON / SEMICOLON', name='listChar')
listLeafContent = Sequence([NextNot(listChar, expression='!listChar'), inline, EOL], expression='!listChar inline EOL', name='listLeafContent')(liftValue)

bulletListLeaf = Sequence([BULLET, listLeafContent], expression='BULLET listLeafContent', name='bulletListLeaf')(liftValue)
bulletSubList **= Sequence([BULLET, listItem], expression='BULLET listItem', name='bulletSubList')

numberListLeaf = Sequence([HASH, listLeafContent], expression='HASH listLeafContent', name='numberListLeaf')(liftValue)
numberSubList **= Sequence([HASH, listItem], expression='HASH listItem', name='numberSubList')

colonListLeaf = Sequence([COLON, listLeafContent], expression='COLON listLeafContent', name='colonListLeaf')(liftValue)
colonSubList **= Sequence([COLON, listItem], expression='COLON listItem', name='colonSubList')

semiColonListLeaf = Sequence([SEMICOLON, listLeafContent], expression='SEMICOLON listLeafContent', name='semiColonListLeaf')(liftValue)
semiColonSubList **= Sequence([SEMICOLON, listItem], expression='SEMICOLON listItem', name='semiColonSubList')

listLeaf **= Choice([semiColonListLeaf, colonListLeaf, numberListLeaf, bulletListLeaf], expression='semiColonListLeaf / colonListLeaf / numberListLeaf / bulletListLeaf', name='listLeaf')
subList **= Choice([semiColonSubList, colonSubList, numberSubList, bulletSubList], expression='semiColonSubList / colonSubList / numberSubList / bulletSubList', name='subList')
listItem **= Choice([subList, listLeaf], expression='subList / listLeaf', name='listItem')
list = Repetition(listItem, numMin=1, numMax=False, expression='listItem+', name='list')


EOL_or_not = Repetition(EOL, numMin=0, numMax=1, expression='EOL{0..1}', name='EOL_or_not')(drop)
preformattedLine = Sequence([SPACE, inline, EOL], expression='SPACE inline EOL', name='preformattedLine')(liftValue)
preformattedLines = Repetition(preformattedLine, numMin=1, numMax=False, expression='preformattedLine+', name='preformattedLines')
preformattedText = Sequence([inline, EOL_or_not], expression='inline EOL_or_not', name='preformattedText')(liftValue)
preformattedParagraph = Sequence([PRE_BEGIN, EOL, preformattedText, PRE_END, EOL], expression='PRE_BEGIN EOL preformattedText PRE_END EOL', name='preformattedParagraph')
preformattedGroup = Choice([preformattedParagraph, preformattedLines], expression='preformattedParagraph / preformattedLines', name='preformattedGroup')

horizontalRule = Sequence([Repetition(DASH, numMin=4, numMax=4, expression='DASH{4}'), Repetition(DASH, numMin=False, numMax=False, expression='DASH*'), inline, EOL], expression='DASH{4} DASH* inline EOL', name='horizontalRule')(liftValue)

invalidLine = Sequence([anyText, EOL], expression='anyText EOL', name='invalidLine')(liftValue)

CSS_chars = Sequence([NextNot(Choice([PIPE, BANG, L_BRACE], expression='PIPE/BANG/L_BRACE'), expression='!(PIPE/BANG/L_BRACE)'), anyChar], expression='!(PIPE/BANG/L_BRACE) anyChar', name='CSS_chars')
CSS_text = Repetition(CSS_chars, numMin=1, numMax=False, expression='CSS_chars+', name='CSS_text')(join)
CSS_attributes = Sequence([Repetition(CSS_text, numMin=1, numMax=False, expression='CSS_text+'), PIPE, NextNot(PIPE, expression='!PIPE')], expression='CSS_text+ PIPE !PIPE', name='CSS_attributes')(liftValue)
wikiTableParameters = Repetition(Choice([CSS_text, cleanInline], expression='CSS_text / cleanInline'), numMin=1, numMax=False, expression='(CSS_text / cleanInline)+', name='wikiTableParameters')(liftValue)
wikiTableFirstCell = Sequence([Repetition(CSS_attributes, numMin=0, numMax=1, expression='CSS_attributes{0..1}'), Repetition(cleanInline, numMin=False, numMax=False, expression='cleanInline*')], expression='CSS_attributes{0..1} cleanInline*', name='wikiTableFirstCell')(liftValue)
wikiTableOtherCell = Sequence([Repetition(PIPE, numMin=2, numMax=2, expression='PIPE{2}'), wikiTableFirstCell], expression='PIPE{2} wikiTableFirstCell', name='wikiTableOtherCell')(liftValue)
wikiTableLineCells = Sequence([PIPE, wikiTableFirstCell, Repetition(wikiTableOtherCell, numMin=False, numMax=False, expression='wikiTableOtherCell*'), EOL], expression='PIPE wikiTableFirstCell wikiTableOtherCell* EOL', name='wikiTableLineCells')(liftValue)
wikiTableLineHeader = Sequence([BANG, wikiTableFirstCell, Repetition(wikiTableOtherCell, numMin=False, numMax=False, expression='wikiTableOtherCell*'), EOL], expression='BANG wikiTableFirstCell wikiTableOtherCell* EOL', name='wikiTableLineHeader')(liftValue)
wikiTableEmptyCell = Sequence([PIPE, EOL], expression='PIPE EOL', name='wikiTableEmptyCell')(setNullValue)
wikiTableParamLineBreak = Sequence([TABLE_NEWLINE, Repetition(wikiTableParameters, numMin=False, numMax=False, expression='wikiTableParameters*'), EOL], expression='TABLE_NEWLINE wikiTableParameters* EOL', name='wikiTableParamLineBreak')(liftValue)
wikiTableLineBreak = Sequence([TABLE_NEWLINE, EOL], expression='TABLE_NEWLINE EOL', name='wikiTableLineBreak')(setNullValue)
wikiTableTitle = Sequence([TABLE_TITLE, Repetition(CSS_attributes, numMin=0, numMax=1, expression='CSS_attributes{0..1}'), Repetition(inline, numMin=False, numMax=False, expression='inline*'), EOL], expression='TABLE_TITLE CSS_attributes{0..1} inline* EOL', name='wikiTableTitle')(liftValue)
wikiTableSpecialLine = Choice([wikiTableTitle, wikiTableLineBreak, wikiTableParamLineBreak], expression='wikiTableTitle / wikiTableLineBreak / wikiTableParamLineBreak', name='wikiTableSpecialLine')
wikiTableNormalLine = Choice([wikiTableLineCells, wikiTableLineHeader, wikiTableEmptyCell], expression='wikiTableLineCells / wikiTableLineHeader / wikiTableEmptyCell', name='wikiTableNormalLine')
wikiTableLine = Sequence([NextNot(TABLE_END, expression='!TABLE_END'), Choice([wikiTableSpecialLine, wikiTableNormalLine], expression='wikiTableSpecialLine / wikiTableNormalLine')], expression='!TABLE_END (wikiTableSpecialLine / wikiTableNormalLine)', name='wikiTableLine')
wikiTableContent = Choice([wikiTableLine, wikiTable, EOL], expression='wikiTableLine / wikiTable / EOL', name='wikiTableContent')
wikiTableBegin = Sequence([TABLE_BEGIN, Repetition(wikiTableParameters, numMin=False, numMax=False, expression='wikiTableParameters*')], expression='TABLE_BEGIN wikiTableParameters*', name='wikiTableBegin')(liftValue)
wikiTable **= Sequence([wikiTableBegin, Repetition(EOL, numMin=False, numMax=False, expression='EOL*'), Repetition(wikiTableContent, numMin=False, numMax=False, expression='wikiTableContent*'), TABLE_END, EOL], expression='wikiTableBegin EOL* wikiTableContent* TABLE_END EOL', name='wikiTable')(liftValue)

body = Repetition(Choice([list, horizontalRule, preformattedGroup, title, wikiTable, EOL, paragraphs, invalidLine, EOL], expression='list / horizontalRule / preformattedGroup / title / wikiTable / EOL / paragraphs / invalidLine / EOL'), numMin=1, numMax=False, expression='(list / horizontalRule / preformattedGroup / title / wikiTable / EOL / paragraphs / invalidLine / EOL)+', name='body')



wikitextParser._recordPatterns(vars())
wikitextParser._setTopPattern("body")
wikitextParser.grammarTitle = "wikitext"
wikitextParser.filename = "wikitextParser.py"
