# -*- coding: utf8 -*-

from mediawiki_parser.tests import ParserTestCase


class Templates_tests(ParserTestCase):
    def test_template_without_parameter(self):
        source = """{{Template}}"""
        result = """@inline@:
   template:
      page_name:Template"""
        self.parsed_equal_tree(source, result, 'inline')

    def test_template_with_parameters(self):
        source = """{{Template with|1=parameter| 2 = parameters }}"""
        result = """@inline@:
   template:
      page_name:Template with
      parameters:
         parameter:
            parameter_name:1
            optional_value:
               rawText:parameter
         parameter:
            parameter_name:2 
            optional_value:
               rawText: parameters """
        self.parsed_equal_tree(source, result, 'inline')

    def test_template_with_multiline_parameters(self):
        source = """{{Template which
 | is = test
 | multi = test
 | lines = test
}}"""
        result = """@inline@:
   template:
      page_name:Template which
      parameters:
         parameter:
            parameter_name:is 
            optional_value:
               rawText: test
         parameter:
            parameter_name:multi 
            optional_value:
               rawText: test
         parameter:
            parameter_name:lines 
            optional_value:
               rawText: test"""
        self.parsed_equal_tree(source, result, 'inline')

    def test_template_inside_a_text(self):
        source = """A template {{Template with|1=parameter| 2 = parameters }} inside a text."""
        result = """@inline@:
   rawText:A template 
   template:
      page_name:Template with
      parameters:
         parameter:
            parameter_name:1
            optional_value:
               rawText:parameter
         parameter:
            parameter_name:2 
            optional_value:
               rawText: parameters 
   rawText: inside a text."""
        self.parsed_equal_tree(source, result, 'inline')

    def test_template_with_formatted_parameters(self):
        source = """Formatted arguments in a template {{Template with|1='''parameter'''| 2 = ''parameters'' }}."""
        result = """@inline@:
   rawText:Formatted arguments in a template 
   template:
      page_name:Template with
      parameters:
         parameter:
            parameter_name:1
            optional_value:
               rawText:<strong>parameter</strong>
         parameter:
            parameter_name:2 
            optional_value:
               rawText: <em>parameters</em> 
   rawText:."""
        self.parsed_equal_tree(source, result, 'inline')

    def test_nested_templates(self):
        source = """A {{Template with|{{other}} |1={{templates}}| 2 = {{nested|inside=1}} }}."""
        result = """@inline@:
   rawText:A 
   template:
      page_name:Template with
      parameters:
         parameter:
            template:
               page_name:other
            rawText: 
         parameter:
            parameter_name:1
            optional_value:
               template:
                  page_name:templates
         parameter:
            parameter_name:2 
            optional_value:
               rawText: 
               template:
                  page_name:nested
                  parameters:
                     parameter:
                        parameter_name:inside
                        optional_value:
                           rawText:1
               rawText: 
   rawText:."""
        self.parsed_equal_tree(source, result, 'inline')
