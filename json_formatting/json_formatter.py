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
from general_formatting.string_utility import is_string_value, ensure_quotes
    
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
        is_last_token_comment = False

        while True:
            should_linebreak = False
            result = reader.read()

            if not result:
                break

            if is_last_token_comment:
                should_linebreak = True
                is_last_token_comment = False

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
            elif result.type == 'new_line_comment':
                is_last_token_comment = True
                should_linebreak = True
            elif result.type == 'end_line_comment':
                is_last_token_comment = True
            elif result.type == 'new_line_comment_block':
                should_linebreak = True


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
            elif result.type == 'end_line_comment' or result.type == 'in_line_comment_block':
                if len(output) > 0 and output[len(output) - 1] == ' ':
                    output = output[:len(output) - 1]
                output += ' ' + result.value
            else:
                output += result.value


            # suffix
            if result.type == 'property_separator':
                output += ' '
            elif result.type == 'value_separator':
                output += ' '
            elif result.type == 'new_line_comment_block':
                output += ' '

        return output
