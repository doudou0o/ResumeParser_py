#!/usr/bin/env python
# -*- coding: utf-8 -*-

from basic_template_parser import TemplateParser
import logging

logger = logging.getLogger("mylog")

class Five1Parser(TemplateParser):
    def __init__(self):
        super(Five1Parser, self).__init__()
        self.parser_name = "five1Parser"
        self.text = ""

    def parse(self, text=""):
        if not text and not self.text:
            raise Exception("no text content for parser", self.parser_name)

        logging.info(text)

        self.text = text
        pass


