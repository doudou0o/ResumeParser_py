#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

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
    elif re.search(u"female", text):
        return "F"
    elif re.search(u"male", text):
        return "M"
    else:
        return "U"
