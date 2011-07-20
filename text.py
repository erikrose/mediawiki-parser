from constants import html_entities

def render_title2(node):
    node.value += '\n'

def render_title6(node):
    node.value += '\n'

def render_raw_text(node):
    pass

def render_paragraph(node):
    node.value += '\n'

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

toolset = {'render_raw_text': render_raw_text,
           'render_paragraph': render_paragraph,
           'render_title2': render_title2,
           'render_body': render_body,
           'render_entity': render_entity,
           'render_lt': render_lt,
           'render_gt': render_gt}

from mediawiki_parser import wikitextParser

def make_parser():
    return wikitextParser.make_parser(toolset)
