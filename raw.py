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

from mediawiki_parser.wikitextParser import make_parser

toolset = {'render_raw_text': render_raw_text,
           'render_paragraph': render_paragraph,
           'render_title2': render_title2,
           'render_body': render_body}
parser = make_parser(toolset)
