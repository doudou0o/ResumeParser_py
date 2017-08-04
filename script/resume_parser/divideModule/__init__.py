#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os

from resume_parser.utils import StringUtils


"""
DivideModule
usage:
1, divide text to content block
2, divide text to exp block

/*
* # 0 基本信息, 1 联系方式, 2 期望信息, 3 自我评价,
* # 4 工作经历, 5 教育经历, 6 项目经历, 7 证书模块,
* # 8 语言模块, 9 培训经历, 10 技能
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
    def nextline(i, lines):
        return lines[i+1] if i+1<len(lines) else ""

    lines_clean = map(_clean_cand_headline, text.split("\n") )
    lines = text.split("\n")
    for i in xrange(len(lines)):
        if i == 0:
            h = _isHeadline("", lines_clean[i], nextline(i,lines), headlines_dict)
            blocks.append([h if h else [99], lines[i]])
            continue
        h = _isHeadline(lines_clean[i-1], lines_clean[i], nextline(i,lines), headlines_dict)
        if h:
            blocks.append([h, lines[i]])
        else:
            blocks[-1][1] += '\n'+lines[i]


    blocks.extend(_split_enResume_block(blocks.pop()))

    return blocks


def divideExpBlock(text, isSplit=None):
    """
    :itype: text: unicode
    :itype: isSplit: function
    :rtype: list[unicode]
    """

    blocks = []
    lines = text.split("\n")

    for i, line in enumerate(lines):
        if isSplit(i, lines):
            blocks.append(line)
        else:
            if len(blocks)<1:continue
            blocks[-1] += "\n"+line
        pass
    return blocks


def text_HeadlineBlock(blocks):
    text = []
    for block in blocks:
        text.append(str(block[0]))
        text.append("=======")
        text.append(block[1])
    return "\n".join(text)


def getNameByBid(bid):
    return bid_name_dict.get(bid, "unknow")

def getBlockByid(blocked_text, bid):
    """
    itype: blocked_text unicode
    itype: bid int
    rtype: block unicode
    """
    isStart,block = False, []
    lines = blocked_text.split('\n')
    for i,line in enumerate(lines):
        if line == "[%d]"%bid:
            if i+1<len(lines) and lines[i+1] == "=======":
                isStart = not isStart
        if isStart:
            block.append(line)
    return "\n".join(block)




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


def _isHeadline(preline, line, nextline, headlines_dict):
    if line == "":
        return None

    if re.search(u"(所属行业)|(行业类别)", preline):
        return None

    if _isHeadline(line, nextline, "", headlines_dict):
        return None

    if line in headlines_dict:
        return [headlines_dict[line]]

    if '/' in line:
        ret = []
        for l in line.split('/'):
            h = _isHeadline(preline, l, "", headlines_dict)
            if h: ret.extend(h)
        return ret if ret else None

    return None

def _split_enResume_block(block):
    blocks = [[block[0], block[1]],]
    text_lines = block[1].split("\n")
    for i, line in enumerate(text_lines):
        if len(text_lines) - i < 10: break
        if not re.search(u"[\u4e00-\u9fa5]", line) and \
                len(re.findall(u"[\u4e00-\u9fa5]","\n".join(text_lines[i:])))<10:
            blocks = [[block[0], "\n".join(text_lines[:i])], [[100], "\n".join(text_lines[i:])]]
            break

    return blocks

def _clean_cand_headline(text):
    text = text.strip().upper()
    text = StringUtils.clean_all_un_chinese(text, ["/", "IT"])
    return text


# global dict init
global_headline, bid_name_dict = init_readconf()


