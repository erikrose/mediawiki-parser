Presentation
============

This is a parser for MediaWiki's (MW) syntax. It's goal is to transform wikitext into an abstract syntax tree (AST) and then render this AST into various formats such as plain text and HTML.


How it works
============ 

Two files, preprocessor.pijnu and mediawiki.pijnu describe the MW syntax using patterns that form a grammar. Another Python tool called Pijnu will interpret those grammars and use them to match the wikitext content and build the AST.

Then, specific Python functions will render the leaves of the AST into the wanted format.

The reason why we use two grammars is that we will first substitute the templates in the wikitext with a preprocessor before actually parsing the content of the page.


How to test
===========

The current simplest way to test the tool is to put wikitext inside the wikitext.txt file. Then, run:

::

 python parser.py
 
and the wikitext will be rendered as HTML in the article.htm file.

Other ways might be implemented in the future.

Unit tests
----------

Install nose and run:

::

 cd /PATH/TO/mediawiki-parser/
 ln -s ../mediawiki-parser/ mediawiki_parser
 export PYTHONPATH=/PATH/TO/mediawiki-parser/:/PATH/TO/pijnu/
 nosetests tests

How to use in a program
=======================

Example for HTML
----------------
In order to use this tool to render wikitext into HTML in a Python program, you can use the following lines:

::

 templates = {}
 allowed_tags = []
 allowed_self_closing_tags = []
 allowed_attributes = []
 interwiki = {}
 namespaces = {}
 
 from preprocessor import make_parser
 preprocessor = make_parser(templates)

 from html import make_parser
 parser = make_parser(allowed_tags, allowed_self_closing_tags, allowed_attributes, interwiki, namespaces)

 preprocessed_text = preprocessor.parse(source)
 output = parser.parse(preprocessed_text.leaves())

The `output` string will contain the rendered HTML. You should describe the behavior you expect by filling the variables of the first lines:
 * if the wikitext calls foreign templates, put their names and content in the `templates` dict (e.g.: `{'my template': 'my template content'}`)
 * if some HTML tags are allowed on your wiki, list them in the `allowed_tags` list (e.g.: `['center', 'big', 'small', 'span']`; avoid `'script'` and some others, for security reasons)
 * if some self-closing HTML tags are allowed on your wiki, list them in the `allowed_self_closing_tags` list (e.g.: `['br', 'hr']`; avoid `'script'` and some others, for security reasons)
 * if some HTML tags are allowed on your wiki, list the attributes they can use the `allowed_attributes` list (e.g.: `['style', 'class']`; avoid `'onclick'` and some others, for security reasons)
 * if you want to be able to use interwiki links, list the foreign wikis in the `interwiki` dict (e.g.: `{'fr': 'http://fr.wikipedia.org/wiki/'}`) 
 * if you want to be able to distinguish between standard links, file inclusions or categories, list the namespaces of your wiki in the `namespaces` dict (e.g.: `{'Template': 10, 'Category': 14, 'File': 6}` where the numbers are the namespace codes used in MW)

Example for text
----------------
In order to use this tool to render wikitext into text in a Python program, you can use the following lines:

::

 templates = {}
 
 from preprocessor import make_parser
 preprocessor = make_parser(templates)

 from text import make_parser
 parser = make_parser()

 preprocessed_text = preprocessor.parse(source)
 output = parser.parse(preprocessed_text.leaves())

The `output` string will contain the rendered text.
If the wikitext calls foreign templates, put their names and content in the `templates` dict (e.g.: `{'my template': 'my template content'}`)

Example for templates substitution
----------------------------------
If you just want to replace the templates in a given wikitext, you can just call the preprocessor and no rendering postprocessor:

::

 templates = {}
 
 from preprocessor import make_parser
 preprocessor = make_parser(templates)

 output = preprocessor.parse(source)

The `output` string will contain the rendered wikitext.
Put the templates names and content in the `templates` dict (e.g.: `{'my template': 'my template content'}`)


Known bugs
==========

This tool should be able to render any wikitext page into text or HTML.

However, it does not intent to be bug-for-bug compatible with MW. For instance, using HTML entities in template calls (e.g.: `'{{temp&copy;late}}`') is currently not supported.

Please don't hesitate to report bugs that you may find when using this tool.
