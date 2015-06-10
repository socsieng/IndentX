#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of IndentX.
# https://github.com/socsieng/IndentX

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

import re

class StringReader:
    tokens = ['"', '\'']

    def __init__(self, value, position = 0):
        self._value = value
        self._original_position = position
        self._position = position

    def read(self):
        start = self._original_position
        position = self._original_position

        if self._value:
            char = self._value[position]

            if char == '"' or char == '\'':
                position += 1

                while True:
                    end = self._find_first_token([char, '\\\\' + char, '$'], position)

                    if end:
                        position = end.end()
                        if len(end.group(0)) == 0 or end.group(0)[0] != '\\':
                            break

                result = self._value[start:position]

                return result

        return None

    def _find_first_token(self, tokens, start):
        search = self._value
        min_match = None

        for token in tokens:
            exp = re.compile(token, re.M)
            match = exp.search(search, start)

            if match:
                if not min_match:
                    min_match = match
                elif match.start() < min_match.start():
                    min_match = match

        return min_match
