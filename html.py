from constants import html_entities

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
