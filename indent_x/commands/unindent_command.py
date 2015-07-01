#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of IndentX.
# https://github.com/socsieng/IndentX

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

from indent_x.commands.format_command_base import FormatCommandBase
from indent_x.general_formatting.general_formatter import GeneralFormatter
from indent_x.general_formatting import document_builder

class UnindentCommand(FormatCommandBase):
    def __init__(self, view, sublime):
        FormatCommandBase.__init__(self, view, sublime)
        self.command_name = 'Unindent'

    def format(self, text, options):
        formatter = GeneralFormatter()
        formattedText = formatter.unindent(text)
        return formattedText
