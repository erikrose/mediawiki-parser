from constants import html_entities
from pijnu.library.node import Nil, Nodes
from mediawiki_parser import wikitextParser
from mutagen import Metadata
import apostrophes

def toolset(allowed_tags, allowed_autoclose_tags, allowed_attributes, interwiki, namespaces):
    tags_stack = []

    external_autonumber = []
    """ This is for the autonumbering of external links.
    e.g.: "[http://www.mozilla.org] [http://fr.wikipedia.org]"
    is rendered as: "<a href="...">[1]</a> <a href="...">[2]</a>
    """

    category_links = []
    """ This will contain the links to the categories of the article. """
    interwiki_links = []
    """ This will contain the links to the foreign versions of the article. """

    for namespace, value in namespaces.iteritems():
        assert value in range(16), "Incorrect value for namespaces"
    """
    Predefined namespaces; source: includes/Defines.php of MediaWiki-1.17.0
    'NS_MAIN', 0
    'NS_TALK', 1
    'NS_USER', 2
    'NS_USER_TALK', 3
    'NS_PROJECT', 4
    'NS_PROJECT_TALK', 5
    'NS_FILE', 6
    'NS_FILE_TALK', 7
    'NS_MEDIAWIKI', 8
    'NS_MEDIAWIKI_TALK', 9
    'NS_TEMPLATE', 10
    'NS_TEMPLATE_TALK', 11
    'NS_HELP', 12
    'NS_HELP_TALK', 13
    'NS_CATEGORY', 14
    'NS_CATEGORY_TALK', 15 
    """

    def balance_tags(tag=None):
        i = 0
        if tag is not None:
            try:
                i = tags_stack.index(tag, -1)
            except ValueError:
                return ''
        result = ''
        while len(tags_stack) > i:
            result += '</%s>' % tags_stack.pop()
        return result

    def content(node):
        return apostrophes.parse('%s' % node.leaf() + balance_tags())

    def render_title1(node):
        node.value = '<h1>' + content(node) +  '</h1>\n'

    def render_title2(node):
        node.value = '<h2>' + content(node) +  '</h2>\n'

    def render_title3(node):
        node.value = '<h3>' + content(node) +  '</h3>\n'

    def render_title4(node):
        node.value = '<h4>' + content(node) +  '</h4>\n'

    def render_title5(node):
        node.value = '<h5>' + content(node) +  '</h5>\n'

    def render_title6(node):
        node.value = '<h6>' + content(node) +  '</h6>\n'

    def render_raw_text(node):
        node.value = "%s" % node.leaf()

    def render_paragraph(node):
        value = content(node)
        if value != '':
            node.value = '<p>' + value +  '</p>\n'

    def render_wikitext(node):
        node.value = content(node)

    def render_body(node):
        metadata = ''
        if category_links != []:
            metadata += '<p>Categories: ' + ', '.join(category_links) + '</p>\n'
        if interwiki_links != []:
            metadata += '<p>Interwiki: ' + ', '.join(interwiki_links) + '</p>\n'
        node.value = '<body>\n' + content(node) + metadata + '</body>'

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

    def process_attribute(node, allowed_tag):
        assert len(node.value) == 2, "Bad AST shape!"
        attribute_name = node.value[0].value
        attribute_value = node.value[1].value
        if attribute_name in allowed_attributes or not allowed_tag:
            return '%s="%s"' % (attribute_name, attribute_value)
        return ''

    def process_attributes(node, allowed_tag):
        result = ''
        if len(node.value) == 1:
            pass
        elif len(node.value) == 2:
            attributes = node.value[1].value
            for i in range(len(attributes)):
                attribute = process_attribute(attributes[i], allowed_tag)
                if attribute is not '':
                    result += ' ' + attribute 
        else:
            raise Exception("Bad AST shape!")
        return result

    def render_attribute(node):
        node.value = process_attribute(node, True)

    def render_tag_open(node):
        tag_name = node.value[0].value
        if tag_name in allowed_autoclose_tags:
            render_tag_autoclose(node)
        elif tag_name in allowed_tags:
            attributes = process_attributes(node, True)
            tags_stack.append(tag_name)
            node.value = '<%s%s>' % (tag_name, attributes) 
        else:
            attributes = process_attributes(node, False)
            node.value = '&lt;%s%s&gt;' % (tag_name, attributes)

    def render_tag_close(node):
        tag_name = node.value[0].value
        if tag_name in allowed_autoclose_tags:
            render_tag_autoclose(node)
        elif tag_name in allowed_tags:
            node.value = balance_tags(tag_name)
        else:
            node.value = "&lt;/%s&gt;" % tag_name

    def render_tag_autoclose(node):
        tag_name = node.value[0].value
        if tag_name in allowed_autoclose_tags:
            attributes = process_attributes(node, True)
            node.value = '<%s%s />' % (tag_name, attributes) 
        else:
            attributes = process_attributes(node, False)
            node.value = '&lt;%s%s /&gt;' % (tag_name, attributes)

    def render_table(node):
        table_parameters = ''
        table_content = ''
        if isinstance(node.value, Nodes) and node.value[0].tag == 'table_begin':
            attributes = node.value[0].value[0]
            for attribute in attributes:
                if attribute.tag == 'HTML_attribute':
                    table_parameters += ' ' + attribute.value
            contents = node.value[1].value
            for item in contents:
                table_content += content(item)
        else:
            table_content = content(node)
        node.value = '<table%s>\n<tr>\n%s</tr>\n</table>\n' % (table_parameters, table_content)

    def render_cell_content(node):
        if isinstance(node.value, Nil):
            return None
        cell_parameters = ''
        cell_content = ''
        if len(node.value) > 1:
            values = node.value[0].value
            for value in values:
                if value.tag == 'HTML_attribute':
                    cell_parameters += ' ' + value.value
                else:
                    cell_content += value.value
            cell_content += content(node.value[1])
        else:
            cell_content = content(node)
        return (cell_parameters, cell_content)

    def render_table_header_cell(node):
        content = render_cell_content(node)
        if content is not None:
            node.value = '\t<th%s>%s</th>\n' % content

    def render_table_normal_cell(node):
        content = render_cell_content(node)
        if content is not None:
            node.value = '\t<td%s>%s</td>\n' % content

    def render_table_empty_cell(node):
        node.value = '\t<td></td>\n'

    def render_table_caption(node):
        content = render_cell_content(node)
        if content is not None:
            node.value = '\t<caption%s>%s</caption>\n' % content

    def render_table_line_break(node):
        line_parameters = ''
        if node.value != '':
            assert len(node.value) == 1, "Bad AST shape!"
            parameters = node.value[0].value
            for value in parameters:
                if value.tag == 'HTML_attribute':
                    line_parameters += ' ' + value.value
        node.value = '</tr>\n<tr%s>\n' % line_parameters

    def render_preformatted(node):
        node.value = '<pre>' + content(node) +  '</pre>\n'

    def render_hr(node):
        node.value = '<hr />\n'

    def render_ul(list):
        result = '<ul>\n'
        for i in range(len(list)):
            result += '\t<li>' + content(list[i]) +  '</li>\n'
        result += '</ul>\n'
        return result

    def render_ol(list):
        result = '<ol>\n'
        for i in range(len(list)):
            result += '\t<li>' + content(list[i]) +  '</li>\n'
        result += '</ol>\n'
        return result

    def render_dd(list):
        result = '<dl>\n'
        for i in range(len(list)):
            result += '\t<dd>' + content(list[i]) +  '</dd>\n'
        result += '</dl>\n'
        return result

    def render_dt(list):
        result = '<dl>\n'
        for i in range(len(list)):
            result += '\t<dt>' + content(list[i]) +  '</dt>\n'
        result += '</dl>\n'
        return result

    def collapse_list(list):
        i = 0
        while i+1 < len(list):
            if list[i].tag == 'bullet_list_leaf' and list[i+1].tag == '@bullet_sub_list@' or \
               list[i].tag == 'number_list_leaf' and list[i+1].tag == '@number_sub_list@' or \
               list[i].tag == 'colon_list_leaf' and list[i+1].tag == '@colon_sub_list@' or \
               list[i].tag == 'semi_colon_list_leaf' and list[i+1].tag == '@semi_colon_sub_list@':
                list[i].value.append(list[i+1].value[0])
                list.pop(i+1)
            else:
                i += 1
        for i in range(len(list)):
            if isinstance(list[i].value, Nodes):
                collapse_list(list[i].value)

    def select_items(nodes, i, value):
        list_tags = ['bullet_list_leaf', 'number_list_leaf', 'colon_list_leaf', 'semi_colon_list_leaf']
        list_tags.remove(value)
        if isinstance(nodes[i].value, Nodes):
            render_lists(nodes[i].value)
        items = [nodes[i]]
        while i + 1 < len(nodes) and nodes[i+1].tag not in list_tags:
            if isinstance(nodes[i+1].value, Nodes):
                render_lists(nodes[i+1].value)
            items.append(nodes.pop(i+1))
        return items

    def render_lists(list):
        i = 0
        while i < len(list):
            if list[i].tag == 'bullet_list_leaf' or list[i].tag == '@bullet_sub_list@':
                list[i].value = render_ul(select_items(list, i, 'bullet_list_leaf'))
            elif list[i].tag == 'number_list_leaf' or list[i].tag == '@number_sub_list@':
                list[i].value = render_ol(select_items(list, i, 'number_list_leaf'))
            elif list[i].tag == 'colon_list_leaf' or list[i].tag == '@colon_sub_list@':
                list[i].value = render_dd(select_items(list, i, 'colon_list_leaf'))
            elif list[i].tag == 'semi_colon_list_leaf' or list[i].tag == '@semi_colon_sub_list@':
                list[i].value = render_dt(select_items(list, i, 'semi_colon_list_leaf'))
            i += 1

    def render_list(node):
        assert isinstance(node.value, Nodes), "Bad AST shape!"
        collapse_list(node.value)
        render_lists(node.value)

    def render_url(node):
        node.value = '<a href="%s">%s</a>' % (node.leaf(), node.leaf())

    def render_external_link(node):
        if len(node.value) == 1:
            external_autonumber.append(node.leaf())
            node.value = '<a href="%s">[%s]</a>' % (node.leaf(), len(external_autonumber))
        else:
            text = node.value[1].leaf()
            node.value = '<a href="%s">%s</a>' % (node.value[0].leaf(), text)

    def render_interwiki(prefix, page):
        link = '<a href="%s">%s</a>' % (interwiki[prefix] + page, page)
        if link not in interwiki_links:
            interwiki_links.append(link)

    def render_category(category_name):
        link = '<a href="%s">%s</a>' % (category_name, category_name)
        if link not in category_links:
            category_links.append(link)

    def render_file(file_name, arguments):
        """ This implements a basic handling of images.
        MediaWiki supports much more parameters (see includes/Parser.php).
        """
        style = ''
        thumbnail = False
        legend = ''
        if arguments != []:
            parameters = arguments[0].value
            for parameter in parameters:
                parameter = '%s' % parameter.leaf()
                if parameter[-2:] == 'px':
                    size = parameter[0:-2]
                    if 'x' in size:
                        size_x, size_y = size.split('x', 1)
                        try:
                            size_x = int(size_x)
                            size_y = int(size_y)
                            style += 'width:%spx;height:%spx' % (size_x, size_y)
                        except:
                            legend = parameter
                    else:
                        try:
                            size_x = int(size)
                            style += 'width:%spx;' % size_x
                        except:
                            legend = parameter
                elif parameter in ['left', 'right', 'center']:
                    style += 'float:%s;' % parameter
                elif parameter in ['thumb', 'thumbnail']:
                    thumbnail = True
                elif parameter == 'border':
                    style += 'border:1px solid grey'
                else:
                    legend = parameter
        result = '<img src="%s" style="%s" alt="" />' % (file_name, style)
        if thumbnail:
            result = '<div class="thumbnail">%s<p>%s</p></div>\n' % (result, legend)
        return result

    def render_internal_link(node):
        force_link = False
        url = ''
        page_name = node.value.pop(0).value
        if page_name[0] == ':':
            force_link = True
            page_name = page_name[1:]
        if ':' in page_name:
            namespace, page_name = page_name.split(':', 1)
            if namespace in interwiki and not force_link:
                render_interwiki(namespace, page_name)
                node.value = ''
                return
            elif namespace in interwiki:
                url = interwiki[namespace]
                namespace = ''
            if namespace in namespaces:
                if namespaces[namespace] == 6 and not force_link:  # File
                    node.value = render_file(page_name, node.value)
                    return
                elif namespaces[namespace] == 14 and not force_link:  # Category
                    render_category(page_name)
                    node.value = ''
                    return
            if namespace:
                page_name = namespace + ':' + page_name
        if len(node.value) == 0:
            text = page_name
        else:
            text = '|'.join('%s' % item.leaf() for item in node.value[0])
        node.value = '<a href="%s%s">%s</a>' % (url, page_name, text)

    return locals()

def make_parser(allowed_tags=[], allowed_autoclose_tags=[], allowed_attributes=[], interwiki={}, namespaces={}):
    """Constructs the parser for the HTML backend.
    
    :arg allowed_tags: List of the HTML tags that should be allowed in the parsed wikitext.
            Opening tags will be closed. Closing tags with no opening tag will be removed.
            All the tags that are not in the list will be output as &lt;tag&gt;.
    :arg allowed_autoclose_tags: List of the self-closing tags that should be allowed in the
            parsed wikitext. All the other self-closing tags will be output as &lt;tag /&gt;
    :arg allowed_attributes: List of the HTML attributes that should be allowed in the parsed
            tags (e.g.: class="", style=""). All the other attributes (e.g.: onclick="") will
            be removed.
    :arg interwiki: List of the allowed interwiki prefixes (en, fr, es, commons, etc.)
    :arg namespaces: List of the namespaces of the wiki (File, Category, Template, etc.),
            including the localized version of those strings (Modele, Categorie, etc.),
            associated to the corresponding namespace code.
    """
    tools = toolset(allowed_tags, allowed_autoclose_tags, allowed_attributes, interwiki, namespaces)
    return wikitextParser.make_parser(tools)
