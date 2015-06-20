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
    
class YamlDocumentRenderer:
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

        return strip_leading(output, '\n')

    def render_document(self, doc, indent):
        output = ''

        for item in doc.children:
            if isinstance(item, Comment):
                output = strip_trailing(output, ' ') + self.render_comment(item, indent)
            elif isinstance(item, Property):
                output += '\n' + indent * self._options['indent_character']
                output += item.name.value + ': '

                if len(item.name.comments):
                    output = join(' ', output, self.render_comments(item.name.comments, indent + 1))
                    output += '\n' + (indent + 1) * self._options['indent_character']
                    output += self.render_value(item.value, indent + 1)
                elif isinstance(item.value, Value):
                    if isinstance(item.value.value, Document):
                        output = strip_trailing(output, ' ')
                    output += self.render_value(item.value, indent)
                    output = strip_trailing(output, ' ')
            elif isinstance(item, Value):
                output += '\n' + indent * self._options['indent_character'] + '- '
                if isinstance(item.value, Document):
                    output = strip_trailing(output, ' ')
                output += self.render_value(item, indent)

        return output

    def render_comment(self, comment, indent):
        indent_sequence = '\n' + indent * self._options['indent_character'] + '# '
        if comment.comment_type == 'new_line_comment' or comment.comment_type == 'new_line_comment_block':
            output = re.compile('^|\\n').sub(indent_sequence, comment.value)
        else:
            output = ' # ' + comment.value
        return output

    def render_comments(self, comments, indent):
        output = ''
        for comment in comments:
            output += self.render_comment(comment, indent)
        return output

    def render_value(self, val, indent):
        if val.value_type == 'string':
            output = val.value
        elif val.value_type == 'object':
            output = self.render_document(val.value, indent + 1)
        elif val.value_type == 'array':
            output = self.render_document(val.value, indent + 1)
        else:
            output = val.value

        if len(val.comments):
            output = join(' ', output, self.render_comments(val.comments, indent + 1))

        return output
