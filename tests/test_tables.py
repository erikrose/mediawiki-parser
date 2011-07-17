# -*- coding: utf8 -*-

from mediawiki_parser.tests import ParserTestCase


class TablesTests(ParserTestCase):
    def test_table_first_cell(self):
        source = 'style="color:red" | cell 1'
        result = """wikiTableFirstCell:
   wikiTableParameter:
      HTML_attribute:
         HTML_name:style
         HTML_value_quote:color:red
   wikiTableCellContent:
      @cleanInline@:
         rawText: cell 1"""
        self.parsed_equal_tree(source, result, 'wikiTableFirstCell')

    def test_table_other_cell(self):
        source = '|| cell 1'
        result = "[@cleanInline@:[rawText:' cell 1']]"
        self.parsed_equal_string(source, result, 'wikiTableOtherCell')

    def test_table_special_line(self):
        source = '|-\n'
        result = ""
        self.parsed_equal_string(source, result, 'wikiTableSpecialLine')

    def test_table_line_with_css(self):
        source = '| style="color:red" | cell 1\n'
        result = """wikiTableLineCells:
   wikiTableParameter:
      HTML_attribute:
         HTML_name:style
         HTML_value_quote:color:red
   wikiTableCellContent:
      @cleanInline@:
         rawText: cell 1"""
        self.parsed_equal_tree(source, result, 'wikiTableLine')

    def test_table_line_with_multiple_attributes(self):
        source = '| style="color:red" id=\'test\' name=test| cell 1\n'
        result = """wikiTableLineCells:
   wikiTableParameter:
      HTML_attribute:
         HTML_name:style
         HTML_value_quote:color:red
      HTML_attribute:
         HTML_name:id
         HTML_value_apostrophe:test
      HTML_attribute:
         HTML_name:name
         HTML_value_noquote:test
   wikiTableCellContent:
      @cleanInline@:
         rawText: cell 1"""
        self.parsed_equal_tree(source, result, 'wikiTableLine')

    def test_table_line_without_css(self):
        source = '| cell 1\n'
        result = "[@cleanInline@:[rawText:' cell 1']]"
        self.parsed_equal_string(source, result, 'wikiTableLine')

    def test_table_line_with_dash(self):
        source = '|data L2-B\n'
        result = "[@cleanInline@:[rawText:'data L2-B']]"
        self.parsed_equal_string(source, result, 'wikiTableLine')

    def test_table_line_with_2_cells(self):
        source = '| cell 1 || cell 2\n'
        result = """wikiTableLineCells:
   wikiTableCellContent:
      @cleanInline@:
         rawText: cell 1 
   wikiTableCellContent:
      @cleanInline@:
         rawText: cell 2"""
        self.parsed_equal_tree(source, result, 'wikiTableLine')

    def test_table_line_with_HTML_in_1st_cell(self):
        source = '| style="color:red" | cell 1 || cell 2\n'
        result = """wikiTableLineCells:
   wikiTableFirstCell:
      wikiTableParameter:
         HTML_attribute:
            HTML_name:style
            HTML_value_quote:color:red
      wikiTableCellContent:
         @cleanInline@:
            rawText: cell 1 
   wikiTableCellContent:
      @cleanInline@:
         rawText: cell 2"""
        self.parsed_equal_tree(source, result, 'wikiTableLine')

    def test_table_line_with_HTML_in_2nd_cell(self):
        source = '| cell 1 || style="color:red" | cell 2\n'
        result = """wikiTableLineCells:
   wikiTableCellContent:
      @cleanInline@:
         rawText: cell 1 
   wikiTableFirstCell:
      wikiTableParameter:
         HTML_attribute:
            HTML_name:style
            HTML_value_quote:color:red
      wikiTableCellContent:
         @cleanInline@:
            rawText: cell 2"""
        self.parsed_equal_tree(source, result, 'wikiTableLine')

    def test_table_header_with_css(self):
        source = '! scope=row | Line 1\n'
        result = """wikiTableLineHeader:
   wikiTableParameter:
      HTML_attribute:
         HTML_name:scope
         HTML_value_noquote:row
   wikiTableCellContent:
      @cleanInline@:
         rawText: Line 1"""
        self.parsed_equal_tree(source, result, 'wikiTableLine')

    def test_table_line_with_global_css(self):
        source = '|- style="color:red"\n'
        result = "[wikiTableParameters:[HTML_name:'style'  HTML_value_quote:'color:red']]"
        self.parsed_equal_string(source, result, 'wikiTableLine')

    def test_table_with_css(self):
        source = """{|
! cellA
! cellB
|- style="color:red"
| cell C
| cell D
|}
"""
        result = """@wikiTable@:
   wikiTableLineHeader:
      @cleanInline@:
         rawText: cellA
   wikiTableLineHeader:
      @cleanInline@:
         rawText: cellB
   wikiTableParamLineBreak:
      wikiTableParameters:
         HTML_name:style
         HTML_value_quote:color:red
   wikiTableLineCells:
      @cleanInline@:
         rawText: cell C
   wikiTableLineCells:
      @cleanInline@:
         rawText: cell D"""
        self.parsed_equal_tree(source, result, "wikiTable")

    def test_table_with_template(self):
        source = """{|
|+ Table {{title|parameter=yes}}
| cell 1 || cell 2
|-
| cell 3 || cell 4
|}
"""
        result = """@wikiTable@:
   wikiTableTitle:
      @cleanInline@:
         rawText: Table test: yes
   wikiTableLineCells:
      wikiTableCellContent:
         @cleanInline@:
            rawText: cell 1 
      wikiTableCellContent:
         @cleanInline@:
            rawText: cell 2
   wikiTableLineBreak:
   wikiTableLineCells:
      wikiTableCellContent:
         @cleanInline@:
            rawText: cell 3 
      wikiTableCellContent:
         @cleanInline@:
            rawText: cell 4"""
        templates = {'title': 'test: {{{parameter}}}'}
        self.parsed_equal_tree(source, result, "wikiTable", templates)

    def test_table_with_HTML_and_template(self):
        source = """{| class="wikitable" {{prettyTable}}
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
        result = """@wikiTable@:
   wikiTableBegin:
      wikiTableParameters:
         HTML_attribute:
            HTML_name:class
            HTML_value_quote:wikitable
         HTML_attribute:
            HTML_name:style
            HTML_value_quote:color:blue
   wikiTableContent:
      wikiTableTitle:
         wikiTableParameter:
            HTML_attribute:
               HTML_name:style
               HTML_value_quote:color:red
         wikiTableCellContent:
            @cleanInline@:
               rawText: Table test: parameter
      wikiTableLineBreak:
      wikiTableLineHeader:
         wikiTableParameter:
            HTML_attribute:
               HTML_name:scope
               HTML_value_noquote:col
         wikiTableCellContent:
            @cleanInline@:
               rawText: Title A
      wikiTableLineHeader:
         wikiTableParameter:
            HTML_attribute:
               HTML_name:scope
               HTML_value_noquote:col
         wikiTableCellContent:
            @cleanInline@:
               rawText: Title B
      wikiTableLineBreak:
      wikiTableLineHeader:
         wikiTableParameter:
            HTML_attribute:
               HTML_name:scope
               HTML_value_noquote:row
         wikiTableCellContent:
            @cleanInline@:
               rawText: Line 1
      wikiTableLineCells:
         @cleanInline@:
            rawText:data L1.A
      wikiTableLineCells:
         @cleanInline@:
            rawText:data L1.B
      wikiTableLineBreak:
      wikiTableLineHeader:
         wikiTableParameter:
            HTML_attribute:
               HTML_name:scope
               HTML_value_noquote:row
         wikiTableCellContent:
            @cleanInline@:
               rawText: Line 2
      wikiTableLineCells:
         @cleanInline@:
            rawText:data L2.A
      wikiTableLineCells:
         @cleanInline@:
            rawText:data with and L2.B..."""
        templates = {'prettyTable': 'style="color:blue"',
                     'title': 'test: {{{1}}}',
                     'template': '{{{1}}} and {{{parameters}}}...'}
        self.parsed_equal_tree(source, result, "wikiTable", templates)

    def test_nested_tables(self):
        source = """{| class="wikitable" {{prettyTable}}
|+ style="color:red" | Table {{title|1=true}}
|-
! scope=col | First (mother)
! scope=col | table
|
{| class="wikitable" {{prettyTable}}
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
        result = """@wikiTable@:
   wikiTableBegin:
      wikiTableParameters:
         HTML_attribute:
            HTML_name:class
            HTML_value_quote:wikitable
         HTML_attribute:
            HTML_name:style
            HTML_value_quote:color:blue
   wikiTableContent:
      wikiTableTitle:
         wikiTableParameter:
            HTML_attribute:
               HTML_name:style
               HTML_value_quote:color:red
         wikiTableCellContent:
            @cleanInline@:
               rawText: Table test: true
      wikiTableLineBreak:
      wikiTableLineHeader:
         wikiTableParameter:
            HTML_attribute:
               HTML_name:scope
               HTML_value_noquote:col
         wikiTableCellContent:
            @cleanInline@:
               rawText: First (mother)
      wikiTableLineHeader:
         wikiTableParameter:
            HTML_attribute:
               HTML_name:scope
               HTML_value_noquote:col
         wikiTableCellContent:
            @cleanInline@:
               rawText: table
      @wikiTable@:
         wikiTableBegin:
            wikiTableParameters:
               HTML_attribute:
                  HTML_name:class
                  HTML_value_quote:wikitable
               HTML_attribute:
                  HTML_name:style
                  HTML_value_quote:color:blue
         wikiTableContent:
            wikiTableLineBreak:
            wikiTableLineHeader:
               wikiTableParameter:
                  HTML_attribute:
                     HTML_name:scope
                     HTML_value_noquote:row
               wikiTableCellContent:
                  @cleanInline@:
                     rawText: Second (daughter) table
            wikiTableLineCells:
               @cleanInline@:
                  rawText:data L1.A
            wikiTableLineCells:
               @cleanInline@:
                  rawText:data L1.B
            wikiTableLineBreak:
            wikiTableLineHeader:
               wikiTableParameter:
                  HTML_attribute:
                     HTML_name:scope
                     HTML_value_noquote:row
               wikiTableCellContent:
                  @cleanInline@:
                     rawText: in the first one
            wikiTableLineCells:
               @cleanInline@:
                  rawText:data L2.A
            wikiTableLineCells:
               @cleanInline@:
                  rawText:data L2.B
      wikiTableLineBreak:
      wikiTableLineCells:
         @cleanInline@:
            rawText: first
      wikiTableLineCells:
         @cleanInline@:
            rawText: table
      wikiTableLineCells:
         @cleanInline@:
            rawText: again"""
        templates = {'prettyTable': 'style="color:blue"',
                     'title': 'test: {{{1}}}'}
        self.parsed_equal_tree(source, result, "wikiTable", templates)
