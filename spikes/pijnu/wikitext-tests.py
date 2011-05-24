# -*- coding: utf8 -*-
# get the parser
from pijnu import makeParser
mediawikiGrammar = file("mediawiki.pijnu").read()
mediawikiParser = makeParser(mediawikiGrammar)

# use it
# Titles
mediawikiParser.test("=Title 1=\n")
mediawikiParser.test("== Title 2 ==\n")
mediawikiParser.test("===Title 3===text to be ignored\n")
mediawikiParser.test("==== Title 4 ====\n")
mediawikiParser.test("===== Title 5 =====\n")
mediawikiParser.test("====== Title 6 ======\n")

# Formatted titles
mediawikiParser.test("= [[a link]] =\n")
mediawikiParser.test("== ''italic text'' ==\n")
mediawikiParser.test("=== '''bold text''' ===\n")
mediawikiParser.test("==== ''[[Title 4|formatted link]]'' ====\n") #Fails
mediawikiParser.test("===== {{Title 5}} =====\n")
mediawikiParser.test("====== { Title 6} ======\n")

# nowiki
mediawikiParser.nowiki.test("<nowiki>some [[text]] that should {{not}} be changed</nowiki>")
mediawikiParser.test("This should [[be plain text\n")

# Links
mediawikiParser.inline.test("[[article]]")
mediawikiParser.inline.test("[[article|alternate]]")
mediawikiParser.inline.test("An URL: http://www.mozilla.org")
mediawikiParser.inline.test("[http://www.mozilla.org this is an ''external'' link]")
mediawikiParser.inline.test("<a href=\"http://www.mozilla.org\">this is an ''external'' link</a>") #Fails

# Italic and bold
mediawikiParser.inline.test("Here, we have ''italic'' text.")
mediawikiParser.inline.test("Here, we have '''bold''' text.")
mediawikiParser.inline.test("Here, we have '''''bold and italic''''' text.")
mediawikiParser.inline.test("Here, we have ''italic only and '''bold and italic''''' text.")
mediawikiParser.inline.test("Here, we have '''bold only and ''bold and italic''''' text.")
mediawikiParser.inline.test("Here, we have '''''bold and italic''' and italic only''.")
mediawikiParser.inline.test("Here, we have '''''bold and italic'' and bold only'''.")
mediawikiParser.inline.test("Here, we have ''italic, '''bold and italic''' and italic only''.")
mediawikiParser.inline.test("Here, we have '''bold, ''bold and italic'' and bold only'''.")

# Templates
mediawikiParser.advancedTemplate.test("{{Template whith|1=parameter| 2 = parameters }}")
mediawikiParser.advancedTemplate.test("""{{Template which
 | is = test
 | multi = test
 | lines = test
}}""")
mediawikiParser.inline.test("A template {{Template whith|1=parameter| 2 = parameters }} inside a text.")
mediawikiParser.inline.test("Formatted arguments in a template {{Template whith|1='''parameter'''| 2 = ''parameters'' }}.")
mediawikiParser.inline.test("A '''template {{Template whith|1=parameter| 2 = parameters }} inside formatted''' text.") #Fails

# Verifications for special characters
mediawikiParser.inline.test("Some Unicode characters: 你好.")
mediawikiParser.inline.test("This # should pass.")
mediawikiParser.inline.test("This { should pass.")
mediawikiParser.inline.test("This } should pass.")
mediawikiParser.inline.test("This < should pass.") #Fails
mediawikiParser.inline.test("This > should pass.") #Fails
mediawikiParser.inline.test("This [ should pass.") #Fails
mediawikiParser.inline.test("This ] should pass.") #Fails
mediawikiParser.inline.test("This = should pass.") #Fails

source = file("wikitext.txt").read()

print "\nLet's get all the external links of the article:"
print mediawikiParser.url.findAll(source)

print "\nLet's get all the internal links of the article:"
print mediawikiParser.internalLink.findAll(source)

print "\nLet's get all the templates of the article:" # Fails
print mediawikiParser.templateName.findAll(source)
