# -*- coding: utf8 -*-

from mediawiki_parser.tests import ParserTestCase


class SpecialCharsTests(ParserTestCase):
    def test_tabs_in_text(self):
        source = "Some\ttext and\t\ttabs."
        result = "[raw_text:'Some'  tab_to_space:' '  raw_text:'text and'  tab_to_space:' '  raw_text:'tabs.']"
        self.parsed_equal_string(source, result, 'inline')

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
        result = "[raw_text:'This '  LT:'<'  raw_text:' should pass.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_gt(self):
        source = 'This > should pass.'
        result = "[raw_text:'This '  GT:'>'  raw_text:' should pass.']"
        self.parsed_equal_string(source, result, 'inline')

    def test_lt_gt(self):
        "Entities corresponding to < and > should be left untouched"
        source = 'This is a tag: <p> but &lt;p&gt; and &#60;p&#62; are not tags.'
        result = "[raw_text:'This is a tag: '  tag_open:[tag_name:'p']  raw_text:' but '  entity:'<'  raw_text:'p'  entity:'>'  raw_text:' and '  allowed_char:'&'  raw_text:'#60'  allowed_char:';'  raw_text:'p'  allowed_char:'&'  raw_text:'#62'  allowed_char:';'  raw_text:' are not tags.']"
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
        result = "[raw_text:'This should be a '  internal_link:[page_name:'link']  raw_text:' and '  allowed_char:'['  allowed_char:'['  raw_text:'plain text']"
        self.parsed_equal_string(source, result, 'inline')

    def test_valid_named_entities(self):
        source = '&Alpha;&beta;&gamma; &diams;'
        result = u"[raw_text:'Αβγ ♦']"
        self.parsed_equal_string(source, result, 'inline')

    def test_valid_numbered_entities(self):
        source = '&#169;&#8212; &#9830;'
        result = u"[raw_text:'©— ♦']"
        self.parsed_equal_string(source, result, 'inline')

    def test_invalid_named_entities(self):
        source = '&abcd;&1234; &apos;'
        result = "[entity:'&abcd;'  entity:'&1234;'  raw_text:' '  entity:'&apos;']"
        self.parsed_equal_string(source, result, 'inline')

    def test_invalid_numbered_entities(self):
        source = '&#12252524534; &#04359435;'
        result = "[allowed_char:'&'  raw_text:'#12252524534'  allowed_char:';'  raw_text:' '  allowed_char:'&'  raw_text:'#4359435'  allowed_char:';']"
        self.parsed_equal_string(source, result, 'inline')

    def test_valid_entities_in_links(self):
        source = 'a [[test&copy;test]] and two other: [[&diams;]] [[&#8212;]]'
        result = u"[raw_text:'a '  internal_link:[page_name:'test©test']  raw_text:' and two other: '  internal_link:[page_name:'♦']  raw_text:' '  internal_link:[page_name:'—']]"
        self.parsed_equal_string(source, result, 'inline')

    def test_invalid_entities_in_links(self):
        source = 'a [[test&abcd;test]] and two other: [[&efgh;]] [[&#8282828212;]]'
        result = "[raw_text:'a '  allowed_char:'['  allowed_char:'['  raw_text:'test'  entity:'&abcd;'  raw_text:'test'  allowed_char:']'  allowed_char:']'  raw_text:' and two other: '  allowed_char:'['  allowed_char:'['  entity:'&efgh;'  allowed_char:']'  allowed_char:']'  raw_text:' '  allowed_char:'['  allowed_char:'['  allowed_char:'&'  raw_text:'#8282828212'  allowed_char:';'  allowed_char:']'  allowed_char:']']"
        self.parsed_equal_string(source, result, 'inline')

    def test_valid_entities_in_template_calls(self):
        source = 'a {{test&copy;test}} and another: {{&diams;}}'
        result = u"[raw_text:'a '  internal_link:[page_name:'Template:test©test']  raw_text:' and another: '  internal_link:page_name['Template:♦']]"
        #self.parsed_equal_string(source, result, 'inline')
        import nose
        raise nose.SkipTest

    def test_invalid_entities_in_template_calls(self):
        source = 'a {{test&abcd;test}} and another: {{&efgh;}}'
        result = "[raw_text:'a '  allowed_char:'{'  allowed_char:'{'  raw_text:'test'  entity:'&abcd;'  raw_text:'test'  allowed_char:'}'  allowed_char:'}'  raw_text:' and another: '  allowed_char:'{'  allowed_char:'{'  entity:'&efgh;'  allowed_char:'}'  allowed_char:'}']"
        self.parsed_equal_string(source, result, 'inline')
