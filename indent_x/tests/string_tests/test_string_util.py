#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of py-json-reader.
# https://github.com/socsieng/py-json-reader

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

from preggy import expect

from indent_x.tests.base import TestCase
from indent_x.general_formatting.string_utility import unwrap_quotes, wrap_quotes, join

class StringUtilTestCase(TestCase):
    def test_should_unwrap_basic_single_quotes(self):
        output = unwrap_quotes('\'hello\'')
        expect(output).to_equal('hello')

    def test_should_unwrap_basic_double_quotes(self):
        output = unwrap_quotes('"hello"')
        expect(output).to_equal('hello')

    def test_should_unwrap_back_slashes_in_double_quotes(self):
        output = unwrap_quotes('"c:\\\\"')
        expect(output).to_equal('c:\\')

    def test_should_unwrap_single_quotes_containing_double_quote_characters(self):
        output = unwrap_quotes('\'hello "world"\'')
        expect(output).to_equal('hello "world"')

    def test_should_unwrap_double_quotes_containing_single_quote_characters(self):
        output = unwrap_quotes('"hello \'world\'"')
        expect(output).to_equal('hello \'world\'')

    def test_should_unwrap_single_quotes_containing_escaped_single_quote_characters(self):
        output = unwrap_quotes('\'hello \\\'ello\'')
        expect(output).to_equal('hello \'ello')

    def test_should_unwrap_double_quotes_containing_escaped_double_quote_characters(self):
        output = unwrap_quotes('"hello \\"friends\\""')
        expect(output).to_equal('hello "friends"')

    def test_should_wrap_basic_string_in_quotes(self):
        output = wrap_quotes('hello')
        expect(output).to_equal('"hello"')

    def test_should_wrap_quoted_string_in_quotes(self):
        output = wrap_quotes('"hello"')
        expect(output).to_equal('"\\"hello\\""')

    def test_should_join_multiple_strings_with_spaces(self):
        output = join(' ', '1', '2', '3')
        expect(output).to_equal('1 2 3')

    def test_should_join_multiple_strings_with_regex_special_character(self):
        output = join('\\', '1', '2', '3')
        expect(output).to_equal('1\\2\\3')

    def test_should_join_multiple_strings_preserving_first_string_stripping_others(self):
        output = join('/', '/1/', '/2/', '/3')
        expect(output).to_equal('/1/2/3')

    def test_should_join_multiple_strings_with_new_lines(self):
        output = join('\n', '', '1', '2', '3')
        expect(output).to_equal('1\n2\n3')

    def test_should_join_end_object_to_json_with_new_line(self):
        output = join('\n', '{\n  "hello": "world"', '}')
        expect(output).to_equal('{\n  "hello": "world"\n}')

    def test_should_join_whitespace_to_json_with_new_line(self):
        output = join('\n', '{\n  "hello": "world"', ' ')
        expect(output).to_equal('{\n  "hello": "world"\n ')
