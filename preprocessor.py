from constants import html_entities

templates = {}
parsed_templates = {}  # Caches templates, to accelerate and avoid infinite loops

def substitute_named_entity(node):
    value = '%s' % node.leaf()
    if value in html_entities and value not in ['lt', 'gt']:
        node.value = unichr(html_entities[value])
    else:
        node.value = '&%s;' % value

def substitute_numbered_entity(node):
    try:
        value = int(node.leaf())
        # We eliminate some characters such as < and >
        if value in [60, 62]:
            raise Exception()
        node.value = unichr(value)
    except:
        node.value = '&#%s;' % value

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
    node_to_str = '%s' % node
    if node_to_str in parsed_templates:
        if parsed_templates[node_to_str] is not None:
            result = parsed_templates[node_to_str]
        else:
            result = 'Infinite template call detected!'
    else:
        parsed_templates[node_to_str] = None
        if len(node.value) > 0:
            page_name = node.value[0].value
            count = 0
            parameters = {}
            if len(node.value) > 1:
                for parameter in node.value[1].value:
                    if isinstance(parameter.value, unicode) or \
                       isinstance(parameter.value, str) or \
                       len(parameter.value) == 1:
                        # It is a standalone parameter
                        count += 1 
                        parameters['%s' % count] = parameter.value
                    elif len(parameter.value) == 2 and \
                         parameter.value[0].tag == 'parameter_name' and \
                         parameter.value[1].tag == 'parameter_value':
                        parameter_name = parameter.value[0].value
                        parameter_value = parameter.value[1].value
                        parameters['%s' % parameter_name] = parameter_value
                    else:
                        raise Exception("Bad AST shape!")
            if page_name in templates:
                template = parse_template(templates[page_name], parameters)
                result = '%s' % template
            else:
                # FIXME: should be a link to page_name if page_name begins with a namespace
                # that is valid for this wiki or to Template:page_name otherwise
                result = '[[Template:%s]]' % page_name
        else:
            result = '{{}}'
    node.value = result
    parsed_templates[node_to_str] = result

toolset = {'substitute_template': substitute_template,
           'substitute_template_parameter': substitute_template_parameter,
           'substitute_named_entity': substitute_named_entity,
           'substitute_numbered_entity': substitute_numbered_entity}

from mediawiki_parser import preprocessorParser

def make_parser(template_dict):
    global templates
    templates = template_dict
    global parsed_templates
    parsed_templates = {}
    return preprocessorParser.make_parser(toolset)

def parse_template(template, parameters):
    def subst_param(node):
        substitute_template_parameter(node, parameters)

    toolset['substitute_template_parameter'] = subst_param
    parser = preprocessorParser.make_parser(toolset)
    result = parser.parse(template)
    
    # We reinitialize this so that we won't pollute other templates with our values
    toolset['substitute_template_parameter'] = substitute_template_parameter
    return result.value
