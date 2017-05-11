#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import resume_parser.controllers.parser_controller as parser




filepath = sys.argv[1]
ori = open(filepath).read()


req={}
req["filename"] = filepath.split('/')[-1]
req["filetext"] = ""
req["fileori"]  = ori

print parser.run(req)


