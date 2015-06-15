#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of py-json-reader.
# https://github.com/socsieng/py-json-reader

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

from preggy import expect

from tests.base import TestCase
from general_formatting import document_builder
from json_formatting import JsonReader
from yaml_formatting import YamlDocumentRenderer

class YamlFormatterTestCase(TestCase):
    def test_should_format_empty_object(self):
        reader = JsonReader('{ }')
        document = document_builder.build(reader)
        renderer = YamlDocumentRenderer(document)

        output = renderer.render()
        expect(output).to_equal('')

    def test_should_format_empty_array(self):
        reader = JsonReader('[ ]')
        document = document_builder.build(reader)
        renderer = YamlDocumentRenderer(document)

        output = renderer.render()
        expect(output).to_equal('')

    def test_should_format_scalar_array(self):
        reader = JsonReader('[1,2,3]')
        document = document_builder.build(reader)
        renderer = YamlDocumentRenderer(document)

        output = renderer.render()
        expect(output).to_equal('- 1\n- 2\n- 3')

    def test_should_format_scalar_array_with_value_comment(self):
        reader = JsonReader('[1,2 /*comment*/,3]')
        document = document_builder.build(reader)
        renderer = YamlDocumentRenderer(document)

        output = renderer.render()
        expect(output).to_equal('- 1\n- 2 # comment\n- 3')

    def test_should_format_single_property(self):
        reader = JsonReader('{"hello":"world"}')
        document = document_builder.build(reader)
        renderer = YamlDocumentRenderer(document)

        output = renderer.render()
        expect(output).to_equal('hello: world')

    def test_should_format_multiple_properties(self):
        reader = JsonReader('{"hello":"world" ,"value":123}')
        document = document_builder.build(reader)
        renderer = YamlDocumentRenderer(document)

        output = renderer.render()
        expect(output).to_equal('hello: world\nvalue: 123')

    def test_should_format_nested_object(self):
        reader = JsonReader('{"hello":"world" ,"obj":{"abc":123}}')
        document = document_builder.build(reader)
        renderer = YamlDocumentRenderer(document)

        output = renderer.render()
        expect(output).to_equal('hello: world\nobj:\n  abc: 123')

    def test_should_format_object_with_array(self):
        reader = JsonReader('{"hello":"world" ,"arr":["hello","world"]}')
        document = document_builder.build(reader)
        renderer = YamlDocumentRenderer(document)

        output = renderer.render()
        expect(output).to_equal('hello: world\narr:\n  - hello\n  - world')

    def test_should_format_array_of_objects(self):
        reader = JsonReader('{"arr":[{"int":123,"str":"hello"},{"int":123,"str":"hello"}]}')
        document = document_builder.build(reader)
        renderer = YamlDocumentRenderer(document)

        output = renderer.render()
        expect(output).to_equal('arr:\n  -\n    int: 123\n    str: hello\n  -\n    int: 123\n    str: hello')

    def test_should_format_array_of_objects_with_tabs(self):
        reader = JsonReader('{"arr":[{"int":123,"str":"hello"},{"int":123,"str":"hello"}]}')
        document = document_builder.build(reader)
        renderer = YamlDocumentRenderer(document, {'indent_character': '\t'})

        output = renderer.render()
        expect(output).to_equal('arr:\n\t-\n\t\tint: 123\n\t\tstr: hello\n\t-\n\t\tint: 123\n\t\tstr: hello')

    def test_should_format_property_with_empty_string(self):
        reader = JsonReader('{\'hello\':\'\'}')
        document = document_builder.build(reader)
        renderer = YamlDocumentRenderer(document)

        output = renderer.render()
        expect(output).to_equal('hello:')

    def test_should_preserve_end_line_comment(self):
        reader = JsonReader('{\'"hello"\':"world", // comment\n\'value\':123}')
        document = document_builder.build(reader)
        renderer = YamlDocumentRenderer(document, {'force_property_quotes': True})

        output = renderer.render()
        expect(output).to_equal('"hello": world # comment\nvalue: 123')

    def test_should_preserve_end_line_comment_forcing_new_line_for_subsequent_tokens(self):
        reader = JsonReader('{\'"hello"\':"world",\n// full line comment\n\'value\'://comment\n123}')
        document = document_builder.build(reader)
        renderer = YamlDocumentRenderer(document, {'force_property_quotes': True})

        output = renderer.render()
        expect(output).to_equal('"hello": world\n# full line comment\nvalue: # comment\n  123')

    def test_should_preserve_multiple_end_line_comment_forcing_new_line_for_subsequent_tokens(self):
        reader = JsonReader('{\'"hello"\':"world",\n// full line comment\n\'value\'://comment\n//comment\n123}')
        document = document_builder.build(reader)
        renderer = YamlDocumentRenderer(document, {'force_property_quotes': True})

        output = renderer.render()
        expect(output).to_equal('"hello": world\n# full line comment\nvalue: # comment\n  # comment\n  123')

    def test_should_preserve_new_line_comment_block(self):
        reader = JsonReader('{\'"hello"\':"world",\n/* comment\nblock */ \'value\':123}')
        document = document_builder.build(reader)
        renderer = YamlDocumentRenderer(document, {'force_property_quotes': True})

        output = renderer.render()
        expect(output).to_equal('"hello": world\n# comment\n# block\nvalue: 123')

    def test_should_preserve_new_line_comment_block_in_nested_object(self):
        reader = JsonReader('{obj:{\'"hello"\':"world",\n/* comment\nblock */ \'value\':123}}')
        document = document_builder.build(reader)
        renderer = YamlDocumentRenderer(document, {'force_property_quotes': True})

        output = renderer.render()
        expect(output).to_equal('obj:\n  "hello": world\n  # comment\n  # block\n  value: 123')

    def test_should_preserve_in_line_comment_block(self):
        reader = JsonReader('{\'"hello"\':"world", /* comment block */ \'value\':123}')
        document = document_builder.build(reader)
        renderer = YamlDocumentRenderer(document, {'force_property_quotes': True})

        output = renderer.render()
        expect(output).to_equal('"hello": world # comment block\nvalue: 123')

    def test_should_preserve_multiple_line_comments_block(self):
        reader = JsonReader('{\'"hello"\':"world", /* comment block */\n/*comment block*/ \'value\':123}')
        document = document_builder.build(reader)
        renderer = YamlDocumentRenderer(document, {'force_property_quotes': True})

        output = renderer.render()
        expect(output).to_equal('"hello": world # comment block\n# comment block\nvalue: 123')
