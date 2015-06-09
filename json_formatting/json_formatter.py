#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of IndentX.
# https://github.com/socsieng/IndentX

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

import re
import copy

from json_formatting.json_reader_value import *
from json_formatting.string_reader import *

def is_string_value(input_string):
    char = input_string[0]
    return char == '\'' or char == '"'

def ensure_quotes(input_string, quote_char = '"'):
    other_char = '\'' if quote_char == '"' else '"'
    esc_quote_exp = re.compile('(' + quote_char + ')')
    unesc_quote_exp = re.compile('(\\\\' + other_char + ')')
    wrap_exp = re.compile('^["\']?(.+?)["\']?$')

    def quote_replacer(match):
        inner = match.group(1)
        inner = unesc_quote_exp.sub(other_char, inner)
        inner = esc_quote_exp.sub('\\\\\\1', inner)
        return quote_char + inner + quote_char

    output = wrap_exp.sub(quote_replacer, input_string)

    return output
    
class JsonFormatter:
    default_options = {
        'indent_character': '  ',
        'quote_char': '"',
        'normalize_strings': False
    }

    def __init__(self, json_reader, options = None):
        self._reader = json_reader
        self._options = copy.deepcopy(self.default_options)

        if options:
            self._options.update(options)

    def format(self):
        output = ''
        indent = 0
        reader = self._reader
        has_properties = False

        while True:
            should_linebreak = False
            result = reader.read()

            if not result:
                break

            if result.type == 'begin_object':
                has_properties = False
                indent += 1
            elif result.type == 'end_object':
                indent -= 1
                if has_properties:
                    should_linebreak = True
            elif result.type == 'property':
                should_linebreak = True
                has_properties = True


            # new line
            if should_linebreak:
                if len(output) > 0 and output[len(output) - 1] == ' ':
                    output = output[:len(output) - 1]
                output += '\n' + indent * self._options['indent_character']


            # actual character
            if result.type == 'property' and 'force_property_quotes' in self._options and self._options['force_property_quotes']:
                output += ensure_quotes(result.value, self._options['quote_char'])
            elif result.type == 'value' and 'normalize_strings' in self._options and self._options['normalize_strings'] and is_string_value(result.value):
                output += ensure_quotes(result.value, self._options['quote_char'])
            else:
                output += result.value


            # suffix
            if result.type == 'property_separator':
                output += ' '
            elif result.type == 'value_separator':
                output += ' '

        return output
