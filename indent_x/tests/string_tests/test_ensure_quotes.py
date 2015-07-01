#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of py-json-reader.
# https://github.com/socsieng/py-json-reader

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

from preggy import expect

from indent_x.tests.base import TestCase
from indent_x.general_formatting.string_utility import ensure_quotes

class EnsureQuotesTestCase(TestCase):
    def test_should_add_quotes_to_unquoted_value(self):
        output = ensure_quotes('hello', '"')
        expect(output).to_equal('"hello"')

    def test_should_not_add_quotes_to_quoted_value(self):
        output = ensure_quotes('"hello"', '"')
        expect(output).to_equal('"hello"')

    def test_should_not_add_quotes_to_unterminated_value(self):
        output = ensure_quotes('"hello', '"')
        expect(output).to_equal('"hello"')

    def test_should_flip_empty_single_quotes_to_double_quotes(self):
        output = ensure_quotes('\'\'', '"')
        expect(output).to_equal('""')

    def test_should_flip_single_quotes_to_double_quotes(self):
        output = ensure_quotes('\'hello\'', '"')
        expect(output).to_equal('"hello"')

    def test_should_flip_double_quotes_to_single_quotes(self):
        output = ensure_quotes('"hello"', '\'')
        expect(output).to_equal('\'hello\'')

    def test_should_escape_double_quotes_within_string(self):
        output = ensure_quotes('\'hi "all"\'', '"')
        expect(output).to_equal('"hi \\"all\\""')

    def test_should_unescape_single_quotes_within_string(self):
        output = ensure_quotes('\'how\\\'s it going?\'', '"')
        expect(output).to_equal('"how\'s it going?"')

    def test_should_unescape_double_quotes_within_string(self):
        output = ensure_quotes('"I\'m \\"great\\""', '\'')
        expect(output).to_equal('\'I\\\'m "great"\'')

    def test_should_not_escape_already_escaped_quotes(self):
        output = ensure_quotes('\'how\\\'s it \\"going\\"?\'', '"')
        expect(output).to_equal('"how\'s it \\"going\\"?"')
