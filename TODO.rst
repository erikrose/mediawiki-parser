===================================================================  ==============  =======================================================
Syntax type (example)                                                Implementation  Remark
===================================================================  ==============  =======================================================
Redirection (#REDIRECT[])                                            .
Titles, levels 1 to 6 (==Title==)                                    ¤¤¤
Paragraphs (correctly combine inline text)                           ¤
Bold and italic (<i>, <b>, "''", "'''")                              ¤¤
Internal links ([[Namespace:Title#section|text]])                    ¤               This will include files, categories and interwiki links
External links ([http://www.mozilla.org title])                      ¤¤
Inline URLs                                                          ¤¤
Safe HTML tags (<table>, <i>, <b>...)                                ¤
HTML entities (invalid &xxxx; -> &amp;xxxx; "<" -> &lt;)             .
Unsafe HTML tags (<script>, <iframe> and any non safe tag)           ¤
Preformatted paragraph (<pre> or " ")                                ¤¤
Unformatted sections (<nowiki>)                                      ¤¤
Ordered lists ("#", "##"...)                                         ¤¤
Unordered lists ("*", "**"...)                                       ¤¤
Definition lists (<dl>, <dt>, <dd>, ":", ";")                        ¤
Templates ({{template|parameter=value}})                             ¤¤
Template parameter placeholders ({{{1}}, {{{param_name}}...)         .
WikiTables                                                           ¤¤
Magic links (ISBN, RFC...)                                           .               Is that really needed?
Horizontal rules (----)                                              ¤
Galleries                                                            .
Behavior switches (__toc__, __notoc__...)                            .
===================================================================  ==============  =======================================================

=======  ==============================
Legend:
=======  ==============================
.        Nothing done
¤        Some tests done
¤¤       Partially implemented
¤¤¤      Totally implemented and tested
=======  ==============================