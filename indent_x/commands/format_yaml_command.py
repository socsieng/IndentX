#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of IndentX.
# https://github.com/socsieng/IndentX

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

from indent_x.commands.format_command_base import FormatCommandBase
from indent_x.json_formatting import JsonReader
from indent_x.yaml_formatting import YamlDocumentRenderer
from indent_x.general_formatting import document_builder

class FormatYamlCommand(FormatCommandBase):
    def __init__(self, view, sublime):
        FormatCommandBase.__init__(self, view, sublime)
        self.command_name = 'Convert JSON to YAML'

    def format(self, text, options):
        reader = JsonReader(text)
        document = document_builder.build(reader)
        renderer = YamlDocumentRenderer(document, {'indent_character': options['indent_character']})
        formattedText = renderer.render()

        self.view.set_syntax_file('Packages/YAML/YAML.tmLanguage')

        return formattedText

    def is_enabled(self):
        language = self.get_language()
        return language == 'json' or language == 'plain text'
