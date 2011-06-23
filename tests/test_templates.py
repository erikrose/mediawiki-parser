# -*- coding: utf8 -*-

from mediawiki_parser import wikitextParser
mediawikiParser = wikitextParser.wikitextParser

from unittest import TestCase


class NowikiTests(TestCase):
    def test_template_with_parameters(self):
        source = """{{Template with|1=parameter| 2 = parameters }}"""
        result = """@inline@:
   advancedTemplate:
      pageName:Template with
      parameters:
         parameter:
            parameterName:1
            optionalValue:
               rawText:parameter
         parameter:
            parameterName:2
            optionalValue:
               rawText: parameters """
        mediawikiParser.inline.testSuiteMultiline([source], [result])

    def test_template_with_multiline_parameters(self):
        source = """{{Template which
 | is = test
 | multi = test
 | lines = test
}}"""
        result = """@inline@:
   advancedTemplate:
      pageName:Template which
      parameters:
         parameter:
            parameterName:is
            optionalValue:
               rawText: test
         parameter:
            parameterName:multi
            optionalValue:
               rawText: test
         parameter:
            parameterName:lines
            optionalValue:
               rawText: test"""
        mediawikiParser.inline.testSuiteMultiline([source], [result])

    def test_template_inside_a_text(self):
        source = """A template {{Template with|1=parameter| 2 = parameters }} inside a text."""
        result = """@inline@:
   rawText:A template
   advancedTemplate:
      pageName:Template with
      parameters:
         parameter:
            parameterName:1
            optionalValue:
               rawText:parameter
         parameter:
            parameterName:2
            optionalValue:
               rawText: parameters
   rawText: inside a text."""
        mediawikiParser.inline.testSuiteMultiline([source], [result])

    def test_template_with_formatted_parameters(self):
        source = """Formatted arguments in a template {{Template with|1='''parameter'''| 2 = ''parameters'' }}."""
        result = """@inline@:
   rawText:Formatted arguments in a template
   advancedTemplate:
      pageName:Template with
      parameters:
         parameter:
            parameterName:1
            optionalValue:
               rawText:<strong>parameter</strong>
         parameter:
            parameterName:2
            optionalValue:
               rawText: <em>parameters</em>
   rawText:."""
        mediawikiParser.inline.testSuiteMultiline([source], [result])

    def test_nested_templates(self):
        source = """A {{Template with|{{other}} |1={{templates}}| 2 = {{nested|inside=1}} }}."""
        result = """@inline@:
   rawText:A
   advancedTemplate:
      pageName:Template with
      parameters:
         parameter:
            simpleTemplate:other
            rawText:
         parameter:
            parameterName:1
            optionalValue:
               simpleTemplate:templates
         parameter:
            parameterName:2
            optionalValue:
               rawText:
               advancedTemplate:
                  pageName:nested
                  parameters:
                     parameter:
                        parameterName:inside
                        optionalValue:
                           rawText:1
               rawText:
   rawText:."""
        mediawikiParser.inline.testSuiteMultiline([source], [result])
