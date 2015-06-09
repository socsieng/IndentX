#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of IndentX.
# https://github.com/socsieng/IndentX

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

import re

from json_formatting.json_reader_value import *
from json_formatting.string_reader import *

class JsonReader:
    tokens = [
        ['begin_object', re.compile('\\{')],
        ['end_object', re.compile('\\}')],
        ['begin_array', re.compile('\\[')],
        ['end_array', re.compile('\\]')],
        ['property_separator', re.compile(':')],
        ['value_separator', re.compile(',')],
        ['literal', re.compile('[\'"\\w_\\-+.]+')]
    ]

    def __init__(self, json):
        self._json = json
        self._position = 0
        self._current_match = None
        self._value = None

    def read(self):
        min_index = len(self._json)
        min_match = None
        min_token = None

        for t in self.tokens:
            match = t[1].search(self._json, self._position)

            if match:
                if match.start() < min_index:
                    min_match = match
                    min_index = match.start()
                    min_token = t

        if min_match and min_token:
            self._current_match = min_match
            self._position = min_match.end()
            value = min_match.group(0)
            token_type = min_token[0]

            if token_type == 'literal':
                sr = StringReader(self._json, min_match.start())
                string_value = sr.read()

                if string_value:
                    value = string_value
                    self._position = min_match.start() + len(string_value)

                prop_sep = re.compile('\\s*:').search(self._json, self._position)

                if prop_sep and prop_sep.start() == self._position:
                    token_type = 'property'
                else:
                    token_type = 'value'

            self._value = JsonReaderValue(token_type, value)

            return self._value

        return None
