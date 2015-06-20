#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of IndentX.
# https://github.com/socsieng/IndentX

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

import os
import sys
import sublime
import sublime_plugin

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from general_formatting.general_formatter import GeneralFormatter
from general_formatting import document_builder
from json_formatting import JsonReader
from json_formatting import JsonFormatter
from json_formatting import JsonDocumentRenderer
from yaml_formatting import YamlDocumentRenderer

class BasicIndentCommand(sublime_plugin.TextCommand):
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
            formatter = GeneralFormatter()
            text = self.view.substr(selection)
            formattedText = formatter.format(text, indentString)
            self.view.replace(edit, selection, formattedText)

class JsonIndentFormatCommand(sublime_plugin.TextCommand):
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
            text = self.view.substr(selection)
            reader = JsonReader(text)
            formatter = JsonFormatter(reader, {'force_property_quotes': True, 'quote_char': '"', 'normalize_strings': True, 'indent_character': indentString})
            formattedText = formatter.format()
            if formattedText:
                self.view.replace(edit, selection, formattedText)

class JsonToYamlCommand(sublime_plugin.TextCommand):
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
            text = self.view.substr(selection)
            reader = JsonReader(text)
            document = document_builder.build(reader)
            renderer = YamlDocumentRenderer(document, {'indent_character': indentString})
            formattedText = renderer.render()
            if formattedText:
                self.view.replace(edit, selection, formattedText)
