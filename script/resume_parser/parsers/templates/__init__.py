#!/usr/bin/env python
# -*- coding: utf-8 -*-


import five1_template_0
import five1_template_1

import zhilian_template_0

import liepin_template_0



templates_dict = {}
templates_dict["five1_parse"] = [five1_template_0, five1_template_1]
templates_dict["zhilian_parse"] = [zhilian_template_0]
templates_dict["liepin_parse"] = [liepin_template_0]

def get_parse_templates(parser_name):
    return templates_dict.get(parser_name, [])

