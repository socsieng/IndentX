#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of IndentX.
# https://github.com/socsieng/IndentX

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

from general_formatting.collection import Collection
from general_formatting.comment import Comment
from general_formatting.document import Document
from general_formatting.property import Property
from general_formatting.property_name import PropertyName
from general_formatting.value import Value

def build(reader):
    document = None

    while True:
        result = reader.read()
        if not result:
            break

        if result.type == 'begin_object':
            document = create_document(reader)
        elif result.type == 'begin_array':
            document = create_collection(reader)

        comment = handle_comments(result)
        if comment:
            document.children.append(comment)

    return document

def create_document(reader):
    document = Document()

    while True:
        result = reader.read()

        if not result or result.type == 'end_object':
            break

        element = None

        if result.type == 'property':
            element = create_property(result, reader)

        comment = handle_comments(result)
        if comment:
            element = comment

        if element:
            document.children.append(element)

    return document

def create_property(propertyResult, reader):
    propName = PropertyName(propertyResult.value)
    prop = Property(propName)

    while True:
        result = reader.peek()

        if not result or result.type == 'end_object' or result.type == 'value_separator':
            break

        reader.move()

        if result.type == 'value':
            val = create_value(result, reader)
            prop.value = val
        elif result.type == 'begin_object':
            document = create_document(reader)
            prop.value = Value(document)
        elif result.type == 'begin_array':
            document = create_collection(reader)
            prop.value = Value(document)

        comment = handle_comments(result)
        if comment:
            if prop.value:
                prop.value.comments.append(comment)
            else:
                propName.comments.append(comment)

    return prop

def create_value(valueResult, reader):
    val = Value(valueResult.value)

    while True:
        result = reader.peek()
        if not result or result.type == 'begin_object' or result.type == 'end_object' or result.type == 'begin_array' or result.type == 'end_array' or result.type == 'value_separator':
            break

        reader.move()
        
        comment = handle_comments(result)
        if comment:
            val.comments.append(comment)

    return val

def create_collection(reader):
    document = Collection()

    while True:
        result = reader.read()

        if not result or result.type == 'end_array':
            break

        element = None

        if result.type == 'begin_object':
            doc = create_document(reader)
            element = Value(doc)
        if result.type == 'begin_array':
            doc = create_collection(reader)
            element = Value(doc)
        if result.type == 'value':
            element = create_value(result, reader)

        comment = handle_comments(result)
        if comment:
            element = comment

        if element:
            document.children.append(element)

    return document

def handle_comments(result):
    comment = None

    if result.type == 'new_line_comment' or result.type == 'end_line_comment' or result.type == 'in_line_comment_block' or result.type == 'new_line_comment_block':
        comment = Comment(result.type, result.value)

    return comment
