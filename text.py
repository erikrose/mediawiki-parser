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

toolset = {'render_raw_text': render_raw_text,
           'render_paragraph': render_paragraph,
           'render_title2': render_title2,
           'render_body': render_body}

from mediawiki_parser import wikitextParser

def make_parser():
    return wikitextParser.make_parser(toolset)
