#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import logging

import resume_parser.controllers.parser_controller as parser

fm = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
sh = logging.StreamHandler();sh.setLevel(logging.DEBUG)
logger = logging.getLogger("mylog");logger.setLevel(logging.DEBUG)
sh.setFormatter(fm);logger.addHandler(sh)


filepath = sys.argv[1]
ori = open(filepath).read()

req={}
req["filename"] = filepath.split('/')[-1].decode("utf8")
req["filetext"] = ""
req["fileori"]  = ori

print json.dumps(parser.run(req), ensure_ascii=False,sort_keys=True,
        indent=4, separators=(',', ': '))


