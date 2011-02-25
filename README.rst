Goals
=====
* Possible (to represent MediaWiki syntax)
* Extensible per project (for {for} syntax, DekiWiki conditionals, includes, templates, etc.)
* It is not necessary to implement those MediaWiki language features which make no sense outside the MediaWiki product: for example, category links.
* Easier to comprehend than MW's existing formatter

Ungoals
=======
* It is not necessary to be bug-for-bug compatible with MW. We can't constrain ourselves to give the exact same output for egregiously bad wikisyntax; we'll make a mess, which kills our goal of being easy to understand. We should catch common errors like bad quote nesting but not go out of our minds to be bug-for-bug compatible. After all, MW itself changes the language in every release. Let them chase us.

Parser libs
===========
In the following lists, (+) signifies a pro, (-) a con, and (.) a neutral point.

LEPL
----
* (+) Supports ambiguous grammars
* (o) Idiosyncratic syntax with lots of operator overloading (even slices!)
* (o) Slow (http://www.quora.com/What-is-the-best-parser-generator-for-Python/answer/Matthew-Lloyd)

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
* (.) Recursive descent (LL)
* (+) Easier to write and debug?
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
  * Useful background discussion by the folks who wrote the BNF attempt: http://www.mediawiki.org/wiki/Talk:Markup_spec
  * The flex markup looks to have naive apostrophe jungle state rules: http://www.mediawiki.org/wiki/Markup_spec/flex
  * mwlib has a pretty clean, decoupled Python impl. See styleanalyzer.py.
  * When rebalancing '''hi''' <b>''mo</b>m'', the algorithm seems to be something like this: read left to right, building a tag stack as we go. If we hit a closer that doesn't match what's on the top of the stack (1), close what's on the top (2), and let the closer through. HOWEVER, also put (1) onto another stack (or single var?) and, after doing step (2), push that stack onto the tag stack.

* (Done.) Get a parse tree out of a lib.
* Think about extensibility
* Get apostrophes working (to test ambiguity support).
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
