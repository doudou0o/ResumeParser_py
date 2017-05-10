#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

print "dir:", dir()
print "name", __name__
print "package", __package__

print sys.path


sys.path.append("/opt/userhome/icchenchen/ecv_parser/resume_parser_module/")
sys.path.append("/opt/userhome/icchenchen/ecv_parser/resume_parser_module/log")

import script

from script.controllers import parser_controller

print open("2.txt").read()

