from constants import html_entities

allowed_tags = {}

def toolset():
    def render_title2(node):
        pass
    
    def render_title6(node):
        pass
    
    def render_raw_text(node):
        from apostrophes import parseQuotes
        node.value = "%s" % parseQuotes(node.leaf())
    
    def render_paragraph(node):
        pass
    
    def render_body(node):
        pass
    
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
    
    def render_tag_open(node):
        pass
    
    def render_tag_close(node):
        pass
    
    def render_tag_autoclose(node):
        pass

    return locals()

toolset = toolset()

from mediawiki_parser import wikitextParser

def make_parser():
    return wikitextParser.make_parser(toolset)
