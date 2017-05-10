#!/usr/bin/env python
# -*- coding: utf-8 -*-


from script.divideModule import divideModule
import basic_template_parser


def parse(filename, filetext, fileori):

    resume_ret = basic_template_parser.get_resume_structor("five1 parse")

    blocks = _splitHeadlineBlock(filetext)

    _parseinfo_func_dict = _get_parse_func_dict()

    #divideModule.print_HeadlineBlock(blocks)

    for titles, text in blocks:
        for t in titles:
            m_pret = _parseinfo_func_dict[t](text)
            insert_into_resume_ret(m_pret, t)
        pass

    pass
    return None

def _splitHeadlineBlock(filetext):
    """
    rtype: list[[titles], text] 保证切出来的text被join后保持为原来的文本
    """
    return divideModule.divideHeadlineBlock(filetext, headlines=Headline_Dict)

def _parse_basic_info(text):
    pass

def _parse_contact_info(text):
    pass

def _parse_education_info(text):
    pass

def _get_parse_func_dict():
    """
    可配置方式,一个配置方法
    如果出现需要模块整体需要修正的模板出现,其他方法可以复用
    """
    _parseinfo_func_dict = {}
    _parseinfo_func_dict[0] = _parse_basic_info
    _parseinfo_func_dict[99] = _parse_basic_info
    _parseinfo_func_dict[1] = _parse_contact_info
    _parseinfo_func_dict[5] = _parse_education_info
    return _parseinfo_func_dict

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



