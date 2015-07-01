#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of IndentX.
# https://github.com/socsieng/IndentX

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

import re

from indent_x.json_formatting.json_reader_value import *
from indent_x.json_formatting.string_reader import *

property_exp = re.compile('\\s*:')

class JsonReader:
    tokens = [
        ['begin_object', re.compile('\\{')],
        ['end_object', re.compile('\\}')],
        ['begin_array', re.compile('\\[')],
        ['end_array', re.compile('\\]')],
        ['property_separator', re.compile(':')],
        ['value_separator', re.compile(',')],
        ['new_line_comment', re.compile('^\\s*//.+$', re.M)],
        ['end_line_comment', re.compile('//.+$', re.M)],
        ['new_line_comment_block', re.compile('^\\s*/\\*[\\s\\S]*?\\*/', re.M)],
        ['in_line_comment_block', re.compile('/\\*[\\s\\S]*?\\*/', re.M)],
        ['string', re.compile('".*?((?<!\\\\)|(?<=\\\\\\\\))"', re.M)],
        ['string', re.compile('\'.*?((?<!\\\\)|(?<=\\\\\\\\))\'', re.M)],
        ['property', re.compile('[\'"\\w_\\-+.*]+(?=\\s*:)')],
        ['value', re.compile('([\'"\\w_\\-+.*][\'"\\w_\\-+.* \\t()]*)(?!\\s*:)(?=[\\n,]?)')]
    ]

    def __init__(self, json):
        self._json = json
        self._position = 0
        self._current_match = None
        self._value = None

    def peek(self):
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
            self._peek_position = min_match.end()
            value = min_match.group(0)
            token_type = min_token[0]

            if token_type == 'string':
                prop_sep = property_exp.match(self._json, min_match.end())
                if prop_sep:
                    token_type = 'property'
                else:
                    token_type = 'value'
            elif token_type == 'property' or token_type == 'value':
                sr = StringReader(self._json, min_match.start())
                string_value = sr.read()

                if string_value:
                    value = string_value.strip()
                    self._peek_position = min_match.start() + len(value)

            if value:
                value = value.strip()

            self._value = JsonReaderValue(token_type, value)

            return self._value

        return None

    def read(self):
        result = self.peek()
        self._position = self._peek_position
        return result

    def move(self):
        self._position = self._peek_position
