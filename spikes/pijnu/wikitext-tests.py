# get the parser
from pijnu import makeParser
mediawikiGrammar = file("mediawiki.pijnu").read()
mediawikiParser = makeParser(mediawikiGrammar)

# use it
mediawikiParser.italicText.test("''test''")

mediawikiParser.boldText.test("'''test'''")

mediawikiParser.simpleInternalLink.test("[[article]]")

mediawikiParser.advancedInternalLink.test("[[article|alternate]]")

mediawikiParser.italicText.findAll("Here, we have '''''bold and italic''' and italic only''.")

source = file("wikitext.txt").read()

print "\nLet's get all the external links of the article:"
print mediawikiParser.url.findAll(source)

print "\nLet's get all the interna links of the article:"
print mediawikiParser.internalLink.findAll(source)
