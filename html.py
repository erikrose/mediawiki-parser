from constants import html_entities

def toolset():
    allowed_tags = ['p', 'span', 'b', 'br', 'hr']
    allowed_parameters = ['class', 'style', 'name', 'id', 'scope']

    def render_title2(node):
        node.value = '<h2>%s</h2>\n' % node.leaf()

    def render_title6(node):
        node.value = '<h6>%s</h6>\n' % node.leaf()

    def render_raw_text(node):
        from apostrophes import parseQuotes
        node.value = "%s" % parseQuotes(node.leaf())

    def render_paragraph(node):
        node.value = '<p>%s</p>\n' % node.leaf()

    def render_body(node):
        node.value = '<body>\n%s</body>' % node.leaf()

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
        if len(node.value) > 1 and node.value[0].tag == 'table_begin':
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
        from pijnu.library.node import Nil
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

    return locals()

toolset = toolset()

from mediawiki_parser import wikitextParser

def make_parser():
    return wikitextParser.make_parser(toolset)
