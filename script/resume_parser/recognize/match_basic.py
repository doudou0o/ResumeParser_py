#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import bank

"""
match_phone
match_email
match_gender
match_region
match_language
"""

def match_phone(text):
    reg_phone = "1(3[0-9]|4[57]|5[0-35-9]|7[0135678]|8[0-9])\d{8}"
    m = re.search(reg_phone, text)
    if m:
        return m.group()
    else:
        return None

def match_email(text):
    reg_email = "(?i)[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    m = re.search(reg_email, text)
    if m:
        return m.group()
    else:
        return None


def match_region(text):
    # TODO
    return ""


def match_gender(text):
    if re.search(u"女", text):
        return "F"
    elif re.search(u"男", text):
        return "M"
    elif re.search(u"(?i)female", text):
        return "F"
    elif re.search(u"(?i)male", text):
        return "M"
    else:
        return "U"

def match_marital(text):
    if re.search(u"未婚", text):
        return "N"
    elif re.search(u"已婚", text):
        return "Y"
    elif re.search(u"unmarried", text):
        return "N"
    elif re.search(u"married", text):
        return "Y"
    else:
        return "U"

def match_language(text):
    ans = bank.find_language(text)
    if ans:
        return ans
    else:
        return None
    

