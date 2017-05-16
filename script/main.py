#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json

import resume_parser.controllers.parser_controller as parser




filepath = sys.argv[1]
ori = open(filepath).read()


req={}
req["filename"] = filepath.split('/')[-1]
req["filetext"] = ""
req["fileori"]  = ori

print json.dumps(parser.run(req), ensure_ascii=False,sort_keys=True,
        indent=4, separators=(',', ': '))


