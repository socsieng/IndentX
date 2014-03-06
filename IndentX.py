import sublime
import sublime_plugin
import re

class BasicIndentTagsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        regions = self.view.sel()

        if len(regions) > 1 or not regions[0].empty():
            for selection in regions:
                selected_text = self.view.substr(selection)
                indented_content = indent_xml(selected_text, '    ', 0)
                self.view.replace(edit, selection, indented_content)
        else:
            size = self.view.size()
            doc_region = sublime.Region(0, size)
            doc_text = self.view.substr(doc_region).strip()
            indented_content = indent_xml(doc_text, '    ', 0)
            self.view.replace(edit, doc_region, indented_content)


def repeat_string(string, count):
    output = ''
    for x in range(count):
        output += string
    return output

def indent_xml(xml, indent, initialDepth):
    depth = 0
    prev = 0
    add = False
    indent = '    '
    tag = re.compile(r'\s*(<[!/]?[^>]+>)\s*')
    comment = re.compile(r'^<!--')
    close = re.compile(r'\s*<\/')
    self_close = re.compile(r'\/>')
    nl = '\n'

    def replace_with_indent(match):
        nonlocal nl, depth, prev, add, indent, tag, comment, close, self_close
        output = ''
        p = match.group(0)

        if close.search(p):
            if depth == prev and add:
                output += p
                depth -= 1
            else:
                depth -= 1
                output += nl + repeat_string(indent, depth) + p
            add = False
        elif self_close.search(p):
            output += nl + repeat_string(indent, depth) + p
            add = False
        elif comment.search(p):
            output += nl + repeat_string(indent, depth) + p
        else:
            output += nl + repeat_string(indent, depth) + p
            depth += 1
            add = True

        prev = depth
        return output

    if depth != 0:
        print('Unmatched tags exist')

    indented = tag.sub(replace_with_indent, xml)
    blank = re.compile(r'^\s*$\r?\n', re.M)
    return blank.sub('', indented)
