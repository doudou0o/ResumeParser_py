#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import random
from itertools import izip

from resume_parser import divideModule
from resume_parser.recognize import match_timestamp
from resume_parser.recognize import match_degree
from resume_parser.recognize import match_basic
from resume_parser import resume_struct
from resume_parser.utils import StringUtils

template_name = "_51job_t0"

def split_headline_block(filetext):
    """
    rtype: list[[titles], text]
    """
    return divideModule.divideHeadlineBlock(filetext, headlines=Headline_Dict)

def split_eduexp_block(text):
    def issplit(i, lines):
        for timestamp in timestamps:
            if re.search(timestamp, lines[i]):
                return True
        return False
    exp_blocks = divideModule.divideExpBlock(text, isSplit=issplit)
    return exp_blocks

def extract_eduinfo(expblock):
    found_school = False
    lastline = ""
    edu = resume_struct.get_education_struct()
    edu["ori_text"] = expblock
    for line in expblock.split("\n"):
        if not found_school:
            m = re.search(edu_reg, line)
            if m:
                timestamp = match_timestamp.match_timestamp_by_reg(line, edu_reg)
                edu["school"] = m.group("school")
                edu["start_time"], edu["end_time"], edu["so_far"] = StringUtils.transform_timestamp(timestamp)
        elif lastline == "school":
            items = line.split("|")
            if len(items) >= 2:
                edu["degree"] = match_degree.match_degree(items, 99)
                edu["degree_ori"] = items[0]
                edu["discipline_name"] = items[1]
            else:
                if match_degree.match_degree(items):
                    edu["degree"] = match_degree.match_degree(items)
                    edu["degree_ori"] = items[0]
                else:
                    edu["discipline_name"] = items[0]
        elif lastline == "degree":
            edu["discipline_desc"] += '\n'+line
        pass
    pass

def extract_basicinfo(text):
    basic_info = {}
    basic_info["ori_text_"+str(random.randint(0,1000))] = text

    lines = text.split('\n')
    for line_pre, line in izip([""]+lines, lines):
        ## name update
        if re.search(u"(.+)\s+流程状态.+标签.+", line):
            basic_info["name"] = re.search(u"(.+)\s+流程状态", line).group(1).strip()
            if line_pre.strip().startswith(u"更新时间："):
                m = re.search("\d{4}-\d{2}-\d{2}", line_pre)
                if m: basic_info["updated_at"]=m.group()
        ## email phone
        email = match_basic.match_email(line)
        phone = match_basic.match_phone(line)
        if email: basic_info["contact_email"] = email
        if phone: basic_info["contact_phone"] = phone
        ## gender age birth
        if "U" != match_basic.match_gender(line) and (u"岁" in line or u"经验" in line):
            basic_info["gender"] = match_basic.match_gender(line)
        mage = re.search(u"\d+岁", line)
        if mage: basic_info["age"] = int(mage.group()[:-1])
        mbirth = re.search(u"\d{4}年\d{2}月\d{2}日", line)
        if mbirth: basic_info["birth"] = mbirth.group()
        ## others
        mtel = re.search(u"家庭电话：(.+)", line)
        if mtel: basic_info["contact_tel"] = mtel.group(1).strip()
        mexp = re.search(u"(\d+)年工作经验", line)
        if mexp: basic_info["work_experience"] = int(mexp.group(1))
        mmary = re.search(u"婚姻状况：(.+)", line)
        if mmary: basic_info["marital"] = mmary.group(1).strip()
        maccount = re.search(u"户口/国籍：(.+)", line)
        if maccount:
            basic_info["account_str"] = maccount.group(1).strip()
            basic_info["account"] = match_basic.match_region(maccount.group(1).strip())
        maddress = re.search(u"现居住?(.+?)(\||$)", line)
        if maddress:
            basic_info["address_str"] = maddress.group(1).strip()
            basic_info["address"] = match_basic.match_region(maddress.group(1).strip())

    return  basic_info

def extract_contactinfo(text, contact_info_ori):
    contact_info = {}

    phone = match_basic.match_phone(text)
    email = match_basic.match_email(text)
    if phone: contact_info["phone"] = phone
    if email: contact_info["email"] = phone

    for line in text.split('\n'):
        mtel = re.search(u"家庭电话：(.+)", line)
        if mtel: contact_info["contact_tel"] = mtel.group(1)
    pass
    return contact_info


###### 51job_0 template config
# 51job headlines
Headline_Dict={}
Headline_Dict[u"个人信息"] =  0
Headline_Dict[u"求职意向"] =  2
Headline_Dict[u"教育经历"] =  5
Headline_Dict[u"工作经验"] =  4
Headline_Dict[u"项目经验"] =  6
Headline_Dict[u"语言能力"] =  8

Headline_Dict[u"所获奖项"] = 99
Headline_Dict[u"培训经历"] =  9
Headline_Dict[u"在校情况"] = 99
Headline_Dict[u"最近工作"] = 99
Headline_Dict[u"自我评级"] = 99
Headline_Dict[u"技能特长"] = 99
Headline_Dict[u"社会经验"] = 99
Headline_Dict[u"校内职务"] = 99
Headline_Dict[u"其他信息"] = 99
Headline_Dict[u"IT技能"]   = 99
Headline_Dict[u"证书"]     =  7
Headline_Dict[u"附件"]     = 99

# 51job edu config
timestamps = [
    u"^\d{4}/\d{1,2}\s*-\s*((\d{4}/\d{1,2})|至今)",
    u"^\d{4}\s*/\d{1,2}"]

edu_reg = u"(?P<sy>\d{4})\s*/\s*(?P<sm>\d{1,2})-(((?P<ey>\d{4})\s*/\s*(?P<em>\d{1,2}))|(?P<ep>至今))\s+(?P<school>.+)"

# 51job work config
company_start = u"\d{4}/\d{1,2}\s*-\s*(\d{4}/\d{1,2}|至今)\s*(.+)(\d+年|\d+个月)"

