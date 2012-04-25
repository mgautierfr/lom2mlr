import re
import unittest
import sys

import markdown

from graph_comparison import GraphTester
from util import splitcode

HEADER_R = re.compile(r'^h[1-9]$', re.I)

graphtester = GraphTester()

def t_function(code, title):
    print code
    assert len(code) in range(2, 4), "%d sections of code" % (len(code),)
    if len(code) == 2:
        code.append(('N3',''))
    assert [t.lower() for t, c in code] == ['xml','n3','n3']
    code = [c for t, c in code]
    obtained_graph, errors = graphtester.test_lom(*code)
    assert not errors, title+' '+`errors`

def test_document():
    m = markdown.Markdown()
    data = open('documentation.md').read().decode('utf-8')
    root = m.parser.parseDocument(data.split('\n')).getroot()
    code = []
    for element in root.getiterator():
        if HEADER_R.match(element.tag):
            if code:
                yield t_function, code, title
                code = []
            title = element.text
        if element.tag == 'pre':
            sub = list(element)
            assert len(sub) == 1 and sub[0].tag == 'code'
            code.append(splitcode(sub[0].text))
    if code:
        yield t_function, code, title

