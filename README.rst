Goals
=====
* Possible (to represent MediaWiki syntax). There is no such thing as invalid wiki markup, so we have to make some sense out of anything.
* Extensible per project (for {for} syntax, DekiWiki conditionals, includes, templates, etc.)
* Easier to comprehend than MW's existing formatter
* Must work with Unicode input (Japanese, for example)


Ungoals
=======
* Implement those MediaWiki language features which make no sense outside the MediaWiki product: for example, category links.
* Be bug-for-bug compatible with MW. We can't constrain ourselves to give the exact same output for egregiously bad wikisyntax; we'll make a mess, which kills our goal of being easy to understand. We should catch common errors like bad quote nesting but not go out of our minds to be bug-for-bug compatible. After all, MW itself changes the language in every release. Let them chase us.


MW language properties
======================
* Unambiguous. Rats-based Sweble parses it, and Rats is a PEG-based lib, and PEGs can't represent unambiguous grammars, according to http://en.wikipedia.org/wiki/Parsing_expression_grammar.


Parser libs
===========
See:

* http://wiki.python.org/moin/LanguageParsing
* http://en.wikipedia.org/wiki/Comparison_of_parser_generators

In the following lists, (+) signifies a pro, (-) a con, and (.) a neutral point.

LEPL
----
* (.) Supports ambiguous grammars (doesn't matter: MW is unambiguous)
* (.) Idiosyncratic syntax with lots of operator overloading (even slices!)
* (.) Slow (http://www.quora.com/What-is-the-best-parser-generator-for-Python/answer/Matthew-Lloyd)
* (+) Excellent docs

PLY
---
* (.) LALR or, optionally, SLR (Can SLR look ahead farther? No: actually, it has no lookahead.)
* (-) LALR(1), which is grossly insufficient for MW. I think it's about a lookahead of 4, which we'd have to take care of ourselves, probably making the code hard to comprehend in the process.
* (+) Modal lexer and parser. (Is this necessary? Understand what can't be BNF'd about apostrophe jungles and lists.)
* (+) Easy to translate into C later
* (.) Can turn off magic autodiscovery
* (-) Potential for yacc to guess wrong about how to assemble symbols: reduce/reduce and shift/reduce errors
* (+) Much faster than PyParsing? http://www.mefeedia.com/watch/29412150 at 23:58 suggests it's 5.5x faster. More benchmarks (ANTLR and more): http://www.dalkescientific.com/writings/diary/archive/2007/11/03/antlr_java.html
* (-) A bit more verbose (but very clear)

PyParsing
---------
* (.) Recursive descent (LL) of PEGs
* (+) Packrat, so O(n)
* (+) Easy to write
* (-) "[An LL(k) parser] may defer error detection to a different branch of the grammar due to backtracking, often making errors harder to localize across disjunctions with long common prefixes."—Wikipedia. I had that problem when writing a simple italics/bold parser: you have to keep the recursion stack in your head to make any sense of the debug info. I eventually gave up trying to fix it.

PyBison
-------
Not researched in depth.

* (+) Claims to be nearly as fast as C
* (-) Requires a C build step

ANTLR
-----
* (-) Separate code generation step
* (-) Slow because it generates a lot of function calls
* (+) Can parse LL(k) grammars (arbitrary lookahead)

SPARK
-----
* (+) Has an implementation of an Earley parser, which can do arbitrary lookahead in n^3 worst case.

NLTK
----
* (+) Another Earley parser
* (+) Long-lived. Under active development by multiple authors. Last released 4/2011.
* (.) There's a good, free book about the project: http://nltk.googlecode.com/svn/trunk/doc/book/ch08.html. Not sure how good the documentation about the code itself is, though.
* (-) An enormous dependency

PyGgy (http://pypi.python.org/pypi/pyggy/0.3)
---------------------------------------------
* (.) Untested
* (.) GLR parser
* (+) Public domain
* (-) Might be dead (the home page has disappeared: http://www.lava.net/~newsham/pyggy/)
* (-) "PyGgy was written and tested with Python 2.2.3." (in 2003)

Pijnu (http://spir.wikidot.com/pijnu)
-------------------------------------
* (+) PEG. Easy, easy grammar definition.
* (.) Looks promising but not mature. Author has given no thought to speed but much to clarity.
* (-) Build step
* (-) Currently no Unicode support
* (+) Great docs: http://spir.wikidot.com/pijnu-user-guide
* (+) Great error feedback
* (+) The generated code looks like what you have to hand-write for PyParsing (see the user guide).
* (+) Can handle having Unicode chars in the input.
* (.) Can it handle having Unicode chars as part of parse rules? We might need guillemets.

PyMeta (https://launchpad.net/pymeta)
-------------------------------------
* (.) PEG. Grammar defined in a DSL.
* (+) No build step; converts grammar from a DSL at runtime.
* (+) Good docs in the code
* (-) Nobody's touched it for a year.

PyMeta2 (http://www.allbuttonspressed.com/projects/pymeta)
----------------------------------------------------------
* (.) Is a port of PyMeta to "the simplified OMeta 2 syntax" (new DSL syntax).

Ppeg (https://bitbucket.org/pmoore/ppeg/)
-----------------------------------------
* (-) Not in Python: Python code (21 kB) code is just an API for a C parser (172 kB)

pyPEG (http://fdik.org/pyPEG/)
------------------------------
* (.) Only 340 lines of Python
* (-) Similar to Pijnu but much less easy to use


Previous implementations
========================
See: http://www.mediawiki.org/wiki/Alternative_parsers

Py-wikimarkup (https://github.com/dcramer/py-wikimarkup)
--------------------------------------------------------
* (+) Probably works (untested)
* (-) Direct transformation from wikitext to HTML (generates no AST)
* (-) As a direct port of the MW PHP, it is very difficult to understand or extend.
* (-) Because it is based on a sequence of perilously combined regexes which interact in surprising ways, it, like MW proper, sometimes yields surprising output.

mwlib (http://code.pediapress.com/wiki/wiki/mwlib)
--------------------------------------------------
* (+) Works well, lots of unittests already defined and successfully passed
* (+) Generates an AST
* (.) Implements its own lexer/parser (see mwlib/refine/core.py and mwlib/refine/_core.pyx: compiled token walker)
* (.) Seems to: tokenize the text and then apply ~20 different parsers one by one (see mwlib/refine/core.py#928 and #635)
* (-) Structure of the code somewhat hard to understand (uparser.py vs old_uparser.py, etc.)
* (-) Lot of code not related to parsing (fetching articles, (un)zip files, API stuff, output for ODF, Latex, etc. that should be more isolated from the parsing part)

mediawiki_parser (this one)
---------------------------
* (+) Good start (parser + lexer, unittests)
* (.) Currently using PLY but will be abandoned due to the lack of lookahead
* (-) Currently incomplete syntax
* (-) Currently generates no AST

Sweble (http://sweble.org/gitweb/)
----------------------------------
* (+) Works well: demo here: http://sweble.org/crystalball/
* (.) Interesting description of the parser philosophy: http://sweble.org/gitweb/?p=sweble-wikitext.git;f=swc-parser-lazy/src/main/autogen/org/sweble/wikitext/lazy/parser/Content.rats;h=e6f0e250b01c3c76ce85a38ba75eb0fcbe636d7a;hb=899a68c087fb6439b4d60c3e6d3c7c025ac0d663
* (.) Same for preprocessor: http://sweble.org/gitweb/?p=sweble-wikitext.git;a=blob;f=swc-parser-lazy/src/main/autogen/org/sweble/wikitext/lazy/preprocessor/Grammar.rats;h=c13e8a662178516f730d4c63115ba59210aa2481;hb=899a68c087fb6439b4d60c3e6d3c7c025ac0d663
* (.) Uses the packrat xtc parser: http://www.cs.nyu.edu/rgrimm/xtc/rats.html
* (-) Not simple...


Algorithms
==========

Lexer + parser (e.g. PLY)
-------------------------
* (+) Easy to use and debug
* (+) Stateful (specific simple rules for each context)
* (-) Not enough lookahead in the case of LR(1) parser

Recursive descent of CFGs
------------------------------------------
* (+) No separate lexer and parser
* (+) Memoization ("packrat") makes it run in O(n)
* (.) Recursive
* (-) May require large amounts of memory
* (-) Quite hard to read and debug

Recursive descent of PEGs (e.g. Rats, PyParsing)
-------------------------------------
* (+) No separate lexer and parser
* (+) O(n) with packrat
* (+) Resolves ambiguity by having precedence orders for productions. As a result, it is easy to extend a PEG with productions for use in special situations without wrecking the wider grammar. This could be a very big deal for our extensibility story.
* (+) We can rip off Sweble's grammar.

Earley parser (e.g. Spark, NLTK)
--------------------------------
* (.) O(n³) in the general case, O(n²) for unambiguous grammars and O(n) for almost all LR(k) grammars
* (.) Meant for context-free grammars, but may also work in context-free subsections of context-sensitive grammars according to this publication: http://danielmattosroberts.com/earley/context-sensitive-earley.pdf

GLR parser (e.g. Pyggy)
-----------------------
* (.) Supports ambiguous grammars (which MW isn't)
* (+) O(n) on deterministic grammars


Previous work
=============
* (+) OCaml lexer implementation: http://www.mediawiki.org/wiki/MediaWiki_lexer
* (+) Markup spec: http://www.mediawiki.org/wiki/Markup_spec
* (+) BNF grammar: http://www.mediawiki.org/wiki/Markup_spec/BNF

  * (+) Corresponds closely to yacc input format
  * (+) Pretty comprehensive: lots of English describing corner cases and error recovery
  * (.) Also discusses render phase

* (+) EBNF grammar: http://www.mediawiki.org/wiki/Markup_spec/EBNF

  * (+) Well-organized and concise
  * (-) Nothing about error recovery
  * (-) Wrong in some places (like the header rules that chew up whitespace)

* (+) flex implementation: http://www.mediawiki.org/wiki/Markup_spec/flex

  * (-) Prints HTML directly; doesn't seem to have a consume/parse/render flow
  * (-) Doesn't seem very comprehensive. I converted it quickly to a PLY lex implementation (fixed the \135 codes and such), and it didn't seem to do a particularly good job recognizing things. There are some heuristics we can glean from it, however, like stripping any trailing comma or period off a scanned URL. Another example is that it doesn't look like it handles the "== H2 ===" case correctly.


Milestones
==========
* Understand what's so hard about apostrophes and lists (http://www.mediawiki.org/wiki/Markup_spec/BNF/Inline_text).

  * This claims MW isn't context-free and has C code on how to hack through the apostrophe jungle: http://web.archiveorange.com/archive/v/e7MXfq0OoW0nCOGyX0oa
  * This claims that MW is probably context-free: http://www.mediawiki.org/wiki/User_talk:Kanor#Response_to_article_in_Meatball
  * Useful background discussion by the folks who wrote the BNF attempt: http://www.mediawiki.org/wiki/Talk:Markup_spec
  * The flex markup looks to have naive apostrophe jungle state rules: http://www.mediawiki.org/wiki/Markup_spec/flex
  * mwlib has a pretty clean, decoupled Python impl. See styleanalyzer.py.
  * When rebalancing '''hi''' <b>''mo</b>m'', the algorithm seems to be something like this: read left to right, building a tag stack as we go. If we hit a closer that doesn't match what's on the top of the stack (1), close what's on the top (2), and let the closer through. HOWEVER, also put (1) onto another stack (or single var?) and, after doing step (2), push that stack onto the tag stack.

* (Done.) Get a parse tree out of a lib.
* Think about extensibility
* Get apostrophes working.
* Implement productions, tag by tag


Notes
=====
If we build the parse tree in custom lexer callbacks, we can make it an ElementTree or whatever we want--meaning we can use XPath on it later if we want.


Quasi Gantt chart
=================

::

  Re-examing parsing algorithm,
  & implement links                       |----|----|----   Bold/Italics/Apostrophe Jungles (3 weeks)                                      |----|----|----   HTML formatter |----   Showfor support |--
  & other long-lookahead productions
  (3 weeks)                                                 Simple productions:
                                                            Paragraphs (3 days)                                                            |--
                                                            HRs (1 day)                                                                    |
                                                            magic words (3 days)                                                           |--

                                                            Tables (long lookahead?) (1 week)                                              |----

                                                            One person should do these:
                                                            Includes (long lookahead?) (2 weeks)                                           |----|----
                                                            Templates w/params (long lookahead?) (2 weeks)                                 |----|----

                                                            Redirects (3 days)                                                             |--
                                                            Naked URLs (long lookahead but doable in lexer?) (1 day)                       |
                                                            Headers (long lookahead but doable in lexer) (done for now)
                                                            Entities (done for now)
                                                            Behavior switches (optional) (4 days--will require some architecture thinking) |---

                                                            HTML tags: probably just tokenize and preserve them through the parser and     |----|----|----
                                                              then have a separate post-parse step to balance and validate them and, for
                                                              example, escape any invalid ones (3 weeks)
