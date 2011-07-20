# -*- coding: utf8 -*-

# get the parser
from pijnu import makeParser
preprocessorGrammar = file("preprocessor.pijnu").read()
makeParser(preprocessorGrammar)

mediawikiGrammar = file("mediawiki.pijnu").read()
makeParser(mediawikiGrammar)

templates = {'template1': 'Content of template1.',
             'template 2': '"Template 2" has 2 parameters: {{{1}}} and: {{{name|default}}}!',
             'Template with': 'test {{{1}}} {{{2}}}'}

from preprocessor import make_parser
preprocessor = make_parser(templates)

from html import make_parser
parser = make_parser()

# import the source in a utf-8 string
import codecs
fileObj = codecs.open("wikitext.txt", "r", "utf-8")
source = fileObj.read()

# The last line of the file will not be parsed correctly if
# there is no newline at the end of file, so, we add one.
if source[-1] != '\n':
  source += '\n'

preprocessed_text = preprocessor.parse(source)

print preprocessed_text.treeView()

tree = parser.parse(preprocessed_text.leaves())
print tree.leaves()
