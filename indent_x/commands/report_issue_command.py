#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of IndentX.
# https://github.com/socsieng/IndentX

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

import urllib

urlencode = None

try:
    from urllib import parse
    urlencode = urllib.parse.urlencode
except (ImportError) as e:
    print(e.message)

if urlencode == None:
    try:
        import urllib
        urlencode = urllib.urlencode
    except (ImportError) as e:
        print(e.message)

from indent_x.general_formatting.string_utility import join

issue_url = 'https://github.com/socsieng/IndentX/issues/new'
issue_template = '''Issue with command: %s

Sample input:

```
// provide sample here
```

Expected result:

```
// provide expected result here
```
'''

def create_issue_url(command_name):
    return join('?', issue_url, urlencode({'body': issue_template % command_name}))

class ReportIssueCommand:
    def __init__(self, view, os, sys):
        self.view = view
        self.os = os
        self.sys = sys

    def is_enabled(self):
        return urlencode != None

    def run(self, edit):
        regions = self.view.sel()
        indentString = '\t'
        settings = self.view.settings()

        last_command = settings.get('indent_x_last_command')

        url = create_issue_url(last_command if last_command else '{command name}')

        cmd = 'open "%s"'
        if self.sys.platform.startswith('linux'):
            cmd = 'xdg-open "%s"'
        elif self.sys.platform.startswith('win'):
            cmd = 'cmd /c start %s'

        cmd = cmd % url
        print('executing: %s' % cmd)
        self.os.system(cmd)
