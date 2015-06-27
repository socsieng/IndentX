#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of IndentX.
# https://github.com/socsieng/IndentX

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

from commands.format_command_base import FormatCommandBase
from json_formatting import JsonReader
from json_formatting import JsonFormatter
from json_formatting import JsonDocumentRenderer

class FormatJsonCommand(FormatCommandBase):
    def __init__(self, view, sublime):
        FormatCommandBase.__init__(self, view, sublime)

    def format(self, text, options):
        reader = JsonReader(text)
        formatter = JsonFormatter(reader, {'force_property_quotes': True, 'quote_char': '"', 'normalize_strings': True, 'indent_character': options['indent_character']})
        formattedText = formatter.format()
        return formattedText
