#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of IndentX.
# https://github.com/socsieng/IndentX

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

class FormatCommandBase:
    def __init__(self, view, sublime):
        self.view = view
        self.sublime = sublime

    def format(self, text, options):
        return None

    def run(self, edit):
        regions = self.view.sel()
        indentString = '\t'

        if self.view.settings().get('translate_tabs_to_spaces'):
            indentString = ' ' * self.view.settings().get('tab_size')

        if (len(regions) == 0 or regions[0].empty()):
            size = self.view.size()
            region = self.sublime.Region(0, size)
            regions = [region]

        for selection in regions:
            text = self.view.substr(selection)
            formattedText = self.format(text, { 'indent_character': indentString })
            self.view.replace(edit, selection, formattedText)
