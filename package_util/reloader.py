#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of IndentX.
# https://github.com/socsieng/IndentX

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

import sys
import imp

mods_load_order = [
    'general_formatting.document',
    'general_formatting.collection',
    'general_formatting.comment',
    'general_formatting.property',
    'general_formatting.string_utility',
    'general_formatting.property_name',
    'general_formatting.value',

    'json_formatting.json_reader_value',
    'json_formatting.string_reader',
    'json_formatting.json_reader',
    'json_formatting.json_formatter',
    'json_formatting.json_document_renderer',

    'xml_formatting.xml_indent_formatter',
    'general_formatting.general_formatter',

    'general_formatting.document_builder',
    'yaml_formatting.yaml_document_renderer',

    'commands.format_command_base',
    'commands.indent_command',
    'commands.format_json_command',
    'commands.format_yaml_command',
    'commands.report_issue_command',
    'commands.unindent_command'
]

for mod in mods_load_order:
    if mod in sys.modules:
        try:
            print('reloading: %s' % mod)
            imp.reload(sys.modules[mod])
        except ImportError:
            pass
