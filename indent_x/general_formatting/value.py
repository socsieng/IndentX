#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of IndentX.
# https://github.com/socsieng/IndentX

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

import re

from indent_x.general_formatting.collection import Collection
from indent_x.general_formatting.document import Document
from indent_x.general_formatting.string_utility import unwrap_quotes, is_string_value

class Value:
    def __init__(self, value, comments = None):
        self._original_value = value

        if isinstance(value, Collection):
            self.value_type = 'array'
            self.value = value
        elif isinstance(value, Document):
            self.value_type = 'object'
            self.value = value
        else:
            if is_string_value(value):
                self.value_type = 'string'
                self.value = unwrap_quotes(value)
            else:
                if value == 'true' or value == 'false':
                    self.value_type = 'boolean'
                elif re.compile('^-?\\d*\\.{0,1}\\d+$').match(value):
                    self.value_type = 'number'
                else:
                    self.value_type = 'unknown'

                self.value = value

        self.comments = comments if comments else []
