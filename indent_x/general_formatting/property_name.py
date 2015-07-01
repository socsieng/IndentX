#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of IndentX.
# https://github.com/socsieng/IndentX

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

from indent_x.general_formatting.string_utility import unwrap_quotes

class PropertyName:
    def __init__(self, value, comments = None):
        self.value = unwrap_quotes(value)
        self.comments = comments if comments else []
