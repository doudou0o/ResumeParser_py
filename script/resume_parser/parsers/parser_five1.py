#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import partial

import parser_basic
import templates

"""
51job parser
the origin 51job parser

"""

pname = "five1_parse"

def _parse_basic_info(extract_basicinfo, text):
    """
    itype: extract_basicinfo: function
    itype: text unicode
    rtype: basic struct
    """
    return extract_basicinfo(text)

def _parse_contact_info(extract_contactinfo, text):
    """
    itype: extract_contactinfo: function
    itype: text unicode
    rtype: contact struct
    """
    return extract_contactinfo(text)

def _parse_education_info(split_eduexp_block, extract_eduinfo, text):
    """
    itype: split_eduexp_block: function
    itype: extract_eduinfo: function
    itype: text unicode
    rtype: edu struct
    """
    edu_info_list = []
    exp_blocks = split_eduexp_block(text)
    for exp in exp_blocks:
        edu_info = extract_eduinfo(exp)
        # judge
        # TODO
        edu_info_list.append(edu_info)
    pass
    return edu_info_list

def _parse_employment_info(split_workexp_block, extract_workinfo, text):
    """
    itype: split_workexp_block: function
    itype: extract_workinfo: function
    itype: text unicode
    rtype: work struct
    """
    work_info_list = []
    exp_blocks = split_workexp_block(text)
    for exp in exp_blocks:
        work_info = extract_workinfo(exp)
        # judge
        # TODO
        work_info_list.append(work_info)
    pass
    return work_info_list

def _parse_expect_info(extract_expectinfo, text):
    """
    itype: extract_expectinfo: function
    itype: text unicode
    rtype: map
    """
    return extract_expectinfo(text)

def _parse_language_info(split_lang_block, extract_langinfo, text):
    """
    itype: split_lang_block: function
    itype: extract_langinfo: function
    itype: text unicode
    rtype: language struct
    """
    language_info_list = []
    exp_blocks = split_lang_block(text)
    for exp in exp_blocks:
        language_info = extract_langinfo(exp)
        # judge
        # TODO
        language_info_list.append(language_info)
    pass
    return language_info_list


def _get_parse_func_dict(template):
    """
    可配置方式: 一个配置方法
    如果出现需要模块整体需要修正的模板出现可以重写之
    其他方法可以复用
    """
    _parseinfo_func_dict = {}
    _parseinfo_func_dict[0]  = partial(_parse_basic_info, template.extract_basicinfo)
    _parseinfo_func_dict[3]  = partial(_parse_basic_info, template.extract_basicinfo)
    _parseinfo_func_dict[99] = partial(_parse_basic_info, template.extract_basicinfo)
    _parseinfo_func_dict[2]  = partial(_parse_expect_info, template.extract_expectinfo)
    _parseinfo_func_dict[1] = partial(_parse_contact_info, template.extract_contactinfo)
    _parseinfo_func_dict[5] = partial(_parse_education_info, 
            template.split_eduexp_block, template.extract_eduinfo
            )
    _parseinfo_func_dict[4] = partial(_parse_employment_info, 
            template.split_workexp_block, template.extract_workinfo
            )

    return _parseinfo_func_dict


def parse(filename, filetext, fileori):

    # TODO
    # filename can used to parse or confirm name in resume

    for template in templates.get_parse_templates(pname):
        real_parser = partial(parser_basic.parse,
                        template.split_headline_block,
                        _get_parse_func_dict(template),
                        pname+template.template_name)
        resume_ret = real_parser(filetext)
        if len(resume_ret["work"]) < 1 and len(resume_ret["education"]) < 1:
            continue
        else:
            return resume_ret

    return None


def match(filetext):
    pass




