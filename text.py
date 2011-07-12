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

def make_parser():
    from mediawiki_parser.wikitextParser import make_parser
    return make_parser(toolset)
