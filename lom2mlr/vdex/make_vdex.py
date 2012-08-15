#!/usr/bin/python

import sys
import re

TRE = re.compile('^T[0-9]+$')

if __name__ == '__main__':
    fname = sys.argv[1]
    vocname = fname.rsplit('.', 1)[0]
    lines = open(fname).readlines()
    langs = lines.pop(0).split()
    hasdef = True
    if langs[0] == 'nodef':
        hasdef = False
        langs.pop(0)
    print """<?xml version="1.0" encoding="utf-8"?>
<vdex:vdex xmlns:vdex="http://www.imsglobal.org/xsd/imsvdex_v1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xs="http://www.w3.org/2001/XMLSchema" xsi:schemaLocation="http://www.imsglobal.org/xsd/imsvdex_v1p0 http://www.imsglobal.org/xsd/imsvdex_v1p0.xsd" xs:version="0.2">
  <vdex:vocabIdentifier isRegistered="false">%s</vdex:vocabIdentifier>""" % (vocname)
    while lines:
        caps = {}
        defs = {}
        id = lines.pop(0).strip()
        if not TRE.match(id):
            sys.stderr.write("error, not TXXX:" + id)
            break
        for lang in langs:
            l = lines.pop(0).strip()
            if TRE.match(l):
                sys.stderr.write("error, TXXX %s while expecting cap of %s" % (l, lang))
                break
            caps[lang] = l
            if hasdef:
                l = lines.pop(0).strip()
                if TRE.match(l):
                    sys.stderr.write("error, TXXX %s while expecting def of %s" % (l, lang))
                    break
                defs[lang] = l
        print """  <vdex:term>
    <vdex:termIdentifier>%s</vdex:termIdentifier>
    <vdex:caption>""" % (id,)
        for lang in langs:
            if caps[lang]:
                print "        <vdex:langstring language=\"%s\">%s</vdex:langstring>" % (lang, caps[lang])
        print "    </vdex:caption>"
        if [x for x in defs.itervalues() if x]:
            print "    <vdex:description>"
            for lang in langs:
                if defs[lang]:
                    print "        <vdex:langstring language=\"%s\">%s</vdex:langstring>" % (lang, defs[lang])
            print "    </vdex:description>"
        print "  </vdex:term>"""
    print "</vdex:vdex>"