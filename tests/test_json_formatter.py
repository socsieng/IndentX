#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of py-json-reader.
# https://github.com/socsieng/py-json-reader

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

from preggy import expect

from tests.base import TestCase
from json_formatting import JsonReader
from json_formatting import JsonFormatter
from json_formatting import ensure_quotes

class JsonFormatterTestCase(TestCase):
    def test_should_format_empty_object(self):
        reader = JsonReader('{ }')
        formatter = JsonFormatter(reader)

        output = formatter.format()
        expect(output).to_equal('{}')

    def test_should_format_empty_array(self):
        reader = JsonReader('[ ]')
        formatter = JsonFormatter(reader)

        output = formatter.format()
        expect(output).to_equal('[]')

    def test_should_format_scalar_array(self):
        reader = JsonReader('[1,2,3]')
        formatter = JsonFormatter(reader)

        output = formatter.format()
        expect(output).to_equal('[1, 2, 3]')

    def test_should_format_single_property(self):
        reader = JsonReader('{"hello":"world"}')
        formatter = JsonFormatter(reader)

        output = formatter.format()
        expect(output).to_equal('{\n  "hello": "world"\n}')

    def test_should_format_multiple_properties(self):
        reader = JsonReader('{"hello":"world" ,"value":123}')
        formatter = JsonFormatter(reader)

        output = formatter.format()
        expect(output).to_equal('{\n  "hello": "world",\n  "value": 123\n}')

    def test_should_format_nested_object(self):
        reader = JsonReader('{"hello":"world" ,"obj":{"abc":123}}')
        formatter = JsonFormatter(reader)

        output = formatter.format()
        expect(output).to_equal('{\n  "hello": "world",\n  "obj": {\n    "abc": 123\n  }\n}')

    def test_should_format_object_with_array(self):
        reader = JsonReader('{"hello":"world" ,"arr":["hello","world"]}')
        formatter = JsonFormatter(reader)

        output = formatter.format()
        expect(output).to_equal('{\n  "hello": "world",\n  "arr": ["hello", "world"]\n}')

    def test_should_format_array_of_objects(self):
        reader = JsonReader('{"arr":[{"int":123,"str":"hello"},{"int":123,"str":"hello"}]}')
        formatter = JsonFormatter(reader)

        output = formatter.format()
        expect(output).to_equal('{\n  "arr": [{\n    "int": 123,\n    "str": "hello"\n  }, {\n    "int": 123,\n    "str": "hello"\n  }]\n}')

    def test_should_format_array_of_objects_with_tabs(self):
        reader = JsonReader('{"arr":[{"int":123,"str":"hello"},{"int":123,"str":"hello"}]}')
        formatter = JsonFormatter(reader, {'indent_character': '\t'})

        output = formatter.format()
        expect(output).to_equal('{\n\t"arr": [{\n\t\t"int": 123,\n\t\t"str": "hello"\n\t}, {\n\t\t"int": 123,\n\t\t"str": "hello"\n\t}]\n}')

    def test_should_format_multiple_properties_with_forced_double_quotes(self):
        reader = JsonReader('{hello:"world" ,value:123}')
        formatter = JsonFormatter(reader, {'force_property_quotes': True})

        output = formatter.format()
        expect(output).to_equal('{\n  "hello": "world",\n  "value": 123\n}')

    def test_should_format_single_quote_properties_with_forced_double_quotes(self):
        reader = JsonReader('{\'hello\':"world" ,\'value\':123}')
        formatter = JsonFormatter(reader, {'force_property_quotes': True})

        output = formatter.format()
        expect(output).to_equal('{\n  "hello": "world",\n  "value": 123\n}')

    def test_should_format_escape_properties_with_forced_double_quotes(self):
        reader = JsonReader('{\'"hello"\':"world" ,\'value\':123}')
        formatter = JsonFormatter(reader, {'force_property_quotes': True})

        output = formatter.format()
        expect(output).to_equal('{\n  "\\"hello\\"": "world",\n  "value": 123\n}')

    def test_should_format_properties_with_forced_single_quotes(self):
        reader = JsonReader('{\'hello\':"world" ,"value":123}')
        formatter = JsonFormatter(reader, {'force_property_quotes': True, 'quote_char': '\''})

        output = formatter.format()
        expect(output).to_equal('{\n  \'hello\': "world",\n  \'value\': 123\n}')

    def test_should_format_property_with_empty_string_and_normalized_strings(self):
        reader = JsonReader('{\'hello\':\'\'}')
        formatter = JsonFormatter(reader, {'force_property_quotes': True, 'normalize_strings': True})

        output = formatter.format()
        expect(output).to_equal('{\n  "hello": ""\n}')

    def test_should_format_property_values_with_normalized_strings(self):
        reader = JsonReader('{\'hello\':"world" ,"value":123}')
        formatter = JsonFormatter(reader, {'force_property_quotes': True, 'quote_char': '\'', 'normalize_strings': True})

        output = formatter.format()
        expect(output).to_equal('{\n  \'hello\': \'world\',\n  \'value\': 123\n}')

    def test_should_preserve_end_line_comment(self):
        reader = JsonReader('{\'"hello"\':"world", // comment\n\'value\':123}')
        formatter = JsonFormatter(reader, {'force_property_quotes': True})

        output = formatter.format()
        expect(output).to_equal('{\n  "\\"hello\\"": "world", // comment\n  "value": 123\n}')

    def test_should_preserve_end_line_comment_forcing_new_line_for_subsequent_tokens(self):
        reader = JsonReader('{\'"hello"\':"world",\n// full line comment\n\'value\'://comment\n123}')
        formatter = JsonFormatter(reader, {'force_property_quotes': True})

        output = formatter.format()
        expect(output).to_equal('{\n  "\\"hello\\"": "world",\n  // full line comment\n  "value": //comment\n  123\n}')

    def test_should_preserve_new_line_comment_block(self):
        reader = JsonReader('{\'"hello"\':"world",\n/* comment\nblock */ \'value\':123}')
        formatter = JsonFormatter(reader, {'force_property_quotes': True})

        output = formatter.format()
        expect(output).to_equal('{\n  "\\"hello\\"": "world",\n  /* comment\nblock */\n  "value": 123\n}')

    def test_should_preserve_in_line_comment_block(self):
        reader = JsonReader('{\'"hello"\':"world", /* comment block */ \'value\':123}')
        formatter = JsonFormatter(reader, {'force_property_quotes': True})

        output = formatter.format()
        expect(output).to_equal('{\n  "\\"hello\\"": "world", /* comment block */\n  "value": 123\n}')
