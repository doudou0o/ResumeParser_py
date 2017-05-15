#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from timeMatcher.time_matcher import TimeMatcher

def match_timestamp(text):
    tm = TimeMatcher()
    ans, tp = tm.extractTimeStamp(text)
    return ans



def match_timestamp_by_reg(reg, text):
    t_reg = re.compile(reg)
    m = t_reg.search(text)
    if m:
        return _build_timestamp_str(m)
    else:
        return None


def match_timestamp_by_regs(regs, text):
    for reg in regs:
        ans = match_timestamp_by_reg(text, reg)
        if ans:
            return ans
    return None



def _build_timestamp_str(match):
    timestamp = ""
    groupdict = match.groupdict()
    if "sy" in groupdict:
        timestamp += groupdict["sy"]+u"年"
    if "sm" in groupdict:
        timestamp += groupdict["sm"]+u"月"
    if "sd" in groupdict:
        timestamp += groupdict["sd"]+u"日"
    timestamp += "-"
    if "ey" in groupdict:
        timestamp += groupdict["ey"]+u"年"
    if "em" in groupdict:
        timestamp += groupdict["em"]+u"月"
    if "ed" in groupdict:
        timestamp += groupdict["ed"]+u"日"
    return timestamp

