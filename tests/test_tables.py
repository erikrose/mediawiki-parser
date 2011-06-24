# -*- coding: utf8 -*-

from mediawiki_parser import wikitextParser
mediawikiParser = wikitextParser.wikitextParser

from unittest import TestCase


class NowikiTests(TestCase):
    def test_table_first_cell(self):
        source = 'style="color:red" | cell 1'
        exp_result = "[<?>:[CSS_attributes:[CSS_text:'style=\"color:red\" ']]  <?>:[@cleanInline@:[rawText:' cell 1']]]"
        got_result = unicode(mediawikiParser.wikiTableFirstCell.parseTest(source).value)
        self.assertEquals(exp_result, got_result)

    def test_table_other_cell(self):
        source = '|| cell 1'
        exp_result = "[@cleanInline@:[rawText:' cell 1']]"
        got_result = unicode(mediawikiParser.wikiTableOtherCell.parseTest(source).value)
        self.assertEquals(exp_result, got_result)

    def test_table_special_line(self):
        source = '|-\n'
        exp_result = ""
        got_result = unicode(mediawikiParser.wikiTableSpecialLine.parseTest(source).value)
        self.assertEquals(exp_result, got_result)

    def test_table_line_with_css(self):
        source = '| style="color:red" | cell 1\n'
        exp_result = "[wikiTableLineCells:[<?>:[CSS_attributes:[CSS_text:' style=\"color:red\" ']]  <?>:[@cleanInline@:[rawText:' cell 1']]]]"
        got_result = unicode(mediawikiParser.wikiTableLine.parseTest(source).value)
        self.assertEquals(exp_result, got_result)

    def test_table_line_without_css(self):
        source = '| cell 1\n'
        exp_result = "[wikiTableLineCells:[@cleanInline@:[rawText:' cell 1']]]"
        got_result = unicode(mediawikiParser.wikiTableLine.parseTest(source).value)
        self.assertEquals(exp_result, got_result)

    def test_table_line_with_dash(self):
        source = '|data L2-B\n'
        exp_result = "[wikiTableLineCells:[@cleanInline@:[rawText:'data L2-B']]]"
        got_result = unicode(mediawikiParser.wikiTableLine.parseTest(source).value)
        self.assertEquals(exp_result, got_result)

    def test_table_line_with_2_cells(self):
        source = '| cell 1 || cell 2\n'
        exp_result = "[wikiTableLineCells:[wikiTableFirstCell:[@cleanInline@:[rawText:' cell 1 ']]  <?>:[wikiTableOtherCell:[@cleanInline@:[rawText:' cell 2']]]]]"
        got_result = unicode(mediawikiParser.wikiTableLine.parseTest(source).value)
        self.assertEquals(exp_result, got_result)

    def test_table_line_with_css_in_1st_cell(self):
        source = '| style="color:red" | cell 1 || cell 2\n'
        exp_result = "[wikiTableLineCells:[wikiTableFirstCell:[<?>:[CSS_attributes:[CSS_text:' style=\"color:red\" ']]  <?>:[@cleanInline@:[rawText:' cell 1 ']]]  <?>:[wikiTableOtherCell:[@cleanInline@:[rawText:' cell 2']]]]]"
        got_result = unicode(mediawikiParser.wikiTableLine.parseTest(source).value)
        self.assertEquals(exp_result, got_result)

    def test_table_line_with_css_in_2nd_cell(self):
        source = '| cell 1 || style="color:red" | cell 2\n'
        exp_result = "[wikiTableLineCells:[wikiTableFirstCell:[@cleanInline@:[rawText:' cell 1 ']]  <?>:[wikiTableOtherCell:[<?>:[CSS_attributes:[CSS_text:' style=\"color:red\" ']]  <?>:[@cleanInline@:[rawText:' cell 2']]]]]]"
        got_result = unicode(mediawikiParser.wikiTableLine.parseTest(source).value)
        self.assertEquals(exp_result, got_result)

    def test_table__header_with_css(self):
        source = '! scope=row | Line 1\n'
        exp_result = "[wikiTableLineHeader:[<?>:[CSS_attributes:[CSS_text:' scope=row ']]  <?>:[@cleanInline@:[rawText:' Line 1']]]]"
        got_result = unicode(mediawikiParser.wikiTableLine.parseTest(source).value)
        self.assertEquals(exp_result, got_result)

    def test_table_line_with_global_css(self):
        source = '|- style="color:red"\n'
        exp_result = "[wikiTableParamLineBreak:[wikiTableParameters:' style=\"color:red\"']]"
        got_result = unicode(mediawikiParser.wikiTableLine.parseTest(source).value)
        self.assertEquals(exp_result, got_result)

    def test_table_with_css(self):
        source = """{|
! cellA
! cellB
|- style="color:red"
| cell C
| cell D
|}
"""
        exp_result = """@wikiTable@:
   <?>:

   <?>:
      wikiTableLine:
         wikiTableLineHeader:
            @cleanInline@:
               rawText: cellA
      wikiTableLine:
         wikiTableLineHeader:
            @cleanInline@:
               rawText: cellB
      wikiTableLine:
         wikiTableParamLineBreak:
            wikiTableParameters: style="color:red"
      wikiTableLine:
         wikiTableLineCells:
            @cleanInline@:
               rawText: cell C
      wikiTableLine:
         wikiTableLineCells:
            @cleanInline@:
               rawText: cell D"""
        got_result = mediawikiParser.wikiTable.parseTest(source).treeView()
        self.assertEquals(exp_result, got_result)

    def test_table_with_template(self):
        source = """{|
|+ Table {{title|parameter=yes}}
| cell 1 || cell 2
|-
| cell 3 || cell 4
|}
"""
        exp_result = """@wikiTable@:
   <?>:

   <?>:
      wikiTableLine:
         wikiTableTitle:
            @inline@:
               rawText: Table 
               advancedTemplate:
                  pageName:title
                  parameters:
                     parameter:
                        parameterName:parameter
                        optionalValue:
                           rawText:yes
      wikiTableLine:
         wikiTableLineCells:
            wikiTableFirstCell:
               @cleanInline@:
                  rawText: cell 1 
            <?>:
               wikiTableOtherCell:
                  @cleanInline@:
                     rawText: cell 2
      wikiTableLine:
         wikiTableLineBreak:
      wikiTableLine:
         wikiTableLineCells:
            wikiTableFirstCell:
               @cleanInline@:
                  rawText: cell 3 
            <?>:
               wikiTableOtherCell:
                  @cleanInline@:
                     rawText: cell 4"""
        got_result = mediawikiParser.wikiTable.parseTest(source).treeView()
        self.assertEquals(exp_result, got_result)

    def test_table_with_css_and_template(self):
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
        exp_result = """@wikiTable@:
   wikiTableBegin:
      wikiTableParameters:
         CSS_text: class="wikitable" 
         @cleanInline@:
            simpleTemplate:prettyTable
   <?>:

   <?>:
      wikiTableLine:
         wikiTableTitle:
            <?>:
               CSS_attributes:
                  CSS_text: style="color:red" 
            <?>:
               @inline@:
                  rawText: Table 
                  advancedTemplate:
                     pageName:title
                     parameters:
                        parameter:parameter
      wikiTableLine:
         wikiTableLineBreak:
      wikiTableLine:
         wikiTableLineHeader:
            <?>:
               CSS_attributes:
                  CSS_text: scope=col 
            <?>:
               @cleanInline@:
                  rawText: Title A
      wikiTableLine:
         wikiTableLineHeader:
            <?>:
               CSS_attributes:
                  CSS_text: scope=col 
            <?>:
               @cleanInline@:
                  rawText: Title B
      wikiTableLine:
         wikiTableLineBreak:
      wikiTableLine:
         wikiTableLineHeader:
            <?>:
               CSS_attributes:
                  CSS_text: scope=row 
            <?>:
               @cleanInline@:
                  rawText: Line 1
      wikiTableLine:
         wikiTableLineCells:
            @cleanInline@:
               rawText:data L1.A
      wikiTableLine:
         wikiTableLineCells:
            @cleanInline@:
               rawText:data L1.B
      wikiTableLine:
         wikiTableLineBreak:
      wikiTableLine:
         wikiTableLineHeader:
            <?>:
               CSS_attributes:
                  CSS_text: scope=row 
            <?>:
               @cleanInline@:
                  rawText: Line 2
      wikiTableLine:
         wikiTableLineCells:
            @cleanInline@:
               rawText:data L2.A
      wikiTableLine:
         wikiTableLineCells:
            @cleanInline@:
               rawText:data 
               advancedTemplate:
                  pageName:template
                  parameters:
                     parameter:with
                     parameter:
                        parameterName:parameters
                        optionalValue:
                           rawText:L2.B"""
        got_result = mediawikiParser.wikiTable.parseTest(source).treeView()
        self.assertEquals(exp_result, got_result)

    def test_nested_tables(self):
        source = """{| class="wikitable" {{prettyTable|1=true}}
|+ style="color:red" | Table {{title}}
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
        exp_result = """@wikiTable@:
   wikiTableBegin:
      wikiTableParameters:
         CSS_text: class="wikitable" 
         @cleanInline@:
            advancedTemplate:
               pageName:prettyTable
               parameters:
                  parameter:
                     parameterName:1
                     optionalValue:
                        rawText:true
   <?>:

   <?>:
      wikiTableLine:
         wikiTableTitle:
            <?>:
               CSS_attributes:
                  CSS_text: style="color:red" 
            <?>:
               @inline@:
                  rawText: Table 
                  simpleTemplate:title
      wikiTableLine:
         wikiTableLineBreak:
      wikiTableLine:
         wikiTableLineHeader:
            <?>:
               CSS_attributes:
                  CSS_text: scope=col 
            <?>:
               @cleanInline@:
                  rawText: First (mother)
      wikiTableLine:
         wikiTableLineHeader:
            <?>:
               CSS_attributes:
                  CSS_text: scope=col 
            <?>:
               @cleanInline@:
                  rawText: table
      @wikiTable@:
         wikiTableBegin:
            wikiTableParameters:
               CSS_text: class="wikitable" 
               @cleanInline@:
                  simpleTemplate:prettyTable
         <?>:

         <?>:
            wikiTableLine:
               wikiTableLineBreak:
            wikiTableLine:
               wikiTableLineHeader:
                  <?>:
                     CSS_attributes:
                        CSS_text: scope=row 
                  <?>:
                     @cleanInline@:
                        rawText: Second (daughter) table
            wikiTableLine:
               wikiTableLineCells:
                  @cleanInline@:
                     rawText:data L1.A
            wikiTableLine:
               wikiTableLineCells:
                  @cleanInline@:
                     rawText:data L1.B
            wikiTableLine:
               wikiTableLineBreak:
            wikiTableLine:
               wikiTableLineHeader:
                  <?>:
                     CSS_attributes:
                        CSS_text: scope=row 
                  <?>:
                     @cleanInline@:
                        rawText: in the first one
            wikiTableLine:
               wikiTableLineCells:
                  @cleanInline@:
                     rawText:data L2.A
            wikiTableLine:
               wikiTableLineCells:
                  @cleanInline@:
                     rawText:data L2.B
      wikiTableLine:
         wikiTableLineBreak:
      wikiTableLine:
         wikiTableLineCells:
            @cleanInline@:
               rawText: first
      wikiTableLine:
         wikiTableLineCells:
            @cleanInline@:
               rawText: table
      wikiTableLine:
         wikiTableLineCells:
            @cleanInline@:
               rawText: again"""
        got_result = mediawikiParser.wikiTable.parseTest(source).treeView()
        self.assertEquals(exp_result, got_result)
