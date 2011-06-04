# -*- coding: utf8 -*-
# get the parser
from pijnu import makeParser
mediawikiGrammar = file("mediawiki.pijnu").read()
mediawikiParser = makeParser(mediawikiGrammar)


print "\n\n== Testing titles and nowiki sections =="

test_suite_dict = {
    '=Title 1=\n' : "[title1:[rawText:'Title 1']]",
    '== Title 2 ==\n' : "[title2:[rawText:' Title 2 ']]",
    '===Title 3===text to be ignored\n' : "[title3:[rawText:'Title 3']]",
    '==== Title 4 ====\n' : "[title4:[rawText:' Title 4 ']]",
    '===== Title 5 =====\n' : "[title5:[rawText:' Title 5 ']]",
    '====== Title 6 ======\n' : "[title6:[rawText:' Title 6 ']]",
    '= [[a link]] =\n' : "[title1:[rawText:' '  simpleInternalLink:'a link'  rawText:' ']]",
    "== ''italic text'' ==\n" : "[title2:[rawText:' <em>italic text</em> ']]",
    "=== '''bold text''' ===\n" : "[title3:[rawText:' <strong>bold text</strong> ']]",
    "==== ''[[Title 4|formatted link]]'' ====\n" : "[title4:[rawText:' <em></em>'  advancedInternalLink:[templateName:'Title 4'  @inline@:[rawText:'formatted link']]  rawText:'<em> </em>']]",
    '===== {{Title 5}} =====\n' : "[title5:[rawText:' '  simpleTemplate:'Title 5'  rawText:' ']]",
    '====== { Title 6} ======\n' : "[title6:[rawText:' { Title 6} ']]",
    '<nowiki>some [[text]] that should {{not}} be changed</nowiki>\n' : "[paragraphs:[paragraph:[nowiki:[ignoredInNowiki:'some [[text]] that should {{not}} be changed']]]]",
    'This should [[be plain text\n' : "[invalidLine:'This should [[be plain text']"
}

mediawikiParser.testSuite(test_suite_dict)


print "\n\n== Testing links =="

test_suite_dict = {
    '[[article]]' : "[simpleInternalLink:'article']",
    '[[article|alternate]]' : "[advancedInternalLink:[templateName:'article'  @inline@:[rawText:'alternate']]]",
    'An URL: http://www.mozilla.org' : "[rawText:'An URL: '  url:'http://www.mozilla.org']",
    "[http://www.mozilla.org this is an ''external'' link]" : "[externalLink:[url:'http://www.mozilla.org'  @inline@:[rawText:'this is an <em>external</em> link']]]",
    '<a href="http://www.mozilla.org">this is an \'\'external\'\' link</a>' : "[externalLink:[url:'http://www.mozilla.org'  @inline@:[rawText:'this is an <em>external</em> link']]]"
}

mediawikiParser.inline.testSuite(test_suite_dict)


print "\n\n== Testing italic and bold =="

test_suite_dict = {
    "Here, we have ''italic'' text." : "[rawText:'Here, we have <em>italic</em> text.']",
    "Here, we have '''bold''' text." : "[rawText:'Here, we have <strong>bold</strong> text.']",
    "Here, we have '''''bold and italic''''' text." : "[rawText:'Here, we have <em><strong>bold and italic</strong></em> text.']",
    "Here, we have ''italic only and '''bold and italic''''' text." : "[rawText:'Here, we have <em>italic only and <strong>bold and italic</strong></em> text.']",
    "Here, we have '''bold only and ''bold and italic''''' text." : "[rawText:'Here, we have <strong>bold only and <em>bold and italic</em></strong> text.']",
    "Here, we have '''''bold and italic''' and italic only''." : "[rawText:'Here, we have <em><strong>bold and italic</strong> and italic only</em>.']",
    "Here, we have '''''bold and italic'' and bold only'''." : "[rawText:'Here, we have <strong><em>bold and italic</em> and bold only</strong>.']",
    "Here, we have ''italic, '''bold and italic''' and italic only''." : "[rawText:'Here, we have <em>italic, <strong>bold and italic</strong> and italic only</em>.']",
    "Here, we have '''bold, ''bold and italic'' and bold only'''." : "[rawText:'Here, we have <strong>bold, <em>bold and italic</em> and bold only</strong>.']"
}

mediawikiParser.inline.testSuite(test_suite_dict)

print "\n\n== Testing templates =="

mediawikiParser.advancedTemplate.test("{{Template whith|1=parameter| 2 = parameters }}")
mediawikiParser.advancedTemplate.test("""{{Template which
 | is = test
 | multi = test
 | lines = test
}}""")
mediawikiParser.inline.test("A template {{Template whith|1=parameter| 2 = parameters }} inside a text.")
mediawikiParser.inline.test("Formatted arguments in a template {{Template whith|1='''parameter'''| 2 = ''parameters'' }}.")
mediawikiParser.inline.test("A '''template {{Template whith|1=parameter| 2 = parameters }} inside formatted''' text.") #Fails


print "\n\n== Testing tables =="

mediawikiParser.wikiTableLine.test("| style=\"color:red\" | cell 1\n")
mediawikiParser.wikiTableFirstCell.test("style=\"color:red\" | cell 1")
mediawikiParser.wikiTableLine.test("| cell 1\n")
mediawikiParser.wikiTableLine.test("|data L2-B\n")
mediawikiParser.wikiTableOtherCell.test("|| cell 1")
mediawikiParser.wikiTableLine.test("| cell 1 || cell 2\n")
mediawikiParser.wikiTableLine.test("| cell 1 || style=\"color:red\" | cell 2\n")
mediawikiParser.wikiTableLine.test("| style=\"color:red\" | cell 1 || cell 2\n")
mediawikiParser.wikiTableLine.test("! scope=row | Line 1\n")
mediawikiParser.wikiTableSpecialLine.test("|-\n")
mediawikiParser.wikiTableLine.test("|- style=\"color:red\"\n")
mediawikiParser.wikiTable.test("""{|
! cellA
! cellB
|- style="color:red"
| cell C
| cell D
|}
""")
mediawikiParser.wikiTable.test("""{|
|+ Table {{title}}
| cell 1 || cell 2
|-
| cell 3 || cell 4
|}
""")
mediawikiParser.wikiTable.test("""{| class="wikitable" {{prettyTable}}
|+ style="color:red" | Table {{title}}
|-
|
! scope=col | Title A
! scope=col | Title B
|-
! scope=row | Line 1
|data L1.A
|data L1.B
|-
! scope=row | Line 2
|data L2.A
|data L2.B
|}
""")


print "\n\n== Testing special characters =="

test_suite_dict = {
    "Some Unicode characters: 你好." : "[rawText:'Some Unicode characters: 你好.']",
    'This # should pass.' : "[rawText:'This # should pass.']",
    'This { should pass.' : "[rawText:'This { should pass.']",
    'This } should pass.' : "[rawText:'This } should pass.']",
    'This < should pass.' : "[rawText:'This < should pass.']",
    'This > should pass.' : "[rawText:'This > should pass.']",
    'This [ should pass.' : "[rawText:'This [ should pass.']",
    'This ] should pass.' : "[rawText:'This ] should pass.']",
    'This = should pass.' : "[rawText:'This = should pass.']",
    'This - should pass.' : "[rawText:'This - should pass.']"
}

mediawikiParser.inline.testSuite(test_suite_dict)


print "\n\n== Testing lists =="

test_suite_dict = {
    '* text\n' : "[list:[bulletListLeaf:[rawText:' text']]]",
    '** other text\n' : "[list:[@bulletSubList@:[bulletListLeaf:[rawText:' other text']]]]",
    '# text\n' : "[list:[numberListLeaf:[rawText:' text']]]",
    "## ''more text''\n" : "[list:[@numberSubList@:[numberListLeaf:[rawText:' <em>more text</em>']]]]",
    "### ''other text''\n" : "[list:[@numberSubList@:[@numberSubList@:[numberListLeaf:[rawText:' <em>other text</em>']]]]]",
    ": '''more text'''\n" : "[list:[colonListLeaf:[rawText:' <strong>more text</strong>']]]",
    '; still more [[text]]\n' : "[list:[semiColonListLeaf:[rawText:' still more '  simpleInternalLink:'text']]]",
    ':* more complicated case\n' : "[list:[@colonSubList@:[bulletListLeaf:[rawText:' more complicated case']]]]",
    ';* same as previous line\n' : "[list:[@semiColonSubList@:[bulletListLeaf:[rawText:' same as previous line']]]]",
    '::** another complicated case\n' : "[list:[@colonSubList@:[@colonSubList@:[@bulletSubList@:[bulletListLeaf:[rawText:' another complicated case']]]]]]",
    '*: one more\n' : "[list:[@bulletSubList@:[colonListLeaf:[rawText:' one more']]]]",
    "*:*;#*: this is '''correct''' syntax!\n" : "[list:[@bulletSubList@:[@colonSubList@:[@bulletSubList@:[@semiColonSubList@:[@numberSubList@:[@bulletSubList@:[colonListLeaf:[rawText:' this is <strong>correct</strong> syntax!']]]]]]]]]"
}

mediawikiParser.testSuite(test_suite_dict)
