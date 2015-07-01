#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of IndentX.
# https://github.com/socsieng/IndentX

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

from indent_x.commands.format_command_base import FormatCommandBase
from indent_x.json_formatting import JsonReader
from indent_x.json_formatting import JsonFormatter
from indent_x.json_formatting import JsonDocumentRenderer

class FormatJsonCommand(FormatCommandBase):
    def __init__(self, view, sublime):
        FormatCommandBase.__init__(self, view, sublime)
        self.command_name = 'Indent & Format JSON'

    def format(self, text, options):
        reader = JsonReader(text)
        formatter = JsonFormatter(reader, {'force_property_quotes': True, 'quote_char': '"', 'normalize_strings': True, 'indent_character': options['indent_character']})
        formattedText = formatter.format()

        self.view.set_syntax_file('Packages/JavaScript/JSON.tmLanguage')

        return formattedText
