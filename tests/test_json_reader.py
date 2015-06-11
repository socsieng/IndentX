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

class JsonReaderTestCase(TestCase):
    def test_should_initialize_json_reader(self):
        reader = JsonReader('{}')
        expect(reader._json).to_equal('{}')

    def test_should_read_empty_json_object(self):
        reader = JsonReader('{}')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('begin_object')
        expect(result.value).to_equal('{')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('end_object')
        expect(result.value).to_equal('}')

        result = reader.read()
        expect(result).to_be_false()

    def test_should_read_json_with_strings(self):
        reader = JsonReader('{"hello":"world"}')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('begin_object')
        expect(result.value).to_equal('{')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('property')
        expect(result.value).to_equal('"hello"')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('property_separator')
        expect(result.value).to_equal(':')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('value')
        expect(result.value).to_equal('"world"')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('end_object')
        expect(result.value).to_equal('}')

        result = reader.read()
        expect(result).to_be_false()

    def test_should_read_formatted_json(self):
        reader = JsonReader('{\n  "hello": "world"\n}')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('begin_object')
        expect(result.value).to_equal('{')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('property')
        expect(result.value).to_equal('"hello"')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('property_separator')
        expect(result.value).to_equal(':')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('value')
        expect(result.value).to_equal('"world"')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('end_object')
        expect(result.value).to_equal('}')

        result = reader.read()
        expect(result).to_be_false()

    def test_should_read_json_with_literals(self):
        reader = JsonReader('{hello:123.4}')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('begin_object')
        expect(result.value).to_equal('{')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('property')
        expect(result.value).to_equal('hello')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('property_separator')
        expect(result.value).to_equal(':')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('value')
        expect(result.value).to_equal('123.4')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('end_object')
        expect(result.value).to_equal('}')

        result = reader.read()
        expect(result).to_be_false()

    def test_should_read_json_with_multiple_properties(self):
        reader = JsonReader('{"hello": "world", value: 123.4}')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('begin_object')
        expect(result.value).to_equal('{')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('property')
        expect(result.value).to_equal('"hello"')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('property_separator')
        expect(result.value).to_equal(':')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('value')
        expect(result.value).to_equal('"world"')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('value_separator')
        expect(result.value).to_equal(',')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('property')
        expect(result.value).to_equal('value')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('property_separator')
        expect(result.value).to_equal(':')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('value')
        expect(result.value).to_equal('123.4')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('end_object')
        expect(result.value).to_equal('}')

        result = reader.read()
        expect(result).to_be_false()

    def test_should_read_empty_array(self):
        reader = JsonReader('[]')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('begin_array')
        expect(result.value).to_equal('[')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('end_array')
        expect(result.value).to_equal(']')

        result = reader.read()
        expect(result).to_be_false()

    def test_should_read_basic_array(self):
        reader = JsonReader('[1, 2, 3]')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('begin_array')
        expect(result.value).to_equal('[')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('value')
        expect(result.value).to_equal('1')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('value_separator')
        expect(result.value).to_equal(',')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('value')
        expect(result.value).to_equal('2')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('value_separator')
        expect(result.value).to_equal(',')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('value')
        expect(result.value).to_equal('3')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('end_array')
        expect(result.value).to_equal(']')

        result = reader.read()
        expect(result).to_be_false()

    def test_should_read_complex_array(self):
        reader = JsonReader('[{"int":123,"str":"hello"},{"int":123,"str":"hello"}]')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('begin_array')
        expect(result.value).to_equal('[')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('begin_object')
        expect(result.value).to_equal('{')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('property')
        expect(result.value).to_equal('"int"')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('property_separator')
        expect(result.value).to_equal(':')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('value')
        expect(result.value).to_equal('123')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('value_separator')
        expect(result.value).to_equal(',')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('property')
        expect(result.value).to_equal('"str"')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('property_separator')
        expect(result.value).to_equal(':')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('value')
        expect(result.value).to_equal('"hello"')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('end_object')
        expect(result.value).to_equal('}')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('value_separator')
        expect(result.value).to_equal(',')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('begin_object')
        expect(result.value).to_equal('{')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('property')
        expect(result.value).to_equal('"int"')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('property_separator')
        expect(result.value).to_equal(':')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('value')
        expect(result.value).to_equal('123')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('value_separator')
        expect(result.value).to_equal(',')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('property')
        expect(result.value).to_equal('"str"')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('property_separator')
        expect(result.value).to_equal(':')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('value')
        expect(result.value).to_equal('"hello"')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('end_object')
        expect(result.value).to_equal('}')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('end_array')
        expect(result.value).to_equal(']')

        result = reader.read()
        expect(result).to_be_false()

    def test_should_find_comment_on_line_by_itself(self):
        reader = JsonReader('\t// this is a comment')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('new_line_comment')
        expect(result.value).to_equal('// this is a comment')

    def test_should_find_comment_on_end_of_line(self):
        reader = JsonReader('something // this is a comment')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('value')
        expect(result.value).to_equal('something')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('end_line_comment')
        expect(result.value).to_equal('// this is a comment')

    def test_should_find_new_line_comment_block(self):
        reader = JsonReader('/* this is a\nblock comment */')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('new_line_comment_block')
        expect(result.value).to_equal('/* this is a\nblock comment */')

    def test_should_find_in_line_comment_block(self):
        reader = JsonReader('before /* this is a\nblock comment */ after */')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('value')
        expect(result.value).to_equal('before')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('in_line_comment_block')
        expect(result.value).to_equal('/* this is a\nblock comment */')

        result = reader.read()
        expect(result).to_be_true()
        expect(result.type).to_equal('value')
        expect(result.value).to_equal('after')
