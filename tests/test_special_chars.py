# -*- coding: utf8 -*-

from mediawiki_parser.tests import ParserTestCase


class SpecialCharsTests(ParserTestCase):
    def test_unicode_chars(self):
        source = u"Some Unicode characters: 你好."
        result = u"[rawText:'Some Unicode characters: 你好.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_hash(self):
        source = 'This # should pass.'
        result = "[rawText:'This # should pass.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_l_brace(self):
        source = 'This { should pass.'
        result = "[rawText:'This '  allowedChar:'{'  rawText:' should pass.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_r_brace(self):
        source = 'This } should pass.'
        result = "[rawText:'This '  allowedChar:'}'  rawText:' should pass.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_double_l_brace(self):
        source = 'This {{ should pass.'
        result = "[rawText:'This '  allowedChar:'{'  allowedChar:'{'  rawText:' should pass.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_double_r_brace(self):
        source = 'This }} should pass.'
        result = "[rawText:'This '  allowedChar:'}'  allowedChar:'}'  rawText:' should pass.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_lt(self):
        source = 'This < should pass.'
        result = "[rawText:'This '  allowedChar:'<'  rawText:' should pass.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_gt(self):
        source = 'This > should pass.'
        result = "[rawText:'This '  allowedChar:'>'  rawText:' should pass.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_l_bracket(self):
        source = 'This [ should pass.'
        result = "[rawText:'This '  allowedChar:'['  rawText:' should pass.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_double_l_bracket(self):
        source = 'This [[ should pass.'
        result = "[rawText:'This '  allowedChar:'['  allowedChar:'['  rawText:' should pass.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_r_bracket(self):
        source = 'This ] should pass.'
        result = "[rawText:'This '  allowedChar:']'  rawText:' should pass.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_double_r_bracket(self):
        source = 'This ]] should pass.'
        result = "[rawText:'This '  allowedChar:']'  allowedChar:']'  rawText:' should pass.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_pipe(self):
        source = 'This | should pass.'
        result = "[rawText:'This '  allowedChar:'|'  rawText:' should pass.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_equal(self):
        source = 'This = should pass.'
        result = "[rawText:'This = should pass.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_colon(self):
        source = 'This: should pass.'
        result = "[rawText:'This: should pass.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_semicolon(self):
        source = 'This; should pass.'
        result = "[rawText:'This'  allowedChar:';'  rawText:' should pass.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_quotes(self):
        source = 'This "should" pass.'
        result = "[rawText:'This \"should\" pass.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_dash(self):
        source = 'This - should pass.'
        result = "[rawText:'This - should pass.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_double_r_bracket_with_link(self):
        source = 'This should be a [[link]] and [[plain text'
        result = "[rawText:'This should be a '  internal_link:'link'  rawText:' and '  allowedChar:'['  allowedChar:'['  rawText:'plain text']"
        self.parsed_equal_string(source, result, 'inline')
