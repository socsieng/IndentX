#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of IndentX.
# https://github.com/socsieng/IndentX

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

import re

class Comment:
    def __init__(self, comment_type, value):
        self.comment_type = comment_type
        self._original_value = value
        self.value = value

        if comment_type == 'end_line_comment' or comment_type == 'new_line_comment':
            self.value = re.compile('^//\\s*').sub('', value)
        elif comment_type == 'in_line_comment_block' or comment_type == 'new_line_comment_block':
            self.value = re.compile('/\\*\\s*([\\s\\S]*?)\\s*\\*/').sub('\\1', value)

