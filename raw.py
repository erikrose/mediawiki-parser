from constants import html_entities
from mediawiki_parser import wikitextParser

def toolset():
    def render_title1(node):
        pass

    def render_title2(node):
        pass

    def render_title3(node):
        pass

    def render_title4(node):
        pass

    def render_title5(node):
        pass

    def render_title6(node):
        pass
    
    def render_raw_text(node):
        pass
    
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

    def render_attribute(node):
        pass

    def render_table(node):
        pass

    def render_table_line_break(node):
        pass

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
        pass

    def render_li(node):
        pass

    def render_list(node):
        pass

    def render_url(node):
        pass

    def render_external_link(node):
        pass

    def render_internal_link(node):
        pass

    return locals()

def make_parser():
    return wikitextParser.make_parser(toolset())
