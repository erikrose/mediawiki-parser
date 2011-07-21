from constants import html_entities

def toolset():
    allowed_tags = ['p', 'span', 'b', 'br', 'hr']
    allowed_parameters = ['class', 'style', 'name', 'id']

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
    
    def process_attributes(node, allowed_tag):
        result = ''
        if len(node.value) == 1:
            pass
        elif len(node.value) == 2:
            attributes = node.value[1].value
            for i in range(len(attributes)):
                attribute_name = attributes[i].value[0].value
                attribute_value = attributes[i].value[1].value
                if not allowed_tag or attribute_name in allowed_parameters:
                    result += ' %s="%s"' % (attribute_name, attribute_value)
        else:
            raise Exception("Bad AST shape!")
        return result
    
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
    
    return locals()

toolset = toolset()

from mediawiki_parser import wikitextParser

def make_parser():
    return wikitextParser.make_parser(toolset)
