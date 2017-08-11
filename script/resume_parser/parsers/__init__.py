#!/usr/bin/env python
# -*- coding: utf-8 -*-

import parser_five1
import parser_zhilian
import parser_liepin
import parser_htmltemplate
import parser_general


##### config #####
parsers_dict = {}
parsers_dict["five1"]   = parser_five1
parsers_dict["zhilian"] = parser_zhilian
parsers_dict["liepin"] = parser_liepin

parsers_dict["htmlTemplate"] = parser_htmltemplate
parsers_dict["general"] = parser_general

parsernames = parsers_dict.keys()

##### function #####

def get_parser(pname):
    return parsers_dict.get(pname, None)


