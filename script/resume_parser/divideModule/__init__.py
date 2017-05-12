#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
from functools import partial

from resume_parser.utils import StringUtils
from resume_parser.recognize import timepair_match


"""
DivideModule
usage:
1, divide text to content block
2, divide text to exp block

/*
* # 0 基本信息, 1 联系方式, 2 期望信息, 3 自我评价,
* # 4 工作经历, 5 教育经历, 6 项目经历, 7 证书模块,
* # 8 语言模块, 9 培训经历,
* # 99 其他
*/
"""


def divideHeadlineBlock(text, headlines={}, isOnly=False):
    """
    :itype: text: unicode
    :itype: headlines: list[unicode]
    :itype: isOnly: boolean
    :rtype: list[[title], unicode] 保证切出来的text被join后保持为原来的文本
    """

    if isOnly:
        headlines_dict = headlines
    else:
        headlines_dict = dict(global_headline, **headlines)


    blocks = []

    lines_clean = map(_clean_cand_headline, text.split("\n") )
    lines = text.split("\n")
    for i in xrange(len(lines)):
        if i == 0:
            h = _isHeadline("", lines_clean[i], headlines_dict)
            blocks.append([h if h else [99], lines[i]])
            continue
        h = _isHeadline(lines_clean[i-1], lines_clean[i], headlines_dict)
        if h:
            blocks.append([h, lines[i]])
        else:
            blocks[-1][1] += '\n'+lines[i]

    return blocks


def divideExpBlock(text, timeRegs=None):
    """
    :itype: text: unicode
    :itype: timeReg: Pattern
    :rtype: list[unicode]
    """
    if timeRegs:
        timematch = partial(timepair_match.match_timestamp_by_reg, timeRegs)
    else:
        timematch = timepair_match.match_timestamp




def print_HeadlineBlock(blocks):
    for block in blocks:
        print block[0]
        print "======="
        print block[1]


def getNameByBid(bid):
    return bid_name_dict.get(bid, "unknow")


def init_readconf():
    conf_file_path = os.path.join(os.path.dirname(__file__),"headlines_dict.conf")
    global_headline = {}
    bid_name_dict = {}
    with open(conf_file_path) as fp:
        for line in fp:
            line = line.strip().decode('utf8')
            if line.startswith('#'):
                continue
            items = line.split(',');
            if len(items)<3: continue;
            m_id = int(items[0])
            m_name = items[1]
            bid_name_dict[m_id] = m_name
            for word in items[2].split(';'):
                if word.strip():
                    global_headline[word.strip()] = m_id
    return global_headline, bid_name_dict


def _isHeadline(preline, line, headlines_dict):
    if re.search(u"(所属行业)|(行业类别)", preline):
        return None

    if line in headlines_dict:
        return [headlines_dict[line]]

    if '/' in line:
        ret = []
        for l in line.split('/'):
            h = _isHeadline(preline, l, headlines_dict)
            if h: ret.extend(h)
        return ret if ret else None

    return None


def _clean_cand_headline(text):
    text = text.strip().upper()
    text = StringUtils.clean_all_un_chinese(text, ["/", "IT"])
    return text


# global dict init
global_headline, bid_name_dict = init_readconf()


