#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of IndentX.
# https://github.com/socsieng/IndentX

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

from commands.format_command_base import FormatCommandBase
from general_formatting.general_formatter import GeneralFormatter
from general_formatting import document_builder

class IndentCommand(FormatCommandBase):
    def __init__(self, view, sublime):
        FormatCommandBase.__init__(self, view, sublime)

    def format(self, text, options):
        formatter = GeneralFormatter()
        formattedText = formatter.format(text, options['indent_character'])
        return formattedText
