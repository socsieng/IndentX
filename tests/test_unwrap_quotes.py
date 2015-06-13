#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of py-json-reader.
# https://github.com/socsieng/py-json-reader

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

from preggy import expect

from tests.base import TestCase
from general_formatting.string_utility import unwrap_quotes

class UnwrapQuotesTestCase(TestCase):
    def test_should_unwrap_basic_single_quotes(self):
        output = unwrap_quotes('\'hello\'')
        expect(output).to_equal('hello')

    def test_should_unwrap_basic_double_quotes(self):
        output = unwrap_quotes('"hello"')
        expect(output).to_equal('hello')

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
