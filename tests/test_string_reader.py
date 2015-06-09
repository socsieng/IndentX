#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of py-json-reader.
# https://github.com/socsieng/py-json-reader

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

from preggy import expect

from tests.base import TestCase
from json_formatting import StringReader

class StringReaderTestCase(TestCase):
    def test_should_read_full_string(self):
        reader = StringReader('"has token"')
        expect(reader.read()).to_equal('"has token"')

    def test_should_read_full_string_single(self):
        reader = StringReader('\'has token\'')
        expect(reader.read()).to_equal('\'has token\'')

    def test_should_read_partial_string(self):
        reader = StringReader('"partial string')
        expect(reader.read()).to_equal('"partial string')

    def test_should_read_string_with_escaped_characters(self):
        reader = StringReader('"special string\\""')
        expect(reader.read()).to_equal('"special string\\""')

    def test_should_read_string_with_nested_characters(self):
        reader = StringReader('"the people\'s string"')
        expect(reader.read()).to_equal('"the people\'s string"')

    def test_should_read_string_terminated_by_new_line(self):
        reader = StringReader('"this has a\nnew line"')
        expect(reader.read()).to_equal('"this has a')

    def test_should_not_read_value_not_starting_with_string_character(self):
        reader = StringReader('blah "stuff"')
        expect(reader.read()).to_equal(None)
