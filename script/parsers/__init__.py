#!/usr/bin/env python
# -*- coding: utf-8 -*-

import five1Parsers
import zhilianParsers
import htmlTemplateParser
import generalParser


##### config #####
parsers_dict = {}
parsers_dict["five1"]   = five1Parsers
parsers_dict["zhilian"] = zhilianParsers
parsers_dict["htmlTemplate"] = htmlTemplateParser
parsers_dict["general"] = generalParser

parsernames = parsers_dict.keys()

##### function #####

def get_parser(pname):
    parsers_dict.get(pname, None)


