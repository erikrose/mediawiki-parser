# -*- coding: utf8 -*-

import wikitextParser
mediawikiParser = wikitextParser.wikitextParser

test_suite_dict = {
    '[[article]]' : "[simpleInternalLink:'article']",
    '[[article|alternate]]' : "[advancedInternalLink:[templateName:'article'  @cleanInline@:[rawText:'alternate']]]",
    'An URL: http://www.mozilla.org' : "[rawText:'An URL: '  url:'http://www.mozilla.org']",
    "[http://www.mozilla.org this is an ''external'' link]" : "[externalLink:[url:'http://www.mozilla.org'  @cleanInline@:[rawText:'this is an <em>external</em> link']]]",
    '<a href="http://www.mozilla.org">this is an \'\'external\'\' link</a>' : "[rawText:'<a href=\"'  url:'http://www.mozilla.org'  rawText:'\">this is an <em>external</em> link</a>']"
}

def test():
    mediawikiParser.inline.testSuite(test_suite_dict)

if __name__ == "__main__":
    test()