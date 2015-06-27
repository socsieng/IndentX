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

import commands

class BasicIndentCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        command = commands.IndentCommand(self.view, sublime)
        command.run(edit)

class JsonIndentFormatCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        command = commands.FormatJsonCommand(self.view, sublime)
        command.run(edit)

class JsonToYamlCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        command = commands.FormatYamlCommand(self.view, sublime)
        command.run(edit)
