#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of IndentX.
# https://github.com/socsieng/IndentX

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

import sys
import imp
import json
import os
import io

mods_load_order = []

with io.open(os.path.join(os.path.dirname(__file__), 'module_order.json')) as data_file:
    data = json.load(data_file)
    mods_load_order = data

for mod in mods_load_order:
    if mod in sys.modules:
        try:
            print('reloading: %s' % mod)
            imp.reload(sys.modules[mod])
        except ImportError:
            pass
