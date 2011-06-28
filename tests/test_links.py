# -*- coding: utf8 -*-

from mediawiki_parser.tests import ParserTestCase


class Links_tests(ParserTestCase):
    def test_simple_internal_link(self):
        source = '[[article]]'
        result = "[internal_link:'article']"
        self.parsed_equal_string(source, result, 'inline')

    def test_advanced_internal_link(self):
        source = '[[article|alternate]]'
        result = "[internal_link:[page_name:'article'  link_arguments:[link_argument:[link_text:[rawText:'alternate']]]]]"
        self.parsed_equal_string(source, result, 'inline')

    def test_special_chars_in_internal_link(self):
        source = '[[article|}}]]'
        result = "[internal_link:[page_name:'article'  link_arguments:[link_argument:[link_text:'}}']]]]"
        self.parsed_equal_string(source, result, 'inline')

    def test_template_in_internal_link(self):
        source = '[[article|{{template|value=1}}]]'
        result = "[internal_link:[page_name:'article'  link_arguments:[link_argument:[link_text:[template:[page_name:'template'  parameters:[parameter:[parameter_name:'value'  optional_value:[rawText:'1']]]]]]]]]"
        self.parsed_equal_string(source, result, 'inline')

    def test_url(self):
        source = 'An URL: http://www.mozilla.org'
        result = "[rawText:'An URL: '  url:'http://www.mozilla.org']"
        self.parsed_equal_string(source, result, 'inline')

    def test_external_link(self):
        source = "[http://www.mozilla.org]"
        result = "[external_link:[url:'http://www.mozilla.org']]"
        self.parsed_equal_string(source, result, 'inline')

    def test_formatted_text_in_link(self):
        source = "[http://www.mozilla.org this is an ''external'' link]"
        result = "[external_link:[url:'http://www.mozilla.org'  optional_link_text:[rawText:'this is an <em>external</em> link']]]"
        self.parsed_equal_string(source, result, 'inline')

    def test_spacetabs_in_link(self):
        source = '[http://www.mozilla.org         some text]'
        result = "[external_link:[url:'http://www.mozilla.org'  optional_link_text:[rawText:'some text']]]"
        self.parsed_equal_string(source, result, 'inline')

    def test_formatted_external_link(self):
        # By default, HTML links are not allowed
        source = '<a href="http://www.mozilla.org">this is an \'\'external\'\' link</a>'
        result = "[tag_open:[tag_name:'a'  optional_attributes:[optional_attribute:[attribute_name:'href'  value_quote:'http://www.mozilla.org']]]  rawText:'this is an <em>external</em> link'  tag_close:[tag_name:'a']]"
        self.parsed_equal_string(source, result, 'inline')
