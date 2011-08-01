# -*- coding: utf8 -*-

from mediawiki_parser.tests import ParserTestCase


class TitlesTests(ParserTestCase):
    def test_title1(self):
        source = '=Title 1=\n'
        result = "[title1:[raw_text:'Title 1']]"
        self.parsed_equal_string(source, result, None)

    def test_title2(self):
        source = '== Title 2 ==\n'
        result = "[title2:[raw_text:' Title 2 ']]"
        self.parsed_equal_string(source, result, None)

    def test_title3_extra_spacetab(self):
        # Ignore extra spaces and tabs
        source = '===Title 3===                    \n'
        result = "[title3:[raw_text:'Title 3']]"
        self.parsed_equal_string(source, result, None)

    def test_title4(self):
        source = '==== Title 4 ====\n'
        result = "[title4:[raw_text:' Title 4 ']]"
        self.parsed_equal_string(source, result, None)

    def test_title5(self):
        source = '===== Title 5 =====\n'
        result = "[title5:[raw_text:' Title 5 ']]"
        self.parsed_equal_string(source, result, None)

    def test_title6(self):
        source = '====== Title 6 ======\n'
        result = "[title6:[raw_text:' Title 6 ']]"
        self.parsed_equal_string(source, result, None)

    def test_title7(self):
        # Max level is 6; keep extra equals
        source = '======= Title 6 =======\n'
        result = "[title6:[raw_text:'= Title 6 =']]"
        self.parsed_equal_string(source, result, None)

    def test_link_in_title(self):
        source = '= [[a link]] =\n'
        result = "[title1:[raw_text:' '  internal_link:[page_name:'a link']  raw_text:' ']]"
        self.parsed_equal_string(source, result, None)

    def test_italic_in_title(self):
        source = "== ''italic text'' ==\n"
        result = "[title2:[raw_text:' \'\'italic text\'\' ']]"
        self.parsed_equal_string(source, result, None)

    def test_bold_in_title(self):
        source = "=== '''bold text''' ===\n"
        result = "[title3:[raw_text:' \'\'\'bold text\'\'\' ']]"
        self.parsed_equal_string(source, result, None)

    def test_formatted_link_in_title(self):
        source = "==== [[Title 4|formatted link]] ====\n"
        result = "[title4:[raw_text:' '  internal_link:[page_name:'Title 4'  link_arguments:[link_argument:[raw_text:'formatted link']]]  raw_text:' ']]"
        self.parsed_equal_string(source, result, None)

    def test_simple_template_in_title(self):
        source = '===== {{Title 5}} =====\n'
        result = "[title5:[raw_text:' '  internal_link:[page_name:'Template:Title 5']  raw_text:' ']]"
        self.parsed_equal_string(source, result, None)

    def test_braces_in_title(self):
        source = '====== { Title 6} ======\n'
        result = "[title6:[raw_text:' '  allowed_char:'{'  raw_text:' Title 6'  allowed_char:'}'  raw_text:' ']]"
        self.parsed_equal_string(source, result, None)

    def test_equal_in_title(self):
        source = '== Title = title ==\n'
        result = "[title2:[raw_text:' Title = title ']]"
        self.parsed_equal_string(source, result, None)

    def test_more_equal_in_title(self):
        source = '== Title == title ==\n'
        result = "[title2:[raw_text:' Title == title ']]"
        self.parsed_equal_string(source, result, None)
