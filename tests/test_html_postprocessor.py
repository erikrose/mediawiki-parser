# -*- coding: utf8 -*-

from mediawiki_parser.tests import PostprocessorTestCase


class HTMLBackendTests(PostprocessorTestCase):
    def test_simple_title2(self):
        source = '== A title ==\n'
        result = "<h2> A title </h2>\n"
        self.parsed_equal_string(source, result, 'wikitext', {}, 'html')

    def test_simple_title6(self):
        source = '====== Test! ======\n'
        result = "<h6> Test! </h6>\n"
        self.parsed_equal_string(source, result, 'wikitext', {}, 'html')

    def test_simple_allowed_open_tag(self):
        source = 'a<span>test'
        result = 'a<span>test'
        self.parsed_equal_string(source, result, 'inline', {}, 'html')

    def test_complex_allowed_open_tag(self):
        """ The postprocessor should remove the disallowed attributes. """
        source = '<span class="wikitext" style="color:red" onclick="javascript:alert()">'
        result = '<span class="wikitext" style="color:red">'
        self.parsed_equal_string(source, result, 'inline', {}, 'html')

    def test_simple_disallowed_open_tag(self):
        source = 'another <a> test'
        result = 'another &lt;a&gt; test'
        self.parsed_equal_string(source, result, 'inline', {}, 'html')

    def test_complex_disallowed_open_tag(self):
        """ The postprocessor doesn't remove the disallowed attributes, but outputs everything as text. """
        source = '<a href="test" class="test" style="color:red" anything="anything">'
        result = '&lt;a href="test" class="test" style="color:red" anything="anything"&gt;'
        self.parsed_equal_string(source, result, 'inline', {}, 'html')

    def test_simple_allowed_autoclose_tag(self):
        source = 'a<br />test'
        result = 'a<br />test'
        self.parsed_equal_string(source, result, 'inline', {}, 'html')

    def test_complex_allowed_autoclose_tag(self):
        source = 'one more <br name="test" /> test'
        result = 'one more <br name="test" /> test'
        self.parsed_equal_string(source, result, 'inline', {}, 'html')

    def test_simple_disallowed_autoclose_tag(self):
        source = 'a<test />test'
        result = 'a&lt;test /&gt;test'
        self.parsed_equal_string(source, result, 'inline', {}, 'html')

    def test_complex_disallowed_autoclose_tag(self):
        source = '<img src="file.png" />'
        result = '&lt;img src="file.png" /&gt;'
        self.parsed_equal_string(source, result, 'inline', {}, 'html')

    def test_simple_table(self):
        source = """{|
! cellA
! cellB
|- style="color:red"
| cell C
| cell D
|}
"""
        result = """<body>
<table>
<tr>
\t<th> cellA</th>
\t<th> cellB</th>
</tr>
<tr style="color:red">
\t<td> cell C</td>
\t<td> cell D</td>
</tr>
</table>
</body>"""
        self.parsed_equal_string(source, result, None, {}, 'html')

    def test_complex_table(self):
        source = """{| style="background:blue" {{prettyTable}}
|+ style="color:red" | Table {{title|parameter}}
|-
|
! scope=col | Title A
! scope=col | Title B
|-
! scope=row | Line 1
| style="test:test" | data L1.A
|data L1.B
|-
! scope=row | Line 2
|data L2.A
|data {{template|with|parameters=L2.B}}
|}
"""
        result = """<body>
<table style="background:blue" class="prettyTable">
<tr>
\t<caption style="color:red"> Table This is the title with a parameter!</caption>
</tr>
<tr>
\t<th scope="col"> Title A</th>
\t<th scope="col"> Title B</th>
</tr>
<tr>
\t<th scope="row"> Line 1</th>
\t<td style="test:test"> data L1.A</td>
\t<td>data L1.B</td>
</tr>
<tr>
\t<th scope="row"> Line 2</th>
\t<td>data L2.A</td>
\t<td>data Template:template</td>
</tr>
</table>
</body>"""
        templates = {'prettyTable': 'class="prettyTable"',
                     'title': 'This is the title with a {{{1}}}!'}
        self.parsed_equal_string(source, result, None, templates, 'html')

    def test_nested_tables(self):
        source = """{| style="background:blue" {{prettyTable}}
|+ style="color:red" | Table {{title|1=true}}
|-
! scope=col | First (mother)
! scope=col | table
|
{| style="background:red" {{prettyTable}}
! scope=row | Second (daughter) table
|data L1.A
|data L1.B
|-
! scope=row | in the first one
|data L2.A
|data L2.B
|}
|-
| first
| table
| again
|}
"""
        result = """<body>
<table style="background:blue" class="prettyTable">
<tr>
\t<caption style="color:red"> Table This is the title, true!</caption>
</tr>
<tr>
\t<th scope="col"> First (mother)</th>
\t<th scope="col"> table</th>
\t<td>
<table style="background:red" class="prettyTable">
<tr>
\t<th scope="row"> Second (daughter) table</th>
\t<td>data L1.A</td>
\t<td>data L1.B</td>
</tr>
<tr>
\t<th scope="row"> in the first one</th>
\t<td>data L2.A</td>
\t<td>data L2.B</td>
</tr>
</table>
</td>
</tr>
<tr>
\t<td> first</td>
\t<td> table</td>
\t<td> again</td>
</tr>
</table>
</body>"""
        templates = {'prettyTable': 'class="prettyTable"',
                     'title': 'This is the title, {{{1}}}!'}
        self.parsed_equal_string(source, result, None, templates, 'html')

    def test_horizontal_rule(self):
        source = """test
----
test
"""
        result = """<body>
<p>test</p>
<hr />
<p>test</p>
</body>"""
        self.parsed_equal_string(source, result, None, {}, 'html')

    def test_preformatted_paragraph(self):
        source = """ test
 {{template}}
 test
"""
        templates = {'template': 'content'}
        result = """<body>
<pre>test
Template:template
test
</pre>
</body>"""
        self.parsed_equal_string(source, result, None, {}, 'html')

    def test_italic(self):
        source = "Here, we have ''italic'' text.\n"
        result = "<body>\n<p>Here, we have <em>italic</em> text.</p>\n</body>"
        self.parsed_equal_string(source, result, None, {}, 'html')

    def test_bold(self):
        source = "Here, we have '''bold''' text.\n"
        result = "<body>\n<p>Here, we have <strong>bold</strong> text.</p>\n</body>"
        self.parsed_equal_string(source, result, None, {}, 'html')

    def test_bold_and_italic_case1(self):
        source = "Here, we have '''''bold and italic''''' text.\n"
        result = "<body>\n<p>Here, we have <em><strong>bold and italic</strong></em> text.</p>\n</body>"
        self.parsed_equal_string(source, result, None, {}, 'html')

    def test_bold_italic_case2(self):
        source = "Here, we have ''italic only and '''bold and italic''''' text.\n"
        result = "<body>\n<p>Here, we have <em>italic only and <strong>bold and italic</strong></em> text.</p>\n</body>"
        self.parsed_equal_string(source, result, None, {}, 'html')

    def test_bold_italic_case3(self):
        source = "Here, we have '''bold only and ''bold and italic''''' text.\n"
        result = "<body>\n<p>Here, we have <strong>bold only and <em>bold and italic</em></strong> text.</p>\n</body>"
        self.parsed_equal_string(source, result, None, {}, 'html')

    def test_bold_italic_case4(self):
        source = "Here, we have '''''bold and italic''' and italic only''.\n"
        result = "<body>\n<p>Here, we have <em><strong>bold and italic</strong> and italic only</em>.</p>\n</body>"
        self.parsed_equal_string(source, result, None, {}, 'html')

    def test_bold_italic_case5(self):
        source = "Here, we have '''''bold and italic'' and bold only'''.\n"
        result = "<body>\n<p>Here, we have <strong><em>bold and italic</em> and bold only</strong>.</p>\n</body>"
        self.parsed_equal_string(source, result, None, {}, 'html')

    def test_bold_italic_case6(self):
        source = "Here, we have ''italic, '''bold and italic''' and italic only''.\n"
        result = "<body>\n<p>Here, we have <em>italic, <strong>bold and italic</strong> and italic only</em>.</p>\n</body>"
        self.parsed_equal_string(source, result, None, {}, 'html')

    def test_bold_italic_case7(self):
        source = "Here, we have '''bold, ''bold and italic'' and bold only'''.\n"
        result = "<body>\n<p>Here, we have <strong>bold, <em>bold and italic</em> and bold only</strong>.</p>\n</body>"
        self.parsed_equal_string(source, result, None, {}, 'html')

    def test_bold_italic_case8(self):
        source = """'''Le gras :'''

et l'''italique''...
"""
        result = "<body>\n<p><strong>Le gras :</strong></p>\n<p>et l'<em>italique</em>...</p>\n</body>"
        self.parsed_equal_string(source, result, None, {}, 'html')

    def test_italic_template(self):
        source = "Here, we have ''italic {{template}}!''.\n"
        result = "<body>\n<p>Here, we have <em>italic text!</em>.</p>\n</body>"
        templates = {'template': 'text'}
        self.parsed_equal_string(source, result, None, templates, 'html')

    def test_styles_in_template(self):
        source = "Here, we have {{template}}.\n"
        result = "<body>\n<p>Here, we have <strong>text</strong> and <em>more text</em> and <em><strong>still more text</strong></em>.</p>\n</body>"
        templates = {'template': "'''text''' and ''more text'' and '''''still more text'''''"}
        self.parsed_equal_string(source, result, None, templates, 'html')

    def test_simple_bullet_list(self):
        source = """* item 1
** item 2
*** item 3
** item 2
"""
        result = """<body>
<ul>
\t<li> item 1<ul>
\t<li> item 2<ul>
\t<li> item 3</li>
</ul>
</li>
\t<li> item 2</li>
</ul>
</li>
</ul>
</body>"""
        self.parsed_equal_string(source, result, None, {}, 'html')

    def test_simple_numbered_list(self):
        source = """## item 2
### item 3
## item 2
### item 3
"""
        result = """<body>
<ol>
\t<li><ol>
\t<li> item 2</li>
</ol>
</li>
\t<li><ol>
\t<li><ol>
\t<li> item 3</li>
</ol>
</li>
</ol>
</li>
\t<li><ol>
\t<li> item 2</li>
</ol>
</li>
\t<li><ol>
\t<li><ol>
\t<li> item 3</li>
</ol>
</li>
</ol>
</li>
</ol>
</body>"""
        self.parsed_equal_string(source, result, None, {}, 'html')

    def test_simple_semicolon_list(self):
        source = """; item 1
;; item 2
;; item 2
; item 1
; item 1
;;; item 3
"""
        result = """<body>
<dl>
\t<dt> item 1<dl>
\t<dt> item 2</dt>
\t<dt> item 2</dt>
</dl>
</dt>
\t<dt> item 1</dt>
\t<dt> item 1<dl>
\t<dt><dl>
\t<dt> item 3</dt>
</dl>
</dt>
</dl>
</dt>
</dl>
</body>"""
        self.parsed_equal_string(source, result, None, {}, 'html')

    def test_simple_colon_list(self):
        source = """: item 1
::: item 3
:: item 2
: item 1
:: item 2
:: item 2
"""
        result = """<body>
<dl>
\t<dd> item 1<dl>
\t<dd><dl>
\t<dd> item 3</dd>
</dl>
</dd>
\t<dd> item 2</dd>
</dl>
</dd>
\t<dd> item 1<dl>
\t<dd> item 2</dd>
\t<dd> item 2</dd>
</dl>
</dd>
</dl>
</body>"""
        self.parsed_equal_string(source, result, None, {}, 'html')

    def test_formatted_mixed_list(self):
        source = """: item 1
; this is ''italic''
* and '''bold''' here
# a [[link]]
: a {{template}}
"""
        result = """<body>
<dl>
\t<dd> item 1</dd>
</dl>
<dl>
\t<dt> this is <em>italic</em></dt>
</dl>
<ul>
\t<li> and <strong>bold</strong> here</li>
</ul>
<ol>
\t<li> a link</li>
</ol>
<dl>
\t<dd> a template!</dd>
</dl>
</body>"""
        templates = {'template': 'template!'}
        self.parsed_equal_string(source, result, None, templates, 'html')

    def test_complex_mixed_list(self):
        source = """*level 1
*level 1
**level 2
**#level 3
**level 2
:: level 2
; level 1
##level 2
##;level 3
####level 4
#**#level 4
:*;#*: weird syntax
* end
"""
        result = """<body>
<ul>
\t<li>level 1</li>
\t<li>level 1<ul>
\t<li>level 2<ol>
\t<li>level 3</li>
</ol>
</li>
\t<li>level 2</li>
</ul>
</li>
\t<li><dl>
\t<dd> level 2</dd>
</dl>
</li>
</ul>
<dl>
\t<dt> level 1</dt>
\t<dt><ol>
\t<li>level 2</li>
</ol>
</dt>
\t<dt><ol>
\t<li><dl>
\t<dt>level 3</dt>
</dl>
</li>
</ol>
</dt>
\t<dt><ol>
\t<li><ol>
\t<li><ol>
\t<li>level 4</li>
</ol>
</li>
</ol>
</li>
</ol>
</dt>
\t<dt><ul>
\t<li><ul>
\t<li><ol>
\t<li>level 4</li>
</ol>
</li>
</ul>
</li>
</ul>
</dt>
\t<dt><ul>
\t<li><dl>
\t<dt><ol>
\t<li><ul>
\t<li><dl>
\t<dd> weird syntax</dd>
</dl>
</li>
</ul>
</li>
</ol>
</dt>
</dl>
</li>
</ul>
</dt>
</dl>
<ul>
\t<li> end</li>
</ul>
</body>"""
        self.parsed_equal_string(source, result, None, {}, 'html')

    def test_tag_balancing_in_title6(self):
        """Close open tags"""
        source = '======<b>Test!======\n'
        result = "<h6><b>Test!</b></h6>\n"
        self.parsed_equal_string(source, result, 'wikitext', {}, 'html')

    def test_tag_balancing_in_title2(self):
        """Ignore close tags for non-open tags"""
        source = '==Test!</i>==\n'
        result = "<h2>Test!</h2>\n"
        self.parsed_equal_string(source, result, 'wikitext', {}, 'html')

    def test_convert_autoclose_tags(self):
        """Ignore close tags for non-open tags"""
        source = 'convert this: <br></br><br/> and <hr>this </hr> too <hr/>!\n'
        result = '<p>convert this: <br /><br /><br /> and <hr />this <hr /> too <hr />!</p>\n'
        self.parsed_equal_string(source, result, 'wikitext', {}, 'html')

    def test_tag_balancing_in_mixed_structures(self):
        """Ignore close tags for non-open tags"""
        source = """==<b>Test!</i>==
* test <i>test</b>
A paragraph with a </hr> tag and a <span style="color:blue">span.

a {{template}}</b>.

Note: an <span>open tag can be closed {{in a template}}
"""
        result = """<body>
<h2><b>Test!</b></h2>
<ul>
\t<li> test <i>test</i></li>
</ul>
<p>A paragraph with a <hr /> tag and a <span style="color:blue">span.</span></p>
<p>a text<i>text.</i></p>
<p>Note: an <span>open tag can be closed like </span> this!</p>
</body>"""
        templates = {'template': 'text<i>text',
                     'in a template': 'like </span> this!'}
        self.parsed_equal_string(source, result, None, templates, 'html')

    def test_inline_url(self):
        source = 'text http://www.mozilla.org text\n'
        result = '<p>text <a href="http://www.mozilla.org">http://www.mozilla.org</a> text</p>\n'
        self.parsed_equal_string(source, result, 'wikitext', {}, 'html')

    def test_external_links(self):
        source = "text [http://www.mozilla.org], [http://www.github.com] and [http://fr.wikipedia.org ''French'' Wikipedia] text\n"
        result = '<body>\n<p>text <a href="http://www.mozilla.org">[1]</a>, <a href="http://www.github.com">[2]</a> and <a href="http://fr.wikipedia.org"><em>French</em> Wikipedia</a> text</p>\n</body>'
        self.parsed_equal_string(source, result, None, {}, 'html')
