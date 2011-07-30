from constants import html_entities
from pijnu.library.node import Nil, Nodes
from mediawiki_parser import wikitextParser

def toolset(allowed_tags, allowed_autoclose_tags, allowed_attributes):
    tags_stack = []
    
    def balance_tags(tag=None):
        i = 0
        if tag is not None:
            try:
                i = tags_stack.index(tag, -1)
            except:
                return ''
        result = ''
        while len(tags_stack) > i:
            result += '</%s>' % tags_stack.pop()
        return result

    def content(node):
        return '%s' % node.leaf() + balance_tags()

    def render_title1(node):
        node.value = '<h1>' + content(node) +  '</h1>\n'

    def render_title2(node):
        node.value = '<h2>' + content(node) +  '</h2>\n'

    def render_title3(node):
        node.value = '<h3>' + content(node) +  '</h3>\n'

    def render_title4(node):
        node.value = '<h4>' + content(node) +  '</h4>\n'

    def render_title5(node):
        node.value = '<h5>' + content(node) +  '</h5>\n'

    def render_title6(node):
        node.value = '<h6>' + content(node) +  '</h6>\n'

    def render_raw_text(node):
        node.value = "%s" % node.leaf()

    def render_paragraph(node):
        node.value = '<p>' + content(node) +  '</p>\n'

    def render_body(node):
        from apostrophes import parseAllQuotes
        node.value = '<body>\n' + parseAllQuotes(content(node)) +  '</body>'

    def render_entity(node):
        value = '%s' % node.leaf()
        if value in html_entities:
            node.value = '%s' % unichr(html_entities[value])
        else:
            node.value = '&amp;%s;' % value

    def render_lt(node):
        node.value = '&lt;'

    def render_gt(node):
        node.value = '&gt;'

    def process_attribute(node, allowed_tag):
        assert len(node.value) == 2, "Bad AST shape!"
        attribute_name = node.value[0].value
        attribute_value = node.value[1].value
        if attribute_name in allowed_attributes or not allowed_tag:
            return '%s="%s"' % (attribute_name, attribute_value)
        return ''

    def process_attributes(node, allowed_tag):
        result = ''
        if len(node.value) == 1:
            pass
        elif len(node.value) == 2:
            attributes = node.value[1].value
            for i in range(len(attributes)):
                attribute = process_attribute(attributes[i], allowed_tag)
                if attribute is not '':
                    result += ' ' + attribute 
        else:
            raise Exception("Bad AST shape!")
        return result

    def render_attribute(node):
        node.value = process_attribute(node, True)

    def render_tag_open(node):
        tag_name = node.value[0].value
        if tag_name in allowed_autoclose_tags:
            render_tag_autoclose(node)
        elif tag_name in allowed_tags:
            attributes = process_attributes(node, True)
            tags_stack.append(tag_name)
            node.value = '<%s%s>' % (tag_name, attributes) 
        else:
            attributes = process_attributes(node, False)
            node.value = '&lt;%s%s&gt;' % (tag_name, attributes)

    def render_tag_close(node):
        tag_name = node.value[0].value
        if tag_name in allowed_autoclose_tags:
            render_tag_autoclose(node)
        elif tag_name in allowed_tags:
            node.value = balance_tags(tag_name)
        else:
            node.value = "&lt;/%s&gt;" % tag_name

    def render_tag_autoclose(node):
        tag_name = node.value[0].value
        if tag_name in allowed_autoclose_tags:
            attributes = process_attributes(node, True)
            node.value = '<%s%s />' % (tag_name, attributes) 
        else:
            attributes = process_attributes(node, False)
            node.value = '&lt;%s%s /&gt;' % (tag_name, attributes)

    def render_table(node):
        table_parameters = ''
        table_content = ''
        if isinstance(node.value, Nodes) and node.value[0].tag == 'table_begin':
            attributes = node.value[0].value[0]
            for attribute in attributes:
                if attribute.tag == 'HTML_attribute':
                    table_parameters += ' ' + attribute.value
            contents = node.value[1].value
            for item in contents:
                table_content += content(item)
        else:
            table_content = content(node)
        node.value = '<table%s>\n<tr>\n%s</tr>\n</table>\n' % (table_parameters, table_content)

    def render_cell_content(node):
        if isinstance(node.value, Nil):
            return None
        cell_parameters = ''
        if len(node.value) > 1:
            values = node.value[0].value
            for value in values:
                if value.tag == 'HTML_attribute':
                    cell_parameters += ' ' + value.value
            cell_content = content(node.value[1])
        else:
            cell_content = content(node)
        return (cell_parameters, cell_content)

    def render_table_header_cell(node):
        content = render_cell_content(node)
        if content is not None:
            node.value = '\t<th%s>%s</th>\n' % content

    def render_table_normal_cell(node):
        content = render_cell_content(node)
        if content is not None:
            node.value = '\t<td%s>%s</td>\n' % content

    def render_table_empty_cell(node):
        node.value = '\t<td></td>\n'

    def render_table_caption(node):
        content = render_cell_content(node)
        if content is not None:
            node.value = '\t<caption%s>%s</caption>\n' % content

    def render_table_line_break(node):
        line_parameters = ''
        if node.value != '':
            assert len(node.value) == 1, "Bad AST shape!"
            parameters = node.value[0].value
            for value in parameters:
                if value.tag == 'HTML_attribute':
                    line_parameters += ' ' + value.value
        node.value = '</tr>\n<tr%s>\n' % line_parameters

    def render_preformatted(node):
        node.value = '<pre>' + content(node) +  '</pre>\n'

    def render_hr(node):
        node.value = '<hr />\n'

    def render_ul(list):
        result = '<ul>\n'
        for i in range(len(list)):
            result += '\t<li>' + content(list[i]) +  '</li>\n'
        result += '</ul>\n'
        return result

    def render_ol(list):
        result = '<ol>\n'
        for i in range(len(list)):
            result += '\t<li>' + content(list[i]) +  '</li>\n'
        result += '</ol>\n'
        return result

    def render_dd(list):
        result = '<dl>\n'
        for i in range(len(list)):
            result += '\t<dd>' + content(list[i]) +  '</dd>\n'
        result += '</dl>\n'
        return result

    def render_dt(list):
        result = '<dl>\n'
        for i in range(len(list)):
            result += '\t<dt>' + content(list[i]) +  '</dt>\n'
        result += '</dl>\n'
        return result

    def collapse_list(list):
        i = 0
        while i+1 < len(list):
            if list[i].tag == 'bullet_list_leaf' and list[i+1].tag == '@bullet_sub_list@' or \
               list[i].tag == 'number_list_leaf' and list[i+1].tag == '@number_sub_list@' or \
               list[i].tag == 'colon_list_leaf' and list[i+1].tag == '@colon_sub_list@' or \
               list[i].tag == 'semi_colon_list_leaf' and list[i+1].tag == '@semi_colon_sub_list@':
                list[i].value.append(list[i+1].value[0])
                list.pop(i+1)
            else:
                i += 1
        for i in range(len(list)):
            if isinstance(list[i].value, Nodes):
                collapse_list(list[i].value)

    def select_items(nodes, i, value):
        list_tags = ['bullet_list_leaf', 'number_list_leaf', 'colon_list_leaf', 'semi_colon_list_leaf']
        list_tags.remove(value)
        if isinstance(nodes[i].value, Nodes):
            render_lists(nodes[i].value)
        items = [nodes[i]]
        while i + 1 < len(nodes) and nodes[i+1].tag not in list_tags:
            if isinstance(nodes[i+1].value, Nodes):
                render_lists(nodes[i+1].value)
            items.append(nodes.pop(i+1))
        return items

    def render_lists(list):
        i = 0
        while i < len(list):
            if list[i].tag == 'bullet_list_leaf' or list[i].tag == '@bullet_sub_list@':
                list[i].value = render_ul(select_items(list, i, 'bullet_list_leaf'))
            elif list[i].tag == 'number_list_leaf' or list[i].tag == '@number_sub_list@':
                list[i].value = render_ol(select_items(list, i, 'number_list_leaf'))
            elif list[i].tag == 'colon_list_leaf' or list[i].tag == '@colon_sub_list@':
                list[i].value = render_dd(select_items(list, i, 'colon_list_leaf'))
            elif list[i].tag == 'semi_colon_list_leaf' or list[i].tag == '@semi_colon_sub_list@':
                list[i].value = render_dt(select_items(list, i, 'semi_colon_list_leaf'))
            i += 1

    def render_list(node):
        assert isinstance(node.value, Nodes), "Bad AST shape!"
        collapse_list(node.value)
        render_lists(node.value)

    return locals()

def make_parser(allowed_tags=[], allowed_autoclose_tags=[], allowed_attributes=[]):
    """Constructs the parser for the HTML backend.
    
    :arg allowed_tags: List of the HTML tags that should be allowed in the parsed wikitext.
            Opening tags will be closed. Closing tags with no opening tag will be removed.
            All the tags that are not in the list will be output as &lt;tag&gt;.
    :arg allowed_autoclose_tags: List of the self-closing tags that should be allowed in the
            parsed wikitext. All the other self-closing tags will be output as &lt;tag /&gt;
    :arg allowed_attributes: List of the HTML attributes that should be allowed in the parsed
            tags (e.g.: class="", style=""). All the other attributes (e.g.: onclick="") will
            be removed. 
    """
    tools = toolset(allowed_tags, allowed_autoclose_tags, allowed_attributes)
    return wikitextParser.make_parser(tools)
