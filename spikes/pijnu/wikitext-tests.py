# get the parser
from pijnu import makeParser
mediawikiGrammar = file("mediawiki.pijnu").read()
mediawikiParser = makeParser(mediawikiGrammar)

# use it
mediawikiParser.inline.test("Here, we have '''''bold and italic''' and italic only''.")
mediawikiParser.nowiki.test("<nowiki>some [[text]] that should {{not}} be changed</nowiki>")
mediawikiParser.italicText.test("''test''","parseTest")
mediawikiParser.boldText.test("'''test'''","parseTest")

mediawikiParser.simpleInternalLink.test("[[article]]")

mediawikiParser.advancedInternalLink.test("[[article|alternate]]")

mediawikiParser.inline.test("Here, we have '''''bold and italic''' and italic only''.")

mediawikiParser.test("This should [[be plain text")

mediawikiParser.advancedTemplate.test("""{{Template which
 | is = test
 | multi = test
 | lines = test
}}""")

source = file("wikitext.txt").read()

print "\nLet's get all the external links of the article:"
print mediawikiParser.url.findAll(source)

print "\nLet's get all the internal links of the article:"
print mediawikiParser.internalLink.findAll(source)

print "\nLet's get all the templates of the article:"
print mediawikiParser.templateName.findAll(source)
