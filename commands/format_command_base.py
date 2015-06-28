#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of IndentX.
# https://github.com/socsieng/IndentX

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

import os

class FormatCommandBase:
    def __init__(self, view, sublime):
        self.view = view
        self.sublime = sublime
        self.command_name = ''

    def format(self, text, options):
        return None

    def run(self, edit):
        regions = self.view.sel()
        indentString = '\t'
        settings = self.view.settings()

        settings.set('indent_x_last_command', self.command_name)

        if settings.get('translate_tabs_to_spaces'):
            indentString = ' ' * settings.get('tab_size')

        if (len(regions) == 0 or regions[0].empty()):
            size = self.view.size()
            region = self.sublime.Region(0, size)
            regions = [region]

        for selection in regions:
            text = self.view.substr(selection)
            formattedText = self.format(text, { 'indent_character': indentString })
            self.view.replace(edit, selection, formattedText)

    def is_enabled(self):
        return True

    def get_language(self):
        syntax_file = self.view.settings().get('syntax')
        language = os.path.basename(syntax_file).replace('.tmLanguage', '').lower() if syntax_file != None else "plain text"
        return language
