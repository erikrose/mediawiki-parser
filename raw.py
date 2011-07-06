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
