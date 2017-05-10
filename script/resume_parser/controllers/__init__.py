#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
dirpath = os.path.dirname(__file__)
deppath = os.path.join(dirpath, "../../thirdlib")
sys.path.append(deppath)



import parser_controller

parser_map = {}
parser_map["resume_parse"] = parser_controller

def getController(m):
    """
    itype: m: unicode
    rtype: controller: one py model 
    """
    return parser_map.get(m, None)
    


