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
