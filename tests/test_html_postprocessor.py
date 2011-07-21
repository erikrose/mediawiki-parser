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
