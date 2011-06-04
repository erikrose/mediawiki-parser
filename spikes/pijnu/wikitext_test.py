# get the parser
from pijnu import makeParser
mediawikiGrammar = file("mediawiki.pijnu").read()
mediawikiParser = makeParser(mediawikiGrammar)

# import the source in a utf-8 string for parseAllQuotes
import codecs
from apostropheParser import parseAllQuotes
fileObj = codecs.open("wikitext.txt", "r", "utf-8")
source = fileObj.read()
#source = parseAllQuotes(source)

# reconvert it back to bytes for Pijnu
backToBytes = source.encode("utf-8")
mediawikiParser.test(backToBytes)


print "\nLet's get all the external links of the article:"
print mediawikiParser.url.findAll(backToBytes)

print "\nLet's get all the internal links of the article:"
print mediawikiParser.internalLink.findAll(backToBytes)

print "\nLet's get all the templates of the article:" # Fails
print mediawikiParser.templateName.findAll(backToBytes)