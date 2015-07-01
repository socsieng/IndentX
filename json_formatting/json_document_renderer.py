#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of IndentX.
# https://github.com/socsieng/IndentX

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

import re
import copy

from general_formatting.string_utility import is_string_value, wrap_quotes, join, strip_leading, strip_trailing
from general_formatting.collection import Collection
from general_formatting.comment import Comment
from general_formatting.document import Document
from general_formatting.property import Property
from general_formatting.property_name import PropertyName
from general_formatting.value import Value

class JsonDocumentRenderer:
    default_options = {
        'indent_character': '  ',
        'quote_char': '"'
    }

    def __init__(self, document, options = None):
        self._document = document
        self._options = copy.deepcopy(self.default_options)

        if options:
            self._options.update(options)

    def render(self):
        output = ''
        indent = 0
        doc = self._document

        if not doc:
            return None

        if isinstance(doc, Collection):
            output += self.render_document(doc, indent)
        else:
            output += self.render_document(doc, indent)

        return output

    def render_document(self, doc, indent):
        start = ''
        end = ''
        output = ''

        if isinstance(doc, Collection):
            start += '['
        else:
            start += '{'

        for item in doc.children:
            if isinstance(item, Comment):
                output = strip_trailing(output, ' ') + self.render_comment(item, indent)
            elif isinstance(item, Property):
                output += '\n' + (indent + 1) * self._options['indent_character']
                output += wrap_quotes(item.name.value, self._options['quote_char']) + ': '
                if len(item.name.comments):
                    output = join(' ', output, self.render_comments(item.name.comments, indent))
                    output += '\n' + (indent + 2) * self._options['indent_character']
                    output += self.render_value(item.value, indent + 1)
                else:
                    output = join(' ', output, self.render_value(item.value, indent))
                output += ','
            elif isinstance(item, Value):
                output = join(' ', output, self.render_value(item, indent))
                output += ','

        output = re.compile(', ?$').sub('', output)

        if isinstance(doc, Collection):
            end += ']'
        else:
            if len(doc.children):
                end += '\n'
            end += indent * self._options['indent_character']
            end += '}'

        return start + output + end

    def render_comment(self, comment, indent):
        if comment.comment_type == 'new_line_comment' or comment.comment_type == 'new_line_comment_block':
            output = '\n' + (indent + 1) * self._options['indent_character']
        else:
            output = ' '
        output += comment._original_value
        return output

    def render_comments(self, comments, indent):
        output = ''
        for comment in comments:
            if output == '':
                output = join(' ', output, self.render_comment(comment, indent))
            else:
                output = join('\n', output, self.render_comment(comment, indent + 1))
        return output

    def render_value(self, val, indent):
        output = ''

        if val.value_type == 'string':
            output = wrap_quotes(val.value, self._options['quote_char'])
        elif val.value_type == 'object':
            output = self.render_document(val.value, indent + 1)
        elif val.value_type == 'array':
            output = self.render_document(val.value, indent)
        else:
            output = val.value

        return output
