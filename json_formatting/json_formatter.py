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
from general_formatting.string_utility import is_string_value, ensure_quotes, join, strip_trailing

block_comment_exp = re.compile('(/\\*)(\\s*[\\s\\S]*?\\s*)(\\*/)', re.M)
preserve_indent_exp = re.compile('\\n\\s*(.*)', re.M)

def format_block_comment(comment, indent):
    def indenter(match):
        if len(match.group(1)) == 0:
            return '\n' + indent
        elif match.group(1)[0] == '*':
            return '\n' + indent + ' ' + match.group(1)
        else:
            return '\n' + indent + '   ' + match.group(1)

    match = block_comment_exp.search(comment)
    if match:
        output = join(' ', match.group(1), preserve_indent_exp.sub(indenter, match.group(2)), match.group(3))

        return output

    return comment

class JsonFormatter:
    default_options = {
        'indent_character': '  ',
        'quote_char': '"',
        'normalize_strings': False,
        'spacer': ' ',
        'newline': '\n',
        'remove_comments': False
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
        spacer = self._options['spacer']
        newline = self._options['newline']
        remove_comments = self._options['remove_comments']

        while True:
            should_linebreak = False
            result = reader.read()
            is_comment = False

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
                is_comment = True
                is_last_token_comment = True
                should_linebreak = True
            elif result.type == 'end_line_comment':
                is_comment = True
                is_last_token_comment = True
            elif result.type == 'new_line_comment_block':
                is_comment = True
                should_linebreak = True
            elif result.type == 'in_line_comment_block':
                is_comment = True

            if is_comment and remove_comments:
                continue


            # new line
            if should_linebreak:
                output = join(newline, strip_trailing(output, spacer), indent * self._options['indent_character'])


            # actual character
            if result.type == 'property' and 'force_property_quotes' in self._options and self._options['force_property_quotes']:
                output += ensure_quotes(result.value, self._options['quote_char'])
            elif result.type == 'value' and 'normalize_strings' in self._options and self._options['normalize_strings'] and is_string_value(result.value):
                output += ensure_quotes(result.value, self._options['quote_char'])
            elif result.type == 'end_line_comment':
                output = strip_trailing(output, spacer)
                output += spacer + result.value
            elif result.type == 'new_line_comment_block':
                output += format_block_comment(result.value, indent * self._options['indent_character']) + newline
            elif result.type == 'in_line_comment_block':
                output = strip_trailing(output, spacer)
                output += spacer + format_block_comment(result.value, indent * self._options['indent_character'])
            else:
                output += result.value


            # suffix
            if result.type == 'property_separator':
                output += spacer
            elif result.type == 'value_separator':
                output += spacer
            elif result.type == 'in_line_comment_block':
                output += spacer

        return output
