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
    class Section:
        depth = 0
        prev = 0
        add = False
        indent = '    '
        tag = re.compile(r'\s*(<[!/]?[^>]+>)\s*')
        nl = '\n'
        comment = re.compile(r'^<!--')
        close = re.compile(r'\s*<\/')
        self_close = re.compile(r'\/>')

    section = Section()

    def replace_with_indent(match):
        output = ''
        p = match.group(0)

        if section.close.search(p):
            if section.depth == section.prev and section.add:
                output += p
                section.depth -= 1
            else:
                section.depth -= 1
                output += section.nl + repeat_string(section.indent, section.depth) + p
            section.add = False
        elif section.self_close.search(p):
            output += section.nl + repeat_string(section.indent, section.depth) + p
            section.add = False
        elif section.comment.search(p):
            output += section.nl + repeat_string(section.indent, section.depth) + p
        else:
            output += section.nl + repeat_string(section.indent, section.depth) + p
            section.depth += 1
            section.add = True

        section.prev = section.depth
        return output

    if section.depth != 0:
        print('Unmatched tags exist')

    indented = section.tag.sub(replace_with_indent, xml)
    blank = re.compile(r'^\s*$\r?\n', re.M)
    return blank.sub('', indented)
