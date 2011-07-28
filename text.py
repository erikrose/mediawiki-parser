from constants import html_entities
from mediawiki_parser import wikitextParser

def toolset():
    def render_tag_p(attributes):
        return '\n'

    def render_tag_br(attributes):
        return '\n'

    allowed_tags = {'p': render_tag_p,
                    'br': render_tag_br}

    def render_title1(node):
        node.value += '\n'

    def render_title2(node):
        node.value += '\n'

    def render_title3(node):
        node.value += '\n'

    def render_title4(node):
        node.value += '\n'

    def render_title5(node):
        node.value += '\n'

    def render_title6(node):
        node.value += '\n'

    def render_raw_text(node):
        pass
    
    def render_paragraph(node):
        node.value = '%s\n' % node.leaf()
    
    def render_body(node):
        from apostrophes import parseQuotes
        tags = {'bold': '*', 'bold_close': '*', 'italic': '_', 'italic_close': '_'}
        print node
        node.value = parseQuotes(node.leaf(), tags)
    
    def render_entity(node):
        value = '%s' % node.leaf()
        if value in html_entities:
            node.value = '%s' % unichr(html_entities[value])
        else:
            node.value = '&%s;' % value
    
    def render_lt(node):
        pass
    
    def render_gt(node):
        pass
    
    def process_attributes(node, allowed_tag):
        result = ''
        if len(node.value) == 1:
            pass
        elif len(node.value) == 2:
            attributes = node.value[1].value
            for i in range(len(attributes)):
                attribute_name = attributes[i].value[0].value
                attribute_value = attributes[i].value[1].value
                result += ' %s="%s"' % (attribute_name, attribute_value)
        else:
            raise Exception("Bad AST shape!")
        return result

    def render_attribute(node):
        node.value = process_attributes(node, True)

    def render_tag_open(node):
        tag_name = node.value[0].value
        if tag_name in allowed_tags:
            attributes = process_attributes(node, True)
            tag_processor = allowed_tags[tag_name]
            node.value = tag_processor(attributes) 
        else:
            attributes = process_attributes(node, False)
            node.value = '<%s%s>' % (tag_name, attributes)
    
    def render_tag_close(node):
        node.value = ''
    
    def render_tag_autoclose(node):
        tag_name = node.value[0].value
        if tag_name in allowed_tags:
            attributes = process_attributes(node, True)
            tag_processor = allowed_tags[tag_name]
            node.value = tag_processor(attributes) 
        else:
            attributes = process_attributes(node, False)
            node.value = '<%s%s />' % (tag_name, attributes)

    def render_table(node):
        pass

    def render_table_line_break(node):
        node.value = '\n'

    def render_table_header_cell(node):
        pass

    def render_table_normal_cell(node):
        pass

    def render_table_empty_cell(node):
        pass

    def render_table_caption(node):
        pass

    def render_preformatted(node):
        pass

    def render_hr(node):
        node.value = '------'

    def render_li(node):
        pass

    def render_list(node):
        pass

    return locals()

def make_parser():
    return wikitextParser.make_parser(toolset())
