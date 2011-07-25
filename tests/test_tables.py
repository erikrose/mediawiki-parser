# -*- coding: utf8 -*-

from mediawiki_parser.tests import ParserTestCase


class TablesTests(ParserTestCase):
    def test_table_first_cell(self):
        source = 'style="color:red" | cell 1'
        result = """table_first_cell:
   table_parameter:
      HTML_attribute:
         attribute_name:style
         value_quote:color:red
   table_cell_content:
      @clean_inline@:
         raw_text: cell 1"""
        self.parsed_equal_tree(source, result, 'table_first_cell')

    def test_table_other_cell(self):
        source = '|| cell 1'
        result = "[@clean_inline@:[raw_text:' cell 1']]"
        self.parsed_equal_string(source, result, 'table_other_cell')

    def test_table_special_line(self):
        source = '|-\n'
        result = ""
        self.parsed_equal_string(source, result, 'table_special_line')

    def test_table_line_with_css(self):
        source = '| style="color:red" | cell 1\n'
        result = """table_line_cells:
   table_parameter:
      HTML_attribute:
         attribute_name:style
         value_quote:color:red
   table_cell_content:
      @clean_inline@:
         raw_text: cell 1"""
        self.parsed_equal_tree(source, result, 'table_line')

    def test_table_line_with_multiple_attributes(self):
        source = '| style="color:red" id=\'test\' name=test| cell 1\n'
        result = """table_line_cells:
   table_parameter:
      HTML_attribute:
         attribute_name:style
         value_quote:color:red
      HTML_attribute:
         attribute_name:id
         value_apostrophe:test
      HTML_attribute:
         attribute_name:name
         value_noquote:test
   table_cell_content:
      @clean_inline@:
         raw_text: cell 1"""
        self.parsed_equal_tree(source, result, 'table_line')

    def test_table_line_without_css(self):
        source = '| cell 1\n'
        result = "[@clean_inline@:[raw_text:' cell 1']]"
        self.parsed_equal_string(source, result, 'table_line')

    def test_table_line_with_dash(self):
        source = '|data L2-B\n'
        result = "[@clean_inline@:[raw_text:'data L2-B']]"
        self.parsed_equal_string(source, result, 'table_line')

    def test_table_line_with_2_cells(self):
        source = '| cell 1 || cell 2\n'
        result = """table_line_cells:
   table_cell_content:
      @clean_inline@:
         raw_text: cell 1 
   table_cell_content:
      @clean_inline@:
         raw_text: cell 2"""
        self.parsed_equal_tree(source, result, 'table_line')

    def test_table_line_with_HTML_in_1st_cell(self):
        source = '| style="color:red" | cell 1 || cell 2\n'
        result = """table_line_cells:
   table_first_cell:
      table_parameter:
         HTML_attribute:
            attribute_name:style
            value_quote:color:red
      table_cell_content:
         @clean_inline@:
            raw_text: cell 1 
   table_cell_content:
      @clean_inline@:
         raw_text: cell 2"""
        self.parsed_equal_tree(source, result, 'table_line')

    def test_table_line_with_HTML_in_2nd_cell(self):
        source = '| cell 1 || style="color:red" | cell 2\n'
        result = """table_line_cells:
   table_cell_content:
      @clean_inline@:
         raw_text: cell 1 
   table_first_cell:
      table_parameter:
         HTML_attribute:
            attribute_name:style
            value_quote:color:red
      table_cell_content:
         @clean_inline@:
            raw_text: cell 2"""
        self.parsed_equal_tree(source, result, 'table_line')

    def test_table_header_with_css(self):
        source = '! scope=row | Line 1\n'
        result = """table_line_header:
   table_parameter:
      HTML_attribute:
         attribute_name:scope
         value_noquote:row
   table_cell_content:
      @clean_inline@:
         raw_text: Line 1"""
        self.parsed_equal_tree(source, result, 'table_line')

    def test_table_line_with_global_css(self):
        source = '|- style="color:red"\n'
        result = "[table_parameters:[HTML_attribute:[attribute_name:'style'  value_quote:'color:red']]]"
        self.parsed_equal_string(source, result, 'table_line')

    def test_table_with_css(self):
        source = """{|
! cellA
! cellB
|- style="color:red"
| cell C
| cell D
|}
"""
        result = """@table@:
   table_line_header:
      @clean_inline@:
         raw_text: cellA
   table_line_header:
      @clean_inline@:
         raw_text: cellB
   table_line_break:
      table_parameters:
         HTML_attribute:
            attribute_name:style
            value_quote:color:red
   table_line_cells:
      @clean_inline@:
         raw_text: cell C
   table_line_cells:
      @clean_inline@:
         raw_text: cell D"""
        self.parsed_equal_tree(source, result, "table")

    def test_table_with_template(self):
        source = """{|
|+ Table {{title|parameter=yes}}
| cell 1 || cell 2
|-
| cell 3 || cell 4
|}
"""
        result = """@table@:
   table_title:
      @clean_inline@:
         raw_text: Table test: yes
   table_line_cells:
      table_cell_content:
         @clean_inline@:
            raw_text: cell 1 
      table_cell_content:
         @clean_inline@:
            raw_text: cell 2
   table_line_break:
   table_line_cells:
      table_cell_content:
         @clean_inline@:
            raw_text: cell 3 
      table_cell_content:
         @clean_inline@:
            raw_text: cell 4"""
        templates = {'title': 'test: {{{parameter}}}'}
        self.parsed_equal_tree(source, result, "table", templates)

    def test_table_with_HTML_and_template(self):
        source = """{| class="table" {{prettyTable}}
|+ style="color:red" | Table {{title|parameter}}
|-
|
! scope=col | Title A
! scope=col | Title B
|-
! scope=row | Line 1
|data L1.A
|data L1.B
|-
! scope=row | Line 2
|data L2.A
|data {{template|with|parameters=L2.B}}
|}
"""
        result = """@table@:
   table_begin:
      table_parameters:
         HTML_attribute:
            attribute_name:class
            value_quote:table
         HTML_attribute:
            attribute_name:style
            value_quote:color:blue
   table_content:
      table_title:
         table_parameter:
            HTML_attribute:
               attribute_name:style
               value_quote:color:red
         table_cell_content:
            @clean_inline@:
               raw_text: Table test: parameter
      table_line_break:
      table_empty_cell:
      table_line_header:
         table_parameter:
            HTML_attribute:
               attribute_name:scope
               value_noquote:col
         table_cell_content:
            @clean_inline@:
               raw_text: Title A
      table_line_header:
         table_parameter:
            HTML_attribute:
               attribute_name:scope
               value_noquote:col
         table_cell_content:
            @clean_inline@:
               raw_text: Title B
      table_line_break:
      table_line_header:
         table_parameter:
            HTML_attribute:
               attribute_name:scope
               value_noquote:row
         table_cell_content:
            @clean_inline@:
               raw_text: Line 1
      table_line_cells:
         @clean_inline@:
            raw_text:data L1.A
      table_line_cells:
         @clean_inline@:
            raw_text:data L1.B
      table_line_break:
      table_line_header:
         table_parameter:
            HTML_attribute:
               attribute_name:scope
               value_noquote:row
         table_cell_content:
            @clean_inline@:
               raw_text: Line 2
      table_line_cells:
         @clean_inline@:
            raw_text:data L2.A
      table_line_cells:
         @clean_inline@:
            raw_text:data with and L2.B..."""
        templates = {'prettyTable': 'style="color:blue"',
                     'title': 'test: {{{1}}}',
                     'template': '{{{1}}} and {{{parameters}}}...'}
        self.parsed_equal_tree(source, result, "table", templates)

    def test_nested_tables(self):
        source = """{| class="table" {{prettyTable}}
|+ style="color:red" | Table {{title|1=true}}
|-
! scope=col | First (mother)
! scope=col | table
|
{| class="table" {{prettyTable}}
|-
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
        result = """@table@:
   table_begin:
      table_parameters:
         HTML_attribute:
            attribute_name:class
            value_quote:table
         HTML_attribute:
            attribute_name:style
            value_quote:color:blue
   table_content:
      table_title:
         table_parameter:
            HTML_attribute:
               attribute_name:style
               value_quote:color:red
         table_cell_content:
            @clean_inline@:
               raw_text: Table test: true
      table_line_break:
      table_line_header:
         table_parameter:
            HTML_attribute:
               attribute_name:scope
               value_noquote:col
         table_cell_content:
            @clean_inline@:
               raw_text: First (mother)
      table_line_header:
         table_parameter:
            HTML_attribute:
               attribute_name:scope
               value_noquote:col
         table_cell_content:
            @clean_inline@:
               raw_text: table
      table_empty_cell:
      @table@:
         table_begin:
            table_parameters:
               HTML_attribute:
                  attribute_name:class
                  value_quote:table
               HTML_attribute:
                  attribute_name:style
                  value_quote:color:blue
         table_content:
            table_line_break:
            table_line_header:
               table_parameter:
                  HTML_attribute:
                     attribute_name:scope
                     value_noquote:row
               table_cell_content:
                  @clean_inline@:
                     raw_text: Second (daughter) table
            table_line_cells:
               @clean_inline@:
                  raw_text:data L1.A
            table_line_cells:
               @clean_inline@:
                  raw_text:data L1.B
            table_line_break:
            table_line_header:
               table_parameter:
                  HTML_attribute:
                     attribute_name:scope
                     value_noquote:row
               table_cell_content:
                  @clean_inline@:
                     raw_text: in the first one
            table_line_cells:
               @clean_inline@:
                  raw_text:data L2.A
            table_line_cells:
               @clean_inline@:
                  raw_text:data L2.B
      table_line_break:
      table_line_cells:
         @clean_inline@:
            raw_text: first
      table_line_cells:
         @clean_inline@:
            raw_text: table
      table_line_cells:
         @clean_inline@:
            raw_text: again"""
        templates = {'prettyTable': 'style="color:blue"',
                     'title': 'test: {{{1}}}'}
        self.parsed_equal_tree(source, result, "table", templates)
