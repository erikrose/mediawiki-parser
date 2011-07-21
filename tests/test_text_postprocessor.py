# -*- coding: utf8 -*-

from mediawiki_parser.tests import PostprocessorTestCase


class TextBackendTests(PostprocessorTestCase):
    def test_simple_title2(self):
        source = '== A title ==\n'
        result = ' A title \n'
        self.parsed_equal_string(source, result, 'wikitext', {}, 'text')

    def test_simple_title6(self):
        source = '====== Test! ======\n'
        result = ' Test! \n'
        self.parsed_equal_string(source, result, 'wikitext', {}, 'text')

    def test_simple_allowed_open_tag(self):
        source = 'a<p>test'
        result = 'a\ntest'
        self.parsed_equal_string(source, result, 'inline', {}, 'text')

    def test_complex_allowed_open_tag(self):
        """ The attributes are ignored. """
        source = 'a<p class="wikitext" style="color:red" onclick="javascript:alert()">test'
        result = 'a\ntest'
        self.parsed_equal_string(source, result, 'inline', {}, 'text')

    def test_simple_disallowed_open_tag(self):
        source = '<a>'
        result = '<a>'
        self.parsed_equal_string(source, result, 'inline', {}, 'text')

    def test_complex_disallowed_open_tag(self):
        source = '<a href="test" class="test" style="color:red" anything="anything">'
        result = '<a href="test" class="test" style="color:red" anything="anything">'
        self.parsed_equal_string(source, result, 'inline', {}, 'text')

    def test_simple_allowed_autoclose_tag(self):
        source = 'a<br />test'
        result = 'a\ntest'
        self.parsed_equal_string(source, result, 'inline', {}, 'text')

    def test_complex_allowed_autoclose_tag(self):
        source = 'one more <br name="test" /> test'
        result = 'one more \n test'
        self.parsed_equal_string(source, result, 'inline', {}, 'text')

    def test_simple_disallowed_autoclose_tag(self):
        source = '<test />'
        result = '<test />'
        self.parsed_equal_string(source, result, 'inline', {}, 'text')

    def test_complex_disallowed_autoclose_tag(self):
        source = '<img src="file.png" />'
        result = '<img src="file.png" />'
        self.parsed_equal_string(source, result, 'inline', {}, 'text')
