#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

def clean_all_un_chinese(text, ignores=[]):
    ans = []
    for word in "".join(gen_en_cn_split(text)).split(" "):
        if word in ignores or is_cn_chr(word):
            ans.append(word)
    return "".join(ans)

def gen_en_cn_split(txt):
    cn_state = -1
    for t in txt:
        if cn_state == -1:
            cn_state = 1 if is_cn_chr(t) else 0
            yield t
        elif cn_state == 0:
            if is_cn_chr(t):
                yield u' '
                yield t
                cn_state = 1
            else:
                yield t
        elif cn_state == 1:
            if not is_cn_chr(t):
                yield u' '
                yield t
                cn_state = 0
            else:
                yield t

def is_cn_chr(c):
    return True if re.search(u"[\u4e00-\u9fa5]",c) else False


def removeShapesSymbols(text):
    shapes  = re.compile(u"[\u25A0-\u25FF]")
    symbols = re.compile(u"[\u3000-\u303F]")
    romans  = re.compile(u"[\u2150-\u218F]")
    boxDraw = re.compile(u"[\u2500-\u267F]")
    letterlike = re.compile(u"[\u2100-\u214F]")

    text = shapes.sub("", text)
    text = symbols.sub("", text)
    text = romans.sub("", text)
    text = boxDraw.sub("", text)
    text = letterlike.sub("", text)

    return text

def removeGeneralPunctuation(line):
    generalPunctuation = re.compile(u"\u2000-\u206f")
    line = generalPunctuation.sub("",line)
    return line

def transform_timestamp(timestamp_str):
    """
    itype: timestamp_str unicode (satisfied timestamp)
    rtype: start_time, end_time, so_far
    """
    if not timestamp_str or -1 == timestamp_str.find("-"):
        return "","",""

    start_time,end_time,so_far = "","",""

    start_time = timestamp_str.split("-")[0]
    if "present" == timestamp_str.split("-")[1]:
        so_far = "Y"
    else:
        end_time = timestamp_str.split["-"][1]

    return start_time, end_time, so_far
