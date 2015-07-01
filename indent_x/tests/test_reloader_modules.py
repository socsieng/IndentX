#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of IndentX.
# https://github.com/socsieng/IndentX

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

from preggy import expect

from tests.base import TestCase
import glob
import os
import re
import io
import json

mods_load_order = []

with io.open(os.path.join(os.path.dirname(__file__), '../package_util/module_order.json')) as data_file:
    data = json.load(data_file)
    mods_load_order = data

module_expression = re.compile('^[./]*(.+)\.py$')
special_exp = re.compile('[./]')
ignore_mod_exp = [
    re.compile('__init__$'),
    re.compile('^indent_x\.test\.'),
    re.compile('^indent_x\.test_'),
    re.compile('^indent_x\.base$'),
    re.compile('^indent_x\.package_util\.reloader$')
]

class ReloaderModuleTestCases(TestCase):
    pass

def generator(module):
    def test(self):
        exists = module in mods_load_order
        if not exists:
            expect(module).to_equal(True)
    return test

def generate_reload_scenarios():
    def get_module_name(file_path):
        file_name = os.path.relpath(file_path, os.path.dirname(__file__))
        match = module_expression.match(file_name)
        if match:
            return 'indent_x.' + special_exp.sub('.', match.group(1))
        return None

    base_input_files_expression = os.path.join(os.path.dirname(__file__), '../**/*.py')
    files = glob.glob(base_input_files_expression)
    for f in files:
        ignored = False
        mod = get_module_name(f)

        for exp in ignore_mod_exp:
            if exp.search(mod):
                ignored = True
                break

        if ignored:
            continue

        test_case_name = special_exp.sub('_', mod)

        if test_case_name:
            test = generator(mod)
            setattr(ReloaderModuleTestCases, 'test_reload_module_defined_' + test_case_name, test)

generate_reload_scenarios()
