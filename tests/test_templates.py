# -*- coding: utf8 -*-

from mediawiki_parser.tests import PreprocessorTestCase


class TemplatesTests(PreprocessorTestCase):
    def test_existent_template_without_parameter(self):
        source = "a {{Template}}"
        result = "a template content"
        templates = {'Template': 'template content'}
        self.parsed_equal_string(source, result, templates)

    def test_nonexistant_template_without_parameter(self):
        source = "a {{test}}"
        result = "a [[Template:test]]"
        self.parsed_equal_string(source, result)

    def test_numeric_template_parameter(self):
        source = "{{{1}}}"
        result = "{{{1}}}"
        self.parsed_equal_string(source, result)

    def test_text_template_parameter(self):
        source = "{{{A text}}}"
        result = "{{{A text}}}"
        self.parsed_equal_string(source, result)

    def test_template_name_as_parameter_name(self):
        "Template should of course not be substituted in this case."
        source = "a {{{Template}}}"
        result = "a {{{Template}}}"
        templates = {'Template': 'template content'}
        self.parsed_equal_string(source, result, templates)

    def test_template_parameter_with_default_value(self):
        source = "{{{parameter name|default value}}}"
        result = "default value"
        self.parsed_equal_string(source, result)

    def test_template_parameter_with_void_default_value(self):
        source = "{{{parameter name|}}}"
        result = ""
        self.parsed_equal_string(source, result)

    def test_nested_default_values(self):
        source = "Cheese or dessert? Person1: {{menu|cheese=camembert}}; person2: {{menu|dessert=apple}}; person3: {{menu}}."
        result = "Cheese or dessert? Person1: Menu: camembert; person2: Menu: apple; person3: Menu: not cheese nor dessert."
        templates = {'menu': 'Menu: {{{cheese|{{{dessert|not cheese nor dessert}}}}}}'}
        self.parsed_equal_string(source, result, templates)

    def test_template_with_parameters(self):
        source = "{{Template with|1=parameter| 2 = parameters}}"
        result = "test parameter parameters"
        templates = {'Template with': 'test {{{1}}} {{{2}}}'}
        self.parsed_equal_string(source, result, templates)

    def test_template_with_automatic_numbering_parameters(self):
        source = "a {{Template with|parameter1|parameter2}}"
        result = "a test: parameter1 parameter2"
        templates = {'Template with': 'test: {{{1}}} {{{2}}}'}
        self.parsed_equal_string(source, result, templates)

    def test_equal_in_template_parameter(self):
        source = "a {{Template with|1=a=b|2=text text = test test}}"
        result = "a test: a=b text text = test test"
        templates = {'Template with': 'test: {{{1}}} {{{2}}}'}
        self.parsed_equal_string(source, result, templates)

    def test_empty_template_parameter(self):
        "We pass an empty value, which is different than no value at all."
        source = "a {{Template with|1=}}"
        result = "a test: "
        templates = {'Template with': 'test: {{{1}}}'}
        self.parsed_equal_string(source, result, templates)

    def test_pipe_in_template_parameter(self):
        source = "a {{Template with|apple{{!}}orange{{!}}lemon}}"
        result = "a test: apple|orange|lemon"
        templates = {'Template with': 'test: {{{1}}}',
                     '!': '|'}
        self.parsed_equal_string(source, result, templates)

    def test_template_parameters_precedence(self):
        "Defining a second time the same parameter should overwrite the previous one"
        source = "a {{Template with|parameter1|1=parameter2}}"
        result = "a test: parameter2"
        templates = {'Template with': 'test: {{{1}}}'}
        self.parsed_equal_string(source, result, templates)

    def test_template_with_multiline_named_parameters(self):
        source = """{{Template which
 | has = test1
 | multi = test2
 | line parameters = test3
}}"""
        result = "Tests: test1 test3 test2..."
        templates = {'Template which': 'Tests: {{{has}}} {{{line parameters}}} {{{multi}}}...'}
        self.parsed_equal_string(source, result, templates)

    def test_template_with_special_chars_in_parameters(self):
        source = "Special chars: {{Template with|1=#<>--| two = '{'}'[']'}}."
        result = "Special chars: test #<>-- '{'}'[']' default."
        templates = {'Template with': 'test {{{1}}} {{{two}}} {{{other param|default}}}'}
        self.parsed_equal_string(source, result, templates)

    def test_links_in_template_arguments(self):
        source = "A {{Template with|1=[http://www.mozilla.org a link] |2=[[inside]] | 3 = [[the|parameters]]}}."
        result = "A test: [http://www.mozilla.org a link]  [[inside]]  [[the|parameters]]."
        templates = {'Template with': 'test: {{{1}}} {{{2}}} {{{3}}}'}
        self.parsed_equal_string(source, result, templates)

    def test_formatted_template_arguments(self):
        "The formatted arguments are allowed, but will be processed in the parser, not in the preprocessor."
        source = "A {{Template with|an argument ''in italic'' |and another one '''in bold'''}}."
        result = "A test: an argument ''in italic''  and another one '''in bold'''."
        templates = {'Template with': 'test: {{{1}}} {{{2}}}'}
        self.parsed_equal_string(source, result, templates)

    def test_template_in_nowiki_section(self):
        "<nowiki> sections must be left untouched"
        source = "a <nowiki>{{Template with|an argument ''in italic'' |and another one '''in bold'''}} section </nowiki>."
        result = "a <nowiki>{{Template with|an argument ''in italic'' |and another one '''in bold'''}} section </nowiki>."
        self.parsed_equal_string(source, result)

    def test_template_in_preformatted_section(self):
        "<pre> sections must be left untouched"
        source = "a <pre>{{Template with|an argument ''in italic'' |and another one '''in bold'''}} section </pre>."
        result = "a <pre>{{Template with|an argument ''in italic'' |and another one '''in bold'''}} section </pre>."
        self.parsed_equal_string(source, result)

    def test_nested_template(self):
        source = "A {{Template with|{{other|inside}}}}."
        result = "A test is inside."
        templates = {'Template with': 'test {{{1}}}',
                     'other': 'is {{{1}}}'}
        self.parsed_equal_string(source, result, templates)

    def test_nested_templates(self):
        source = "{{Template with|1={{other}} |2= {{templates}}| 3 = {{nested|inside=1}} }}"
        result = "1: [[Template:other]] ; 2: another nested template with parameter inside!; 3: nested template with parameter 1 "
        templates = {'Template with': '1: {{{1}}}; 2: {{{2}}}; 3: {{{3}}}',
                     'templates': 'another {{nested|inside = inside}}!',
                     'nested': 'nested template with parameter {{{inside}}}'}
        self.parsed_equal_string(source, result, templates)

    def test_self_nested_templates(self):
        source = "{{template 2|1=Value1|name={{template 2|1=Value1|name=Value for name}}}}"
        result = '"Template 2" has 2 parameters: Value1 and: "Template 2" has 2 parameters: Value1 and: Value for name!!'
        templates = {'template 2': '"Template 2" has 2 parameters: {{{1}}} and: {{{name|default}}}!'}
        self.parsed_equal_string(source, result, templates)

    def test_infinite_loop_calls_protection(self):
        source = "We call {{a}} and {{b}}"
        result = 'We call calls calls calls Infinite template call detected! and calls calls Infinite template call detected!'
        templates = {'a': 'calls {{b}}',
                     'b': 'calls {{c}}',
                     'c': 'calls {{a}}'}
        self.parsed_equal_string(source, result, templates)

    def test_finite_loop_calls(self):
        source = "A call {{aa|{{bb}}}}"
        result = 'A call calls calls calls calls end'
        templates = {'aa': 'calls {{{1|end}}}',
                     'bb': 'calls {{cc}}',
                     'cc': 'calls {{aa}}'}
        self.parsed_equal_string(source, result, templates)
