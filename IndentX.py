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
import imp

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

reloader_name = 'package_util.reloader'
if reloader_name in sys.modules:
    imp.reload(sys.modules[reloader_name])
else:
    import package_util.reloader

import commands

class BasicIndentCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        sublime_plugin.TextCommand.__init__(self, view)
        self.command = commands.IndentCommand(self.view, sublime)

    def is_enabled(self):
        return self.command.is_enabled()

    def run(self, edit):
        self.command.run(edit)

class JsonIndentFormatCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        sublime_plugin.TextCommand.__init__(self, view)
        self.command = commands.FormatJsonCommand(self.view, sublime)

    def is_enabled(self):
        return self.command.is_enabled()

    def run(self, edit):
        self.command.run(edit)

class JsonToYamlCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        sublime_plugin.TextCommand.__init__(self, view)
        self.command = commands.FormatYamlCommand(self.view, sublime)

    def is_enabled(self):
        return self.command.is_enabled()

    def run(self, edit):
        self.command.run(edit)

class BasicUnindentCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        sublime_plugin.TextCommand.__init__(self, view)
        self.command = commands.UnindentCommand(self.view, sublime)

    def is_enabled(self):
        return self.command.is_enabled()

    def run(self, edit):
        self.command.run(edit)

class ReportIssueCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        sublime_plugin.TextCommand.__init__(self, view)
        self.command = commands.ReportIssueCommand(self.view, os, sys)

    def is_enabled(self):
        return self.command.is_enabled()

    def run(self, edit):
        self.command.run(edit)
