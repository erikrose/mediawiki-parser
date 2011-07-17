# -*- coding: utf8 -*-

from mediawiki_parser.tests import ParserTestCase


class LinksTests(ParserTestCase):
    def test_simple_internal_link(self):
        source = '[[article]]'
        result = "[internal_link:'article']"
        self.parsed_equal_string(source, result, 'inline')

    def test_advanced_internal_link(self):
        source = '[[article|alternate]]'
        result = "[internal_link:[page_name:'article'  link_arguments:[link_argument:[rawText:'alternate']]]]"
        self.parsed_equal_string(source, result, 'inline')

    def test_special_chars_in_internal_link(self):
        source = '[[article|}}]]'
        result = "[internal_link:[page_name:'article'  link_arguments:[link_argument:'}}']]]"
        self.parsed_equal_string(source, result, 'inline')

    def test_template_in_internal_link(self):
        source = "[[article|{{template|value=pass}}]]"
        result = "[internal_link:[page_name:'article'  link_arguments:[link_argument:[rawText:'test: pass']]]]"
        templates = {'template': 'test: {{{value}}}'}
        self.parsed_equal_string(source, result, 'inline', templates)

    def test_category(self):
        source = '[[Category:Category name|sort key]]'
        result = "[internal_link:[page_name:'Category:Category name'  link_arguments:[link_argument:[rawText:'sort key']]]]"
        self.parsed_equal_string(source, result, 'inline')

    def test_link_to_category(self):
        source = '[[:Category:MyCategory|mycategory]]'
        result = "[internal_link:[page_name:':Category:MyCategory'  link_arguments:[link_argument:[rawText:'mycategory']]]]"
        self.parsed_equal_string(source, result, 'inline')

    def test_category_foreign_language(self):
        source = u'[[Catégorie:Nom de catégorie]]'
        result = u"[internal_link:'Catégorie:Nom de catégorie']"
        self.parsed_equal_string(source, result, 'inline')

    def test_image(self):
        source = '[[File:Filename.png]]'
        result = "[internal_link:'File:Filename.png']"
        self.parsed_equal_string(source, result, 'inline')

    def test_image_with_parameter(self):
        source = '[[File:File name.JPG|25px]]'
        result = "[internal_link:[page_name:'File:File name.JPG'  link_arguments:[link_argument:[rawText:'25px']]]]"
        self.parsed_equal_string(source, result, 'inline')

    def test_image_with_parameters(self):
        source = '[[Category:Category name|thumb|300px|left|Legend|alt=Image description]]'
        result = "[internal_link:[page_name:'Category:Category name'  link_arguments:[link_argument:[rawText:'thumb']  link_argument:[rawText:'300px']  link_argument:[rawText:'left']  link_argument:[rawText:'Legend']  link_argument:[rawText:'alt=Image description']]]]"
        self.parsed_equal_string(source, result, 'inline')

    def test_inline_url(self):
        source = 'An URL: http://www.mozilla.org'
        result = "[rawText:'An URL: '  url:'http://www.mozilla.org']"
        self.parsed_equal_string(source, result, 'inline')

    def test_external_link(self):
        source = "[http://www.mozilla.org]"
        result = "[external_link:[url:'http://www.mozilla.org']]"
        self.parsed_equal_string(source, result, 'inline')

    def test_formatted_text_in_external_link(self):
        source = "[http://www.mozilla.org this is an ''external'' link]"
        result = "[external_link:[url:'http://www.mozilla.org'  optional_link_text:[rawText:'this is an <em>external</em> link']]]"
        self.parsed_equal_string(source, result, 'inline')

    def test_spacetabs_in_external_link(self):
        source = '[http://www.mozilla.org         some text]'
        result = "[external_link:[url:'http://www.mozilla.org'  optional_link_text:[rawText:'some text']]]"
        self.parsed_equal_string(source, result, 'inline')

    def test_html_external_link(self):
        # By default, HTML links are not allowed
        source = '<a href="http://www.mozilla.org">this is an \'\'external\'\' link</a>'
        result = "[tag_open:[tag_name:'a'  optional_attributes:[optional_attribute:[attribute_name:'href'  value_quote:'http://www.mozilla.org']]]  rawText:'this is an <em>external</em> link'  tag_close:[tag_name:'a']]"
        self.parsed_equal_string(source, result, 'inline')
