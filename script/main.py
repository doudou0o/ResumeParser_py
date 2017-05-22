#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import logging

import resume_parser.controllers.parser_controller as parser

## init log
fm = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
sh = logging.StreamHandler();sh.setLevel(logging.DEBUG)
logger = logging.getLogger("mylog");logger.setLevel(logging.DEBUG)
sh.setFormatter(fm);logger.addHandler(sh)


## input file
filepath = sys.argv[1]
ori = open(filepath).read()


## request
options = {}
#options["ret_type"] = "clean"

req={}
req["filename"] = filepath.split('/')[-1].decode("utf8")
req["filetext"] = ""
req["fileori"]  = ori
req["options"]  = options

## run
ans = parser.run(req)

isShowTinyJson = False
## print ret
if isShowTinyJson:
    print json.dumps(ans, ensure_ascii=False)
else:
    print json.dumps(ans, ensure_ascii=False,sort_keys=True,
            indent=4, separators=(',', ': '))

print "*************************************"
print ans["parser_name"]
print "*************************************"
print ans["ori_block_text"]


print "*************************************"
print u"姓名:%s\t年龄:%d\t性别:%s" % (ans["basic"]["name"],ans["basic"]["age"],ans["basic"]["gender"])
print u"手机:%s\t电话:%s\n" % (ans["contact"]["phone"],ans["contact"]["tel"])

print u"期望地点:%s" % ans["basic"]["expect_city_names"]
print u"期望职位:%s" % ans["basic"]["expect_position_name"]
print u"期望月薪:%d-%d" % (ans["basic"]["expect_salary_from"], ans["basic"]["expect_salary_to"])

print u"\n个人评价:"
print ans["basic"]["self_remark"]

print u"\n教育经历"
for exp in ans["education"]:
    time_zone = exp["start_time"]+" - "+exp["end_time"]
    if exp["so_far"] == "Y": time_zone += u"至今"
    print " | ".join([time_zone, exp["school_name"], exp["discipline_name"], str(exp["degree"])])

print u"\n工作经历"
for exp in ans["work"]:
    time_zone = exp["start_time"]+" - "+exp["end_time"]
    if exp["so_far"] == "Y": time_zone += u"至今"
    print "\t".join([time_zone, exp["corporation_name"]])
    print "\t" + u"职位:%s | 部门:%s" % (exp["position_name"],exp["architecture_name"])

print u"\n项目经历"
for exp in ans["project"]:
    time_zone = exp["start_time"]+" - "+exp["end_time"]
    if exp["so_far"] == "Y": time_zone += u"至今"
    print " | ".join([time_zone, exp["name"]])

print u"\n语言能力"
for exp in ans["language"]:
    print u"语言："+exp["name"] +u"\t程度："+exp["level"]

print u"\n获得证书"
for exp in ans["certificate"]:
    print u"时间："+exp["start_time"] + u"\t证书："+exp["name"]
