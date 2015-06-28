#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of IndentX.
# https://github.com/socsieng/IndentX

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

import urllib

urlencode = None
if hasattr(urllib, 'parse'):
    urlencode = urllib.parse.urlencode
else:
    urlencode = urllib.urlencode

from general_formatting.string_utility import join

issue_url = 'https://github.com/socsieng/IndentX/issues/new'

class ReportIssueCommand:
    def __init__(self, view, os, sys):
        self.view = view
        self.os = os
        self.sys = sys

    def run(self, edit):
        regions = self.view.sel()
        indentString = '\t'
        settings = self.view.settings()
        url = issue_url

        last_command = settings.get('indent_x_last_command')

        if last_command:
            url = join('?', url, urlencode({'title': last_command}))

        cmd = ''
        if self.sys.platform.startswith('darwin'):
            cmd = 'open "%s"' % url
        elif self.sys.platform.startswith('linux'):
            cmd += 'xdg-open "%s"' % url
        elif self.sys.platform.startswith('win'):
            cmd = 'start "%s"' % url

        self.os.system(cmd)
