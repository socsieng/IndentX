#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of IndentX.
# https://github.com/socsieng/IndentX

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

import re

from json_formatting import JsonFormatter
from json_formatting import JsonReader
from xml_formatting import XmlIndentFormatter

first_char_exp = re.compile('\s*([^\s])')

class GeneralFormatter:
    def format(self, text, indent_char = '\t'):
        if text:
            match = first_char_exp.search(text)

            if match:
                first_char = match.group(1)

                if first_char == '<':
                    formatter = XmlIndentFormatter(indent_char)
                    return formatter.indent(text)
                else:
                    formatter = JsonFormatter(JsonReader(text), {'indent_character': indent_char})
                    return formatter.format()
