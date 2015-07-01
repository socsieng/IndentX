#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of IndentX.
# https://github.com/socsieng/IndentX

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

import re

def is_string_value(input_string):
    char = input_string[0]
    return char == '\'' or char == '"'

def ensure_quotes(input_string, quote_char = '"'):
    other_char = '\'' if quote_char == '"' else '"'
    esc_quote_exp = re.compile('(?<!\\\\)(' + quote_char + ')')
    unesc_quote_exp = re.compile('(\\\\' + other_char + ')')
    wrap_exp = re.compile('^["\']?(.*?)["\']?$', re.M)

    def quote_replacer(match):
        inner = match.group(1)
        inner = unesc_quote_exp.sub(other_char, inner)
        inner = esc_quote_exp.sub('\\\\\\1', inner)
        return quote_char + inner + quote_char

    output = wrap_exp.sub(quote_replacer, input_string)

    return output

def wrap_quotes(input_string, quote_char = '"'):
    other_char = '\'' if quote_char == '"' else '"'
    esc_quote_exp = re.compile('(?<!\\\\)([\\\\' + quote_char + '])')
    unesc_quote_exp = re.compile('(\\\\' + other_char + ')')

    output = unesc_quote_exp.sub(other_char, input_string)
    output = esc_quote_exp.sub('\\\\\\1', output)
    return quote_char + output + quote_char

def unwrap_quotes(input_string):
    if is_string_value(input_string):
        output = re.compile('^' + input_string[0]).sub('', input_string)
        output = re.compile(input_string[0] + '$').sub('', output)
        output = re.compile('\\\\([\\\\"\'])').sub('\\1', output)
        return output

    return input_string

def strip_leading(input_string, char):
    if not char:
        return input_string
    start_exp = re.compile('^' + re.escape(char) + '+')
    return start_exp.sub('', input_string)

def strip_trailing(input_string, char):
    if not char:
        return input_string
    end_exp = re.compile(re.escape(char) + '+$')
    return end_exp.sub('', input_string)

def join(char, *params):
    is_first = True
    output = ''
    for p in params:
        if is_first:
            if p == '':
                continue

            is_first = False
            output += strip_trailing(p, char)
        else:
            output += char + strip_leading(strip_trailing(p, char), char)

    return output
