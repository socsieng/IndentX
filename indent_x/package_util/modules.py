#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of IndentX.
# https://github.com/socsieng/IndentX

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

module_order = [
    'indent_x.general_formatting.document',
    'indent_x.general_formatting.collection',
    'indent_x.general_formatting.comment',
    'indent_x.general_formatting.property',
    'indent_x.general_formatting.string_utility',
    'indent_x.general_formatting.property_name',
    'indent_x.general_formatting.value',

    'indent_x.json_formatting.json_reader_value',
    'indent_x.json_formatting.string_reader',
    'indent_x.json_formatting.json_reader',
    'indent_x.json_formatting.json_formatter',
    'indent_x.json_formatting.json_document_renderer',

    'indent_x.xml_formatting.xml_indent_formatter',
    'indent_x.general_formatting.general_formatter',

    'indent_x.general_formatting.document_builder',
    'indent_x.yaml_formatting.yaml_document_renderer',

    'indent_x.commands.format_command_base',
    'indent_x.commands.indent_command',
    'indent_x.commands.format_json_command',
    'indent_x.commands.format_yaml_command',
    'indent_x.commands.report_issue_command',
    'indent_x.commands.unindent_command'
]
