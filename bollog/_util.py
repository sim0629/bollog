from __future__ import unicode_literals

import html5lib
import lxml.html

from ._compat import urlopen

_parser = html5lib.HTMLParser(
    tree=html5lib.treebuilders.getTreeBuilder('lxml'),
    namespaceHTMLElements=False)

def fetch_tree(url, encoding='utf-8'):
    html = urlopen(url).read()
    return _parser.parse(html, encoding=encoding)


def tree_to_string(tree):
    return lxml.html.tostring(tree, encoding='utf-8').decode('utf-8')


def merge_list(*list_of_list):
    yielded = set()
    for list_ in list_of_list:
        for entry in list_:
            if entry not in yielded:
                yielded.add(entry)
                yield entry
