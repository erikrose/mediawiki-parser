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
