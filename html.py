from constants import html_entities
from pijnu.library.node import Nil, Nodes
from mediawiki_parser import wikitextParser

def toolset(allowed_tags, allowed_parameters):
    def render_title1(node):
        node.value = '<h1>%s</h1>\n' % node.leaf()

    def render_title2(node):
        node.value = '<h2>%s</h2>\n' % node.leaf()

    def render_title3(node):
        node.value = '<h3>%s</h3>\n' % node.leaf()

    def render_title4(node):
        node.value = '<h4>%s</h4>\n' % node.leaf()

    def render_title5(node):
        node.value = '<h5>%s</h5>\n' % node.leaf()

    def render_title6(node):
        node.value = '<h6>%s</h6>\n' % node.leaf()

    def render_raw_text(node):
        node.value = "%s" % node.leaf()

    def render_paragraph(node):
        node.value = '<p>%s</p>\n' % node.leaf()

    def render_body(node):
        from apostrophes import parseQuotes
        node.value = '<body>\n%s</body>' % parseQuotes(node.leaf())

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
        if attribute_name in allowed_parameters or not allowed_tag:
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
        if tag_name in allowed_tags:
            attributes = process_attributes(node, True)
            node.value = '<%s%s>' % (tag_name, attributes) 
        else:
            attributes = process_attributes(node, False)
            node.value = '&lt;%s%s&gt;' % (tag_name, attributes)

    def render_tag_close(node):
        tag_name = node.value[0].value
        if tag_name in allowed_tags:
            node.value = "</%s>" % tag_name
        else:
            node.value = "&lt;/%s&gt;" % tag_name

    def render_tag_autoclose(node):
        tag_name = node.value[0].value
        if tag_name in allowed_tags:
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
            for content in contents:
                table_content += content.leaf() 
        else:
            table_content = node.leaf()
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
            cell_content = node.value[1].leaf()
        else:
            cell_content = node.leaf()
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
        node.value = '<pre>%s</pre>\n' % node.leaf()

    def render_hr(node):
        node.value = '<hr />\n'

    def render_ul(list):
        result = '<ul>\n'
        for i in range(len(list)):
            result += '\t<li>%s</li>\n' % list[i].leaf()
        result += '</ul>\n'
        return result

    def render_ol(list):
        result = '<ol>\n'
        for i in range(len(list)):
            result += '\t<li>%s</li>\n' % list[i].leaf()
        result += '</ol>\n'
        return result

    def render_dd(list):
        result = '<dl>\n'
        for i in range(len(list)):
            result += '\t<dd>%s</dd>\n' % list[i].leaf()
        result += '</dl>\n'
        return result

    def render_dt(list):
        result = '<dl>\n'
        for i in range(len(list)):
            result += '\t<dt>%s</dt>\n' % list[i].leaf()
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

def make_parser(allowed_tags=[], allowed_parameters=[]):
    tools = toolset(allowed_tags, allowed_parameters)
    return wikitextParser.make_parser(tools)
