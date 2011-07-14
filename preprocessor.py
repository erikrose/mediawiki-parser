templates = {'template1': 'Content of template1.',
             'template 2': '"Template 2" has 2 parameters: {{{1}}} and: {{{name|default}}}!'}

def substitute_template_parameter(node, values={}):
    assert len(node.value) > 0, "Bad AST shape!"
    parameter_id = node.value[0].value
    if parameter_id in values:
        node.value = values[parameter_id]
    else:
        if len(node.value) > 1:
            # This is the default value
            node.value = node.value[1].value
        else:
            # No value at all: display the name of the parameter
            node.value = '{{{%s}}}' %  parameter_id

def substitute_template(node):
    if len(node.value) > 0:
        page_name = node.value[0].value
        count = 0
        parameters = {}
        if len(node.value) > 1:
            for parameter in node.value[1].value:
                if isinstance(parameter.value, unicode):
                    # It is a standalone parameter
                    count += 1 
                    parameters['%s' % count] = parameter.value
                else:
                    # It is a parameter with a name and a value
                    assert len(parameter.value) == 2, "Wrong AST shape!"
                    parameter_name = parameter.value[0].value
                    parameter_value = parameter.value[1].value
                    parameters['%s' % parameter_name] = parameter_value
        if page_name in templates:
            template = parse_template(templates[page_name], parameters)
            node.value = '%s' % template
        else:
            # FIXME: should be a link to page_name if page_name begins with a namespace
            # that is valid for this wiki or to Template:page_name otherwise
            node.value = '[[Template:%s]]' % page_name
    else:
        node.value = '{{}}'

toolset = {'substitute_template': substitute_template,
           'substitute_template_parameter': substitute_template_parameter}

from mediawiki_parser import preprocessorParser

def make_parser():
    return preprocessorParser.make_parser(toolset)

def parse_template(template, parameters):
    def subst_param(node):
        substitute_template_parameter(node, parameters)

    toolset['substitute_template_parameter'] = subst_param
    parser = preprocessorParser.make_parser(toolset)

    result = parser.parse(template)
    return result.value
