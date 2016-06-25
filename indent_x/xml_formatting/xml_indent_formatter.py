#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of IndentX.
# https://github.com/socsieng/IndentX

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

import re
from indent_x.general_formatting.string_utility import join

comment_exp = re.compile(r'<!--([\s\S]*?)-->', re.M)
preserve_indent_exp = re.compile('^(.*)$', re.M)

class XmlIndentFormatter(object):
    position = 0
    depth = 0
    prevDepth = 0
    add = False
    beforeString = '\n'
    openExp = re.compile(r'<(?![/?!])[^>]+(?<!/)>')
    closeExp = re.compile(r'</[^>]+>')
    selfClosingExp = re.compile(r'<[^>]+/>')
    expressions = [openExp, closeExp, selfClosingExp, comment_exp]
    openExpSpace = re.compile(r'\s+')
    trimExp = re.compile(r'(^\s*|\s*$)')

    def __init__(self, indentString = '\t', removeComments = False, removeEmptyLines = False):
        self.indentString = indentString
        self.removeComments = removeComments
        self.removeEmptyLines = removeEmptyLines

    def getFirstMatch(self, string, startPos):
        pos = len(string)
        m = None

        for exp in self.expressions:
            match = exp.search(string, startPos)

            if match:
                if match.start() < pos:
                    pos = match.start();
                    m = match

        return m

    def indent(self, xml):
        output = ''
        pos = 0
        m = None
        e = None
        newline = self.beforeString

        if self.indentString == '':
            newline = ''

        while True:
            m = self.getFirstMatch(xml, pos)
            if m:
                match = self.trimExp.sub('', m.group(0))
                pre = self.trimExp.sub('', xml[pos:m.start()])
                pos = m.end()

                if m.re == self.openExp:
                    output = join(newline, output + pre, (self.indentString * self.depth) + self.openExpSpace.sub(' ', match))
                    self.depth += 1
                    self.add = True

                elif m.re == self.closeExp:
                    if self.depth == self.prevDepth and self.add:
                        #close on new line
                        output += pre + match
                        self.depth -= 1
                    else:
                        self.depth -= 1
                        output = join(newline, output + pre, (self.indentString * self.depth) + match)

                    self.add = False

                elif m.re == comment_exp:
                    if self.removeComments:
                        continue
                    output = join(newline, output + pre, format_comment(m.group(0), self.indentString * self.depth))
                    self.add = False

                else:
                    output = join(newline, output + pre, (self.indentString * self.depth) + match)
                    self.add = False

                self.prevDepth = self.depth
            else:
                output += xml[pos:]
                break

        if self.removeEmptyLines:
            blank = re.compile(r'^\s*$\r?\n', re.M)
            return blank.sub('', output)

        return output

def format_comment(comment, indent):
    match = comment_exp.search(comment)

    if match:
        output = preserve_indent_exp.sub(indent + '\\1', match.group(0))

        return output

    return comment
