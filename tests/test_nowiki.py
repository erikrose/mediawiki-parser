# -*- coding: utf8 -*-

import wikitextParser
mediawikiParser = wikitextParser.wikitextParser

test_suite_dict = {
        '<nowiki>some [[text]] that should {{not}} be changed</nowiki>\n' : "[paragraphs:[paragraph:[nowiki:[ignoredInNowiki:'some [[text]] that should {{not}} be changed']]]]"
}
mediawikiParser.testSuite(test_suite_dict)
