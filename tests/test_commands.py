#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of py-json-reader.
# https://github.com/socsieng/py-json-reader

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

from preggy import expect

from test_util import fs_test
from tests.base import TestCase
from mock import Mock
import commands

def mock_sublime(region = None):
    sublime = Mock()
    sublime.Region = Mock(return_value = region)
    return sublime

def mock_sublime_view(regions = None, substr = lambda sel: None):
    view = Mock()
    view.settings = Mock(return_value = {
        'tab_size': 4
    })

    view.sel = Mock(return_value = regions)
    view.substr = substr
    view.replace = Mock()
    return view

def mock_regions(contents):
    sublime_regions = []
    if contents:
        for str_value in contents:
            region = Mock(return_value = str_value)
            region.empty = lambda: len(str_value) == 0
            sublime_regions.append(region)

    return sublime_regions

def mock_sublime_edit():
    edit = Mock()
    return edit

class IndentCommandTestCase(TestCase):
    def test_should_invoke_command_with_no_regions(self):
        region = mock_regions(['{ }'])[0]
        sublime = mock_sublime(region)
        view = mock_sublime_view([], lambda sel: sel())
        edit = mock_sublime_edit()

        command = commands.IndentCommand(view, sublime)
        command.run(edit)

        view.replace.assert_called_once_with(edit, region, '{}')

    def test_should_invoke_command_with_multiple_regions(self):
        regions = mock_regions([ '{ }', '[ ]' ])
        sublime = mock_sublime()
        view = mock_sublime_view(regions, lambda sel: sel())
        edit = mock_sublime_edit()

        command = commands.IndentCommand(view, sublime)
        command.run(edit)

        expect(view.replace.call_count).to_equal(2)
        view.replace.assert_any_call(edit, regions[0], '{}')
        view.replace.assert_any_call(edit, regions[1], '[]')

class FormatJsonCommandTestCase(TestCase):
    def test_should_invoke_command_with_no_regions(self):
        region = mock_regions(['{ }'])[0]
        sublime = mock_sublime(region)
        view = mock_sublime_view([], lambda sel: sel())
        edit = mock_sublime_edit()

        command = commands.FormatJsonCommand(view, sublime)
        command.run(edit)

        view.replace.assert_called_once_with(edit, region, '{}')

    def test_should_invoke_command_with_multiple_regions(self):
        regions = mock_regions([ '{ hello: "world" }', '[ ]' ])
        sublime = mock_sublime()
        view = mock_sublime_view(regions, lambda sel: sel())
        edit = mock_sublime_edit()

        command = commands.FormatJsonCommand(view, sublime)
        command.run(edit)

        expect(view.replace.call_count).to_equal(2)
        view.replace.assert_any_call(edit, regions[0], '{\n\t"hello": "world"\n}')
        view.replace.assert_any_call(edit, regions[1], '[]')

    def test_should_invoke_command_with_spaces(self):
        region = mock_regions(['{ hello: "world" }'])[0]
        sublime = mock_sublime(region)
        view = mock_sublime_view([], lambda sel: sel())
        view.settings()['translate_tabs_to_spaces'] = True
        edit = mock_sublime_edit()

        command = commands.FormatJsonCommand(view, sublime)
        command.run(edit)

        view.replace.assert_called_once_with(edit, region, '{\n    "hello": "world"\n}')

class FormatYamlCommandTestCase(TestCase):
    def test_should_invoke_command_with_no_regions(self):
        region = mock_regions(['{ }'])[0]
        sublime = mock_sublime(region)
        view = mock_sublime_view([], lambda sel: sel())
        edit = mock_sublime_edit()

        command = commands.FormatYamlCommand(view, sublime)
        command.run(edit)

        view.replace.assert_called_once_with(edit, region, '')

    def test_should_invoke_command_with_multiple_regions(self):
        regions = mock_regions([ '{ }', '[ ]', '[1,2]' ])
        sublime = mock_sublime()
        view = mock_sublime_view(regions, lambda sel: sel())
        edit = mock_sublime_edit()

        command = commands.FormatYamlCommand(view, sublime)
        command.run(edit)

        expect(view.replace.call_count).to_equal(3)
        view.replace.assert_any_call(edit, regions[0], '')
        view.replace.assert_any_call(edit, regions[1], '')
        view.replace.assert_any_call(edit, regions[2], '- 1\n- 2')
