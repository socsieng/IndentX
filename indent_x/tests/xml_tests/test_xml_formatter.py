#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of IndentX.
# https://github.com/socsieng/IndentX

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

from preggy import expect

from indent_x.tests.base import TestCase
from indent_x.xml_formatting import XmlIndentFormatter

class XmlIndentFormatterTestCases(TestCase):
    def test_should_format_basic_xml(self):
        formatter = XmlIndentFormatter(' ')
        formattedText = formatter.indent('<root><child></child><child/><child with="this attribute" and="that attribute" /></root>')
        expect(formattedText).to_equal('<root>\n <child></child>\n <child/>\n <child with="this attribute" and="that attribute" />\n</root>')

    def test_should_format_xml_with_comment(self):
        formatter = XmlIndentFormatter(' ')
        formattedText = formatter.indent('<root><!--comment--><child></child></root>')
        expect(formattedText).to_equal('<root>\n <!--comment-->\n <child></child>\n</root>')

    def test_should_format_xml_removing_white_space(self):
        formatter = XmlIndentFormatter(' ')
        formattedText = formatter.indent('<root><!--comment--><child></child></root>')
        expect(formattedText).to_equal('<root>\n <!--comment-->\n <child></child>\n</root>')

    def test_should_format_malformed_xml(self):
        formatter = XmlIndentFormatter(' ')
        formattedText = formatter.indent('<root><child><child with="this attribute" and="that attribute" /></root>')
        expect(formattedText).to_equal('<root>\n <child>\n  <child with="this attribute" and="that attribute" />\n </root>')

    def test_should_format_strip_comments(self):
        formatter = XmlIndentFormatter('', True)
        formattedText = formatter.indent('<root>\n <!-- comment -->\n <child a="1"\nb="2"></child>\n</root>')
        expect(formattedText).to_equal('<root><child a="1" b="2"></child></root>')

    def test_should_format_xml_removing_white_space(self):
        formatter = XmlIndentFormatter(' ', False, True)
        formattedText = formatter.indent('<root>\n\n\n<!--comment--><child></child></root>')
        expect(formattedText).to_equal('<root>\n <!--comment-->\n <child></child>\n</root>')

    def test_should_format_strip_comments_and_white_pace(self):
        formatter = XmlIndentFormatter('', True, True)
        formattedText = formatter.indent('<root>\n\n\n\n <!-- comment -->\n <child a="1"\nb="2"></child>\n</root>')
        expect(formattedText).to_equal('<root><child a="1" b="2"></child></root>')
