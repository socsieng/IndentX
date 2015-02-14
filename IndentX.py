import sublime
import sublime_plugin
import re

class XmlIndentFormater(object):
    position = 0
    depth = 0
    prevDepth = 0
    add = False
    beforeString = '\n'
    openExp = re.compile(r'<(?![/?!])[^>]+(?<!/)>')
    closeExp = re.compile(r'</[^>]+>')
    selfClosingExp = re.compile(r'<[^>]+/>')
    openCommentExp = re.compile(r'<!--')
    closeCommentExp = re.compile(r'-->')
    expressions = [openExp, closeExp, openCommentExp, closeCommentExp, selfClosingExp]
    trimExp = re.compile(r'(^\s*|\s*$)')

    def __init__(self, indentString = '\t'):
        self.indentString = indentString

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

        while True:
            m = self.getFirstMatch(xml, pos)
            if m:
                match = self.trimExp.sub('', m.group(0))
                pre = self.trimExp.sub('', xml[pos:m.start()])
                pos = m.end()

                if m.re == self.openExp:
                    output += pre + self.beforeString + (self.indentString * self.depth) + match
                    self.depth += 1
                    self.add = True

                elif m.re == self.closeExp:
                    if self.depth == self.prevDepth and self.add:
                        #close on new line
                        output += pre + match
                        self.depth -= 1
                    else:
                        self.depth -= 1
                        output += pre + self.beforeString + (self.indentString * self.depth) + match

                    self.add = False

                elif m.re == self.openCommentExp:
                    output += pre + self.beforeString + (self.indentString * self.depth) + match
                    self.add = True

                elif m.re == self.closeCommentExp:
                    output += pre + match
                    self.add = True

                else:
                    output += pre + self.beforeString + (self.indentString * self.depth) + match
                    self.add = False

                self.prevDepth = self.depth
            else:
                output += xml[pos:]
                break

        blank = re.compile(r'^\s*$\r?\n', re.M)
        return blank.sub('', output)

class BasicIndentTagsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        regions = self.view.sel()
        indentString = '\t'

        if self.view.settings().get('translate_tabs_to_spaces'):
            indentString = ' ' * self.view.settings().get('tab_size')

        if (len(regions) == 0 or regions[0].empty()):
            size = self.view.size()
            region = sublime.Region(0, size)
            regions = [region]

        for selection in regions:
            formatter = XmlIndentFormater(indentString)
            text = self.view.substr(selection)
            formattedText = formatter.indent(text)
            self.view.replace(edit, selection, formattedText)
