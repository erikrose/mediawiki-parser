# -*- coding: utf8 -*-

from mediawiki_parser.tests import ParserTestCase


class SpecialCharsTests(ParserTestCase):
    def test_unicode_chars(self):
        source = u"Some Unicode characters: 你好."
        result = u"[raw_text:'Some Unicode characters: 你好.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_unicode_chars_in_links(self):
        source = u"[[你好|你好]]"
        result = u"[internal_link:[page_name:'你好'  link_arguments:[link_argument:[raw_text:'你好']]]]"
        self.parsed_equal_string(source, result, 'inline')

    def test_hash(self):
        source = 'This # should pass.'
        result = "[raw_text:'This # should pass.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_l_brace(self):
        source = 'This { should pass.'
        result = "[raw_text:'This '  allowed_char:'{'  raw_text:' should pass.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_r_brace(self):
        source = 'This } should pass.'
        result = "[raw_text:'This '  allowed_char:'}'  raw_text:' should pass.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_double_l_brace(self):
        source = 'This {{ should pass.'
        result = "[raw_text:'This '  allowed_char:'{'  allowed_char:'{'  raw_text:' should pass.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_double_r_brace(self):
        source = 'This }} should pass.'
        result = "[raw_text:'This '  allowed_char:'}'  allowed_char:'}'  raw_text:' should pass.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_lt(self):
        source = 'This < should pass.'
        result = "[raw_text:'This '  allowed_char:'<'  raw_text:' should pass.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_gt(self):
        source = 'This > should pass.'
        result = "[raw_text:'This '  allowed_char:'>'  raw_text:' should pass.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_l_bracket(self):
        source = 'This [ should pass.'
        result = "[raw_text:'This '  allowed_char:'['  raw_text:' should pass.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_double_l_bracket(self):
        source = 'This [[ should pass.'
        result = "[raw_text:'This '  allowed_char:'['  allowed_char:'['  raw_text:' should pass.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_r_bracket(self):
        source = 'This ] should pass.'
        result = "[raw_text:'This '  allowed_char:']'  raw_text:' should pass.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_double_r_bracket(self):
        source = 'This ]] should pass.'
        result = "[raw_text:'This '  allowed_char:']'  allowed_char:']'  raw_text:' should pass.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_pipe(self):
        source = 'This | should pass.'
        result = "[raw_text:'This '  allowed_char:'|'  raw_text:' should pass.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_equal(self):
        source = 'This = should pass.'
        result = "[raw_text:'This = should pass.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_colon(self):
        source = 'This: should pass.'
        result = "[raw_text:'This: should pass.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_semicolon(self):
        source = 'This; should pass.'
        result = "[raw_text:'This'  allowed_char:';'  raw_text:' should pass.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_quotes(self):
        source = 'This "should" pass.'
        result = "[raw_text:'This \"should\" pass.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_dash(self):
        source = 'This - should pass.'
        result = "[raw_text:'This - should pass.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_double_r_bracket_with_link(self):
        source = 'This should be a [[link]] and [[plain text'
        result = "[raw_text:'This should be a '  internal_link:'link'  raw_text:' and '  allowed_char:'['  allowed_char:'['  raw_text:'plain text']"
        self.parsed_equal_string(source, result, 'inline')

    def test_valid_entities(self):
        source = '&Alpha;&beta;&gamma; &diams;'
        result = u"[raw_text:'Αβγ ♦']"
        self.parsed_equal_string(source, result, 'inline')

    def test_invalid_entities(self):
        source = '&abcd;&1234; &apos;'
        result = "[entity:'&abcd;'  entity:'&1234;'  raw_text:' '  entity:'&apos;']"
        self.parsed_equal_string(source, result, 'inline')

    def test_valid_entities_in_links(self):
        source = 'a [[test&copy;test]] and another: [[&diams;]]'
        result = u"[raw_text:'a '  internal_link:'test©test'  raw_text:' and another: '  internal_link:'♦']"
        self.parsed_equal_string(source, result, 'inline')

    def test_invalid_entities_in_links(self):
        source = 'a [[test&abcd;test]] and another: [[&efgh;]]'
        result = "[raw_text:'a '  allowed_char:'['  allowed_char:'['  raw_text:'test'  entity:'&abcd;'  raw_text:'test'  allowed_char:']'  allowed_char:']'  raw_text:' and another: '  allowed_char:'['  allowed_char:'['  entity:'&efgh;'  allowed_char:']'  allowed_char:']']"
        self.parsed_equal_string(source, result, 'inline')

    def test_valid_entities_in_template_calls(self):
        source = 'a {{test&copy;test}} and another: {{&diams;}}'
        result = u"[raw_text:'a '  internal_link:'Template:test©test'  raw_text:' and another: '  internal_link:'Template:♦']"
        self.parsed_equal_string(source, result, 'inline')

    def test_invalid_entities_in_template_calls(self):
        source = 'a {{test&abcd;test}} and another: {{&efgh;}}'
        result = "[raw_text:'a '  allowed_char:'{'  allowed_char:'{'  raw_text:'test'  entity:'&abcd;'  raw_text:'test'  allowed_char:'}'  allowed_char:'}'  raw_text:' and another: '  allowed_char:'{'  allowed_char:'{'  entity:'&efgh;'  allowed_char:'}'  allowed_char:'}']"
        self.parsed_equal_string(source, result, 'inline')
