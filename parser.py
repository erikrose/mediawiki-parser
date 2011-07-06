# -*- coding: utf8 -*-
import config
print "Output will be", config.output

# get the parser
from pijnu import makeParser
mediawikiGrammar = file("mediawiki.pijnu").read()
mediawikiParser = makeParser(mediawikiGrammar)

# import the source in a utf-8 string
import codecs
from apostrophes import parseAllQuotes
fileObj = codecs.open("wikitext.txt", "r", "utf-8")
source = fileObj.read()

# The last line of the file will not be parsed correctly if
# there is no newline at the end of file, so, we add one.
if source[-1] != '\n':
  source += '\n'

tree = mediawikiParser.parse(source)

print tree.leaves()
