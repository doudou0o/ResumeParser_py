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
    if "sy" in groupdict and not groupdict['sy'] is None:
        timestamp += groupdict["sy"]+u"年"
    if "sm" in groupdict and not groupdict['sm'] is None:
        timestamp += groupdict["sm"]+u"月"
    if "sd" in groupdict and not groupdict['sd'] is None:
        timestamp += groupdict["sd"]+u"日"
    timestamp += "-"
    if "ey" in groupdict and not groupdict['ey'] is None:
        timestamp += groupdict["ey"]+u"年"
    if "em" in groupdict and not groupdict['em'] is None:
        timestamp += groupdict["em"]+u"月"
    if "ed" in groupdict and not groupdict['ed'] is None:
        timestamp += groupdict["ed"]+u"日"
    if "ep" in groupdict and not groupdict['ep'] is None:
        timestamp += "present"

    return timestamp

