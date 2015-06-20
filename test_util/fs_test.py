#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of py-json-reader.
# https://github.com/socsieng/py-json-reader

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

import glob
import os
import re

file_name_expression = re.compile('^[^.]+')

def generator(a, b):
    def test(self):
        self.assertEqual(a, b)
    return test

def load_testcases(target_class, test_generator, base_dir, input_files_expression, expected_result_suffix):
    base_input_files_expression = os.path.join(base_dir, input_files_expression)
    files = glob.glob(base_input_files_expression)
    for f in files:
        test_case_name = get_testcase_name(f)
        if test_case_name:
            result_path = os.path.join(os.path.dirname(f), test_case_name + '.' + expected_result_suffix)
            if os.path.exists(result_path):
                input_string = open(f).read()
                expected_string = open(result_path).read()
                test = test_generator(input_string, expected_string)
                setattr(target_class, 'test_' + test_case_name, test)

def get_testcase_name(file_path):
    file_name = os.path.basename(file_path)
    match = file_name_expression.match(file_name)
    if match:
        return match.group(0)
    return None
