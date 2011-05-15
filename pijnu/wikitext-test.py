# get the parser
from pijnu import makeParser
mediawikiGrammar = file("mediawiki.pijnu").read()
mediawikiParser = makeParser(mediawikiGrammar)
print mediawikiParser

# use it
source = file("wikitext.txt").read()
mediawikiParser.test(source)
